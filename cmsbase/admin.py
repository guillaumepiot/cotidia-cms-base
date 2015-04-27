import reversion, json

from django.contrib import admin, messages
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages

from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField

from multilingual_model.admin import TranslationStackedInline

from redactor.widgets import RedactorEditor
from filemanager.widgets import MultipleFileWidget

from cmsbase.models import *
from cmsbase.widgets import AdminImageWidget, AdminCustomFileWidget
from cmsbase import settings as cms_settings
from cmsbase.admin_views import *

from codemirror import CodeMirrorTextarea

class PublishingWorkflowAdmin(admin.ModelAdmin):

    

    def get_list_display(self, request, obj=None):
        if not settings.PREFIX_DEFAULT_LOCALE:
            return ['title', 'home_icon', 'is_published', 'approval', 'order_id', 'get_data_set', 'get_template_name', 'content', 'preview']
        else:
            return ['title', 'home_icon', 'is_published', 'approval', 'order_id', 'get_data_set', 'get_template_name', 'languages', 'preview']

    def save_model(self, request, obj, form, change):
        if not obj.id and obj.parent:
            obj.__class__._tree_manager.insert_node(obj, obj.parent)


        obj.save()

        # Rebuild the tree
        obj.__class__._tree_manager.rebuild()

        obj_name = u'%s' % obj._meta.verbose_name

        if obj.publish:
            obj.published = True
            obj.publish = 0
            obj.approve = 0
            obj.approval_needed = 0
            obj.save()
            obj.publish_version()
            obj.publish_inlines = True
            messages.success(request, 'The %s "%s" has been published.' % (obj_name, obj))
            #print 'Publishing has been requested!'
        elif obj.approve:
            #obj.publish_version()
            obj.approval_needed = 1
            obj.approve = 0
            obj.save()
            obj.publish_inlines = False
            messages.warning(request, 'The %s "%s" has been submitted for approval.' % (obj_name, obj))

        else:
            obj.approval_needed = 1
            obj.save()
            obj.publish_inlines = False
            messages.warning(request, 'The %s "%s" changes must be published to go live.' % (obj_name, obj))

        if not obj.published:
            if request.user.has_perm('cmsbase.can_publish') or request.user.is_superuser:
                obj.unpublish_version()

    # Add extra behaviour depending on the button clicked
    def response_change(self, request, obj):
        response = super(PublishingWorkflowAdmin, self).response_change(request, obj)
        if "_preview" in request.POST:
            if obj.get_translations():
                return HttpResponseRedirect("%s?preview" % obj.get_absolute_url())
            else:
                messages.error(request, "%s could not be published because it doesn't have any content yet." % obj)
        elif "_publish" in request.POST:
            if obj.get_translations():
                self._publish_object(obj)
            else:
                messages.error(request, "%s could not be published because it doesn't have any content yet." % obj)
            
        return response

    # Custom result queryset
    def queryset(self, request):
        """
        Remove the published version of the pages
        """
        qs = super(PublishingWorkflowAdmin, self).queryset(request)

        return qs.filter(published_from=None)

    #Custom queryset for the parent foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = db_field.rel.to.objects.filter(published_from=None)
        return super(PublishingWorkflowAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # Set the templates variable based on CMSMeta
    def formfield_for_dbfield(self, db_field, **kwargs):

        if db_field.name == "template":
            db_field._choices = self.model.CMSMeta.templates
        
        return super(PublishingWorkflowAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            if not request.user.has_perm('cmsbase.can_publish') and not request.user.is_superuser:
                return self.readonly_fields + ('slug',)
        return self.readonly_fields

    # Publishing function for an object
    def _publish_object(self, obj):
        obj.approval_needed = False
        obj.published = True
        obj.save()
        obj.publish_version()
        obj.publish_translations()

    # Custom actions
    def make_published(self, request, queryset):
        if request.user.has_perm('cmsbase.can_publish') or request.user.is_superuser:
            for obj in queryset:
                if obj.get_translations():
                    self._publish_object(obj)
                else:
                    messages.error(request, "%s could not be published because it doesn't have any content yet." % obj)

            # Rebuild the tree
            obj.__class__._tree_manager.rebuild()

    make_published.short_description = "Approve & Publish"

    def make_unpublished(self, request, queryset):
        if request.user.has_perm('cmsbase.can_publish') or request.user.is_superuser:
            for obj in queryset:
                obj.published = False
                obj.save()
                obj.unpublish_version()

            # Rebuild the tree
            obj.__class__._tree_manager.rebuild()

    make_unpublished.short_description = "Un-publish"

    def duplicate(self, request, queryset):
        for obj in queryset:
            obj.duplicate()

        # Rebuild the tree
        obj.__class__._tree_manager.rebuild()

    duplicate.short_description = "Duplicate"

    #Assign those actions
    actions = [make_published, make_unpublished, duplicate]



    def get_actions(self, request):
        actions = super(PublishingWorkflowAdmin, self).get_actions(request)
        if not request.user.has_perm('cmsbase.can_publish') and not request.user.is_superuser:
            del actions['make_published']
            del actions['make_unpublished']
            del actions['delete_selected']
        return actions


    # Custom result list
    def home_icon(self, obj):
        if hasattr(obj, 'home') and obj.home:
            return '<i class="glyphicon glyphicon-home"></i>'
        else:
            return ''
    home_icon.allow_tags = True
    home_icon.short_description = 'Home'

    def approval(self, obj):
        if obj.approval_needed:
            return '<i class="glyphicon glyphicon-time"></i>'
        else:
            return '<i class="glyphicon glyphicon-ok"></i>'
    approval.allow_tags = True
    approval.short_description = 'Approved'

    def is_published(self, obj):
        if obj.published:
            return '<i class="glyphicon glyphicon-ok"></i>'
        else:
            return '<i class="glyphicon glyphicon-remove"></i>'
    is_published.allow_tags = True
    is_published.short_description = 'Published'

    def is_active(self, obj):
        if obj.published:
            return '<i class="glyphicon glyphicon-ok"></i>'
        else:
            return '<i class="glyphicon glyphicon-remove"></i>'
    is_active.allow_tags = True
    is_active.short_description = 'Active'

    def get_template_name(self, obj):
        return dict(cms_settings.CMS_PAGE_TEMPLATES).get(obj.template)
    get_template_name.allow_tags = True
    get_template_name.short_description = 'Template'

    def get_data_set(self, obj):
        return obj.dataset
    get_data_set.allow_tags = True
    get_data_set.short_description = 'Data set'

    
    def content(self, obj):
        translation_class_slug = self.model._meta.model_name

        if obj.get_translations().count() == 0:
            return '<a href="%s">+ %s</a>' % (reverse('admin:add_edit_translation_'+translation_class_slug, kwargs={'page_id':obj.id, 'language_code':settings.DEFAULT_LANGUAGE}), _('Add content'))
        else:
            return '<a href="%s">%s</a>' % (reverse('admin:add_edit_translation_'+translation_class_slug, kwargs={'page_id':obj.id, 'language_code':settings.DEFAULT_LANGUAGE}), _('Edit content'))
    content.allow_tags = True
    content.short_description = 'Content'

    


    def languages(self, obj):
        translation_class_slug = self.model._meta.model_name

        available_ts = {}
        ts=[]
        exiting_lang = []
        for t in obj.get_translations():
            exiting_lang.append(t.language_code)
            available_ts[t.language_code] = u'<a href="%s"><img src="/static/admin/img/flags/%s.png" alt="" rel="tooltip" data-title="%s"></a>' % (reverse('admin:add_edit_translation_'+translation_class_slug, kwargs={'page_id':obj.id, 'language_code':t.language_code}), t.language_code, t.__unicode__())
        for language in settings.LANGUAGES:
            if available_ts.get(language[0], False):
                ts.append(available_ts[language[0]])

        if len(available_ts) < len(settings.LANGUAGES):
            # If we have some language already inputted, load the next missing one
            for lang in settings.LANGUAGES:
                if lang[0] not in exiting_lang:
                    next_missing_language = lang[0]
                    break

            ts.append('<a href="%s">+ %s</a>' % (reverse('admin:add_edit_translation_'+translation_class_slug, kwargs={'page_id':obj.id, 'language_code':next_missing_language}), _('Add translation')))
        return ' '.join(ts)

    languages.allow_tags = True
    languages.short_description = 'Translations'

    def preview(self, obj):
        return '<a href="%s?preview" target="_blank">%s</a>' % (obj.get_absolute_url(), _('Preview'))
    preview.allow_tags = True


    def get_urls(self):
        from django.conf.urls import patterns, url
        urls = super(PublishingWorkflowAdmin, self).get_urls()
        translation_class_slug = self.model._meta.model_name
        my_urls = patterns('',
            url(r'translation/(?P<page_id>[-\w]+)/(?P<language_code>[-\w]+)/history/(?P<translation_id>[-\w]+)/', self.admin_site.admin_view(translation_revision), {'model_class':self.model, 'translation_class':self.model.CMSMeta.translation_class}, name='translation_revision_'+translation_class_slug),
            url(r'translation/(?P<page_id>[-\w]+)/(?P<language_code>[-\w]+)/recover/(?P<recover_id>[-\w]+)/', self.admin_site.admin_view(add_edit_translation),{'model_class':self.model, 'translation_class':self.model.CMSMeta.translation_class, 'translation_form_class':self.translation_form_class}, name='translation_recover_'+translation_class_slug),
            url(r'translation/(?P<page_id>[-\w]+)/(?P<language_code>[-\w]+)/', self.admin_site.admin_view(add_edit_translation), {'model_class':self.model, 'translation_class':self.model.CMSMeta.translation_class, 'translation_form_class':self.translation_form_class}, name='add_edit_translation_'+translation_class_slug ),
        )
        return my_urls + urls


class PageFormAdmin(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'errorfield'
    redirect_to = TreeNodeChoiceField(label=_('Redirect to page'), queryset=Page.objects.get_published_originals(), help_text=_('Redirect this page to another page in the system'), required=False)
    #images = forms.CharField(widget=MultipleFileWidget, required=False)
    class Meta:
        model = Page
        exclude = ()

    class Media:
        js = ('js/slugify.js',)

    def __init__(self, *args, **kwargs):
        from django.contrib.contenttypes.models import ContentType
        super(PageFormAdmin, self).__init__(*args, **kwargs)

        redirect_to = self.fields['redirect_to']
        self.obj = kwargs.get('instance', False)

        # Assign auto-slug from title to slug field
        self.fields['display_title'].widget.attrs['data-slug'] = 'slug'

        if cms_settings.CMS_PAGE_RELATED_PAGES:
            self.fields['related_pages'] = forms.ModelMultipleChoiceField(queryset=Page.objects.get_published_originals(), widget=forms.CheckboxSelectMultiple, required=False)
        
        # if self.instance:
        #     content_type = ContentType.objects.get_for_model(self.instance)
        #     object_pk = self.instance.id
        #     self.fields['images'].widget.attrs.update({'content_type':content_type.id, 'object_pk':object_pk})
        # else:
        #     self.fields['images'].widget.attrs.update({'content_type':False, 'object_pk':False})

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        pages = [page.slug for page in Page.objects.all()]

        if self.obj and slug in pages and slug != self.obj.slug and slug != '':
            raise forms.ValidationError(_('The unique page identifier must be unique')) 
        elif not self.obj and slug in pages and slug != '':
            raise forms.ValidationError(_('The unique page identifier must be unique')) 
        else:
            return slug

    def clean_home(self):
        home = self.cleaned_data['home']

        if home:
            err_message = _('There is already another page set as home. Only one home can exists.')
            # Check if other pages are already home excluded the current edited page
            if self.obj:
                if self.Meta.model.objects.filter(published_from=None, home=True).exclude(id=self.obj.id):
                    raise  forms.ValidationError(err_message) 
            # Check if other pages are already home excluded
            else:
                if self.Meta.model.objects.filter(published_from=None, home=True):
                    raise  forms.ValidationError(err_message) 
        return home


#################
# Images inline #
#################

# class ImageInlineForm(forms.ModelForm):
#     image = forms.ImageField(label=_('Image'), widget=AdminImageWidget)
#     class Meta:
#         model=PageImage

# class PageImageInline(admin.TabularInline):
#     form = ImageInlineForm
#     model = PageImage
#     extra = 0
    #template = 'admin/cmsbase/page/images-inline.html'

####################
# Documents inline #
####################

class DocumentInlineForm(forms.ModelForm):
    document = forms.FileField(label=_('Document'), widget=AdminCustomFileWidget)
    class Meta:
        model=PageDocument
        exclude = ()

class PageDocumentInline(admin.TabularInline):
    form = DocumentInlineForm
    model = PageDocument
    extra = 0
    template="admin/includes/fieldset-inline-tabular.html"

################
# Links inline #
################

class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 0
    #template = 'admin/cmsbase/page/images-inline.html'

##############
# Page admin #
##############

class PageAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin, MPTTModelAdmin):

    form = PageFormAdmin
    translation_form_class = TranslationForm

    if cms_settings.CMS_PAGE_DOCUMENTS:
        inlines += (PageDocumentInline,)

    if cms_settings.CMS_PAGE_LINKS:
        inlines += (PageLinkInline,)

    mptt_indent_field = 'title'

    mptt_level_indent = 20

    change_list_template = 'admin/cmsbase/page/change_list.html'


    # FIELDSETS

    fieldsets = (
        
        ('Settings', {
            'classes': ('default',),
            'fields': ('display_title', 'template', 'dataset',  'parent', 'slug', )
        }),
        ('Redirection', {
            'classes': ('default'),
            'fields': ('redirect_to', 'redirect_to_url', 'target',)
        }),
        ('Meta', {
            'classes': ('default'),
            'fields': ('home', 'hide_from_nav',  'order_id',)
        }),

    )

    # if cms_settings.CMS_PAGE_IMAGES:
    #     fieldsets += ('Images', {
    #         'classes': ('default',),
    #         'fields': ( 'images', )
    #     }),

    if cms_settings.CMS_PAGE_RELATED_PAGES:
        fieldsets = fieldsets + (('Related pages', {
            'classes': ('default',),
            'fields': ( 'related_pages',)
        }),)

    class Media:
        css = {
            "all": ("admin/css/page.css",)
        }
        js = ("admin/js/page.js",)


admin.site.register(Page, PageAdmin)


##############
# Page masks #
##############

class PageDataSetAdminForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'errorfield'
    initial = """[
  {
    "fieldset":"Page content",
    "fields":[
        {
            "name":"description",
            "type":"editorfield",
            "required":false
        }
    ]
  },
  {
    "fieldset":"Meta data",
    "fields":[
        {
            "name":"meta_title",
            "type":"charfield",
            "required":false
        },
        {
            "name":"meta_description",
            "type":"textfield",
            "required":false
        }
    ]
  }
]
"""
    config = forms.CharField(widget=CodeMirrorTextarea(mode="javascript", theme="cobalt", config={ 'fixedGutter': True, 'lineNumbers': True }), initial=initial)
    class Meta:
        model=PageDataSet
        exclude = ()

    def clean_config(self):

        config = self.cleaned_data['config']
        try:
            json.loads(config)
        except:
            raise forms.ValidationError(_('The JSON string is invalid'))


        ############################
        # TO-DO                    #
        # Validate all fields data #
        ############################


        return config

class PageDataSetAdmin(reversion.VersionAdmin):
    form = PageDataSetAdminForm


admin.site.register(PageDataSet, PageDataSetAdmin)


#################
# Page dynamics #
#################

# class PageDynamicAdmin(PageAdmin):
#     inlines = []


# admin.site.register(PageDynamic, PageDynamicAdmin)




