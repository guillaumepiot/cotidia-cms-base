import reversion

from django.contrib import admin, messages
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.conf import settings

from mptt.admin import MPTTModelAdmin
from mptt.forms import TreeNodeChoiceField

from multilingual_model.admin import TranslationInline

from redactor.widgets import RedactorEditor

from cmsbase.models import *
from cmsbase.widgets import AdminImageWidget, AdminCustomFileWidget


class PublishingWorkflowAdmin(admin.ModelAdmin):

	def get_fieldsets(self, request, obj=None):
		new_fieldset = []
		if request.user.has_perm('cms.can_publish') or request.user.is_superuser:
			for fieldset in self.fieldsets:
				if fieldset[0] != 'Approval':
					new_fieldset.append(fieldset)
			return new_fieldset
		else:
			for fieldset in self.fieldsets:
				if fieldset[0] != 'Publishing':
					new_fieldset.append(fieldset)
			return new_fieldset

	def get_list_display(self, request, obj=None):
		if not settings.PREFIX_DEFAULT_LOCALE:
			return ["title", "home_icon", "is_published", "approval", 'template']
		else:
			return ["title", "home_icon", "is_published", "approval", 'template', 'languages']



	def save_model(self, request, obj, form, change):
		if not obj.id and obj.parent:
			Page.tree.insert_node(obj, obj.parent)

		obj.save()

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
			if request.user.has_perm('cms.can_publish') or request.user.is_superuser:
				obj.unpublish_version()

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

	# Custom actions
	def make_published(modeladmin, request, queryset):
		if request.user.has_perm('cms.can_publish') or request.user.is_superuser:
			for obj in queryset:
				obj.approval_needed = False
				obj.published = True
				obj.save()
				obj.publish_version()
				obj.publish_translations()


	make_published.short_description = "Approve & Publish"

	def make_unpublished(modeladmin, request, queryset):
		if request.user.has_perm('cms.can_publish') or request.user.is_superuser:
			for obj in queryset:
				obj.published = False
				obj.save()
				obj.unpublish_version()
	make_unpublished.short_description = "Un-publish"

	#Assign those actions
	actions = [make_published, make_unpublished]



	def get_actions(self, request):
		actions = super(PublishingWorkflowAdmin, self).get_actions(request)
		if not request.user.has_perm('cms.can_publish') and not request.user.is_superuser:
			del actions['make_published']
			del actions['make_unpublished']
		return actions


	# Custom result list
	def home_icon(self, obj):
		if obj.home:
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
		if obj.has_published_version:
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
		translation = PageTranslation.objects.filter(parent=obj, language_code=settings.DEFAULT_LANGUAGE)
		if translation.count() > 0:
			return translation[0].title
		else:
			return _('No translation available for default language')


	def languages(self, obj):
		ts=[]
		for t in obj.get_translations():
			ts.append(u'<img src="/static/admin/img/flags/%s.png" alt="" rel="tooltip" data-title="%s">' % (t.language_code, t.__unicode__()))
		return ' '.join(ts)

	languages.allow_tags = True
	languages.short_description = 'Translations'

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
	extra = 0
	prepopulated_fields = {'slug': ('title',)}
	template = 'admin/cmsbase/cms_translation_inline.html'


	# if settings.PREFIX_DEFAULT_LOCALE:
	# 	fieldsets = (
	# 		('Content', {
	# 			'classes': ('default',),
	# 			'fields': ('language_code','title', 'slug', 'content' )
	# 		}),
	# 		('Meta data', {
	# 			'classes': ('default collapse',),
	# 			'fields': ('meta_title', 'meta_description', )
	# 		}),
	# 	)
	# else:
	# 	fieldsets = (
	# 		('Content', {
	# 			'classes': ('default',),
	# 			'fields': ('language_code','title', 'slug', 'content' )
	# 		}),
	# 		('Meta data', {
	# 			'classes': ('default collapse',),
	# 			'fields': ('meta_title', 'meta_description', )
	# 		}),
	# 	)


class PageFormAdmin(forms.ModelForm):
	redirect_to = TreeNodeChoiceField(queryset=Page.objects.get_published_original(), help_text=_('Redirect this page to another page in the system'), required=False)

	class Meta:
		model = Page

	def __init__(self, *args, **kwargs):
		super(PageFormAdmin, self).__init__(*args, **kwargs)

		redirect_to = self.fields['redirect_to']
		self.obj = kwargs.get('instance', False)
		

	def clean_slug(self):
		slug = self.cleaned_data['slug']

		pages = [page.slug for page in Page.objects.all()]


		if self.obj and slug in pages and slug != self.obj.slug and slug != '':
			raise forms.ValidationError(_('The unique page identifier must be unique')) 
		elif not self.obj and slug in pages and slug != '':
			raise forms.ValidationError(_('The unique page identifier must be unique')) 
		else:
			return slug



# class ImageInlineForm(forms.ModelForm):
# 	image = forms.ImageField(widget=AdminImageWidget)
# 	class Meta:
# 		model=PageImage

# class ListingImageInline(admin.TabularInline):
# 	form = ImageInlineForm
# 	model = PageImage
# 	extra = 0
# 	template = 'admin/cms/page/images-inline.html'

class PageAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin, MPTTModelAdmin):

	form = PageFormAdmin

	#list_display = ["title", "home_icon", "is_published", "approval", 'template', 'languages']
	#list_filter = ["approval_needed"]
	# search_fields = ['title']
	# prepopulated_fields = {'slug': ('title',)}
	inlines = (PageTranslationInline, ) #ListingImageInline

	mptt_indent_field = 'title'

	mptt_level_indent = 20



	# FIELDSETS

	fieldsets = (

		
		('Settings', {
			#'description':_('The page template'),
			'classes': ('default',),
			'fields': ( 'home', 'parent', 'template', 'redirect_to', 'slug', )
		}),

	)


admin.site.register(Page, PageAdmin)