import reversion

from django.contrib import admin, messages
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect

from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField

from multilingual_model.admin import TranslationInline

from redactor.widgets import RedactorEditor

from cmsbase.models import *
from cmsbase.widgets import AdminImageWidget, AdminCustomFileWidget
from cmsbase import settings as cms_settings


class PublishingWorkflowAdmin(admin.ModelAdmin):

	# def get_fieldsets(self, request, obj=None):
	# 	new_fieldset = []
	# 	if request.user.has_perm('cmsbase.can_publish') or request.user.is_superuser:
	# 		for fieldset in self.fieldsets:
	# 			if fieldset[0] != 'Approval':
	# 				new_fieldset.append(fieldset)
	# 	else:
	# 		for fieldset in self.fieldsets:
	# 			if fieldset[0] != 'Publishing':
	# 				new_fieldset.append(fieldset)

	# 	return new_fieldset

	# def __init__(self, *args, **kwargs):
	# 	print kwargs
	# 	request = kwargs['request']
	# 	# Make the slug field read-only for non-superuser and non-publishers
	# 	if not request.user.has_perm('cmsbase.can_publish') and not request.user.is_superuser:
	# 		self.base_fields['slug'].widget.attrs['readonly'] = True
	# 	super(PublishingWorkflowAdmin, self).__init__(*args, **kwargs)

	def get_list_display(self, request, obj=None):
		if not settings.PREFIX_DEFAULT_LOCALE:
			return ['title', 'home_icon', 'is_published', 'approval', 'order_id', 'template', 'preview']
		else:
			return ['title', 'home_icon', 'is_published', 'approval', 'order_id', 'template', 'languages', 'preview']



	def save_model(self, request, obj, form, change):
		if not obj.id and obj.parent:
			obj.__class__.tree.insert_node(obj, obj.parent)


		obj.save()

		# Rebuild the tree
		obj.__class__.tree.rebuild()

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
			return HttpResponseRedirect("%s?preview" % obj.get_absolute_url())
		elif "_publish" in request.POST:
			self._publish_object(obj)
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
				self._publish_object(obj)

			# Rebuild the tree
			obj.__class__.tree.rebuild()

	make_published.short_description = "Approve & Publish"

	def make_unpublished(self, request, queryset):
		if request.user.has_perm('cmsbase.can_publish') or request.user.is_superuser:
			for obj in queryset:
				obj.published = False
				obj.save()
				obj.unpublish_version()

			# Rebuild the tree
			obj.__class__.tree.rebuild()

	make_unpublished.short_description = "Un-publish"

	#Assign those actions
	actions = [make_published, make_unpublished]



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
			return '<i class="icon-home"></i>'
		else:
			return ''
	home_icon.allow_tags = True
	home_icon.short_description = 'Home'

	def approval(self, obj):
		if obj.approval_needed:
			return '<i class="icon-time"></i>'
		else:
			return '<i class="icon-ok"></i>'
	approval.allow_tags = True
	approval.short_description = 'Approved'

	def is_published(self, obj):
		if obj.published:
			return '<i class="icon-ok"></i>'
		else:
			return '<i class="icon-minus-sign"></i>'
	is_published.allow_tags = True
	is_published.short_description = 'Published'

	def is_active(self, obj):
		if obj.published:
			return '<i class="icon-ok"></i>'
		else:
			return '<i class="icon-minus-sign"></i>'
	is_active.allow_tags = True
	is_active.short_description = 'Active'

	def title(self, obj):
		translation = obj.translated() #PageTranslation.objects.filter(parent=obj, language_code=settings.DEFAULT_LANGUAGE)
		if translation:
			return translation.title
		else:
			return _('No translation available for default language')


	def languages(self, obj):
		available_ts = {}
		ts=[]
		for t in obj.get_translations():
			available_ts[t.language_code] = u'<img src="/static/admin/img/flags/%s.png" alt="" rel="tooltip" data-title="%s">' % (t.language_code, t.__unicode__())
		for language in settings.LANGUAGES:
			if available_ts.get(language[0], False):
				ts.append(available_ts[language[0]])
		return ' '.join(ts)

	languages.allow_tags = True
	languages.short_description = 'Translations'

	def preview(self, obj):
		return '<a href="%s?preview" target="_blank">%s</a>' % (obj.get_absolute_url(), _('Preview'))
	preview.allow_tags = True

class PageTranslationInlineFormAdmin(forms.ModelForm):
	slug = forms.SlugField(label=_('Page URL'))
	content = forms.CharField(widget=RedactorEditor(redactor_css="/static/css/redactor-editor.css"), required=False)

	class Meta:
		model = PageTranslation

	def has_changed(self):
		""" Should returns True if data differs from initial.
		By always returning true even unchanged inlines will get validated and saved."""
		return True

class PageTranslationInline(TranslationInline):
	model = PageTranslation
	form = PageTranslationInlineFormAdmin
	extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
	prepopulated_fields = {'slug': ('title',)}
	template = 'admin/cmsbase/cms_translation_inline.html'



class PageFormAdmin(forms.ModelForm):
	redirect_to = TreeNodeChoiceField(label=_('Redirect to page'), queryset=Page.objects.get_published_original(), help_text=_('Redirect this page to another page in the system'), required=False)

	class Meta:
		model = Page

	def __init__(self, *args, **kwargs):
		super(PageFormAdmin, self).__init__(*args, **kwargs)

		redirect_to = self.fields['redirect_to']
		self.obj = kwargs.get('instance', False)

		if cms_settings.CMS_PAGE_RELATED_PAGES:
			self.fields['related_pages'] = forms.ModelMultipleChoiceField(queryset=Page.objects.get_published_original(), widget=forms.CheckboxSelectMultiple, required=False)
		

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

class ImageInlineForm(forms.ModelForm):
	image = forms.ImageField(label=_('Image'), widget=AdminImageWidget)
	class Meta:
		model=PageImage

class PageImageInline(admin.TabularInline):
	form = ImageInlineForm
	model = PageImage
	extra = 0
	template = 'admin/cmsbase/page/images-inline.html'

####################
# Documents inline #
####################

class DocumentInlineForm(forms.ModelForm):
	document = forms.FileField(label=_('Document'), widget=AdminCustomFileWidget)
	class Meta:
		model=PageDocument

class PageDocumentInline(admin.TabularInline):
	form = DocumentInlineForm
	model = PageDocument
	extra = 0
	template = 'admin/cmsbase/page/images-inline.html'

################
# Links inline #
################

class PageLinkInline(admin.TabularInline):
	model = PageLink
	extra = 0
	template = 'admin/cmsbase/page/images-inline.html'

##############
# Page admin #
##############

class PageAdmin(PublishingWorkflowAdmin, MPTTModelAdmin, reversion.VersionAdmin):

	form = PageFormAdmin

	inlines = (PageTranslationInline, )

	if cms_settings.CMS_PAGE_IMAGES:
		inlines += (PageImageInline,)

	if cms_settings.CMS_PAGE_DOCUMENTS:
		inlines += (PageDocumentInline,)

	if cms_settings.CMS_PAGE_LINKS:
		inlines += (PageLinkInline,)

	mptt_indent_field = 'title'

	mptt_level_indent = 20


	# FIELDSETS

	fieldsets = (
		
		('Settings', {
			'classes': ('default',),
			'fields': ( 'home', 'hide_from_nav', 'parent', 'template', 'redirect_to', 'redirect_to_url', 'target', 'slug', 'order_id' )
		}),

	)

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