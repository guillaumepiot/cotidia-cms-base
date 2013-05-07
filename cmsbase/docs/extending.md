Extending CMSBase
=================

To create new app that benefit from the same publishing workflow and multilingual support, you can extend the CMSBase models to inherit behaviour.

We will use the example of a blog as demonstration.

Models
------

When extending the CMSBase model structure, you will need to create a new model class that inherit from `BasePage`.

You will need to supply some extra meta variables using the CMSMeta class:

	class CMSMeta:
	
		# A tuple of templates paths and names
		templates = blog_settings.BLOG_TEMPLATES
		
		# Indicate which Translation class to use for content
		translation_class = ArticleTranslation
		
		# Provide the url name to create a url for that model
		model_url_name = 'blog:article'


Here's an example of a model extension for the blog app:


	from django.db import models
	from django.utils.translation import ugettext as _
	from django.conf import settings

	from multilingual_model.models import MultilingualModel, MultilingualTranslation
	from cmsbase.models import BasePage, PublishTranslation




	# Subclass the PageTranslation model to create the article translation

	class ArticleTranslation(MultilingualTranslation, PublishTranslation):
		parent = models.ForeignKey('Article', related_name='translations')
		title = models.CharField(_('Article title'), max_length=100)
		slug = models.SlugField(max_length=60)
		content = models.TextField(blank=True)

		#Meta data
		meta_title = models.CharField(max_length=100, blank=True)
		meta_description = models.TextField(blank=True)

		class Meta:
			unique_together = ('parent', 'language_code')

			if len(settings.LANGUAGES) > 1:
				verbose_name=_('Translation')
				verbose_name_plural=_('Translations')
			else:
				verbose_name=_('Content')
				verbose_name_plural=_('Content')

		def __unicode__(self):
			return dict(settings.LANGUAGES).get(self.language_code)


	class ArticleManager(models.Manager):

	    def get_published_live(self):
	        return Article.objects.filter(published=True).exclude(published_from=None)

	    def get_published_original(self):
	        return Article.objects.filter(published=True, published_from=None)

	    def get_originals(self):
	        return Article.objects.filter(published_from=None)

	# Subclass the Page model to create the article model

	class Article(BasePage):
		# Extra fields
		publish_date = models.DateTimeField()

		# Manager
		objects = ArticleManager()

		

		class Meta:
			verbose_name=_('Article')
			verbose_name_plural=_('Articles')
	
		class CMSMeta:
		
			# A tuple of templates paths and names
			templates = blog_settings.BLOG_TEMPLATES
			
			# Indicate which Translation class to use for content
			translation_class = ArticleTranslation
			
			# Provide the url name to create a url for that model
			model_url_name = 'blog:article'


Admin
-----

	import reversion

	from django.contrib import admin
	from django import forms
	from django.utils.translation import ugettext as _
	from django.conf import settings
	from django.contrib.admin.views.main import ChangeList

	from mptt.admin import MPTTModelAdmin
	from multilingual_model.admin import TranslationInline

	from redactor.widgets import RedactorEditor

	from cmsbase.admin import PageAdmin, PageFormAdmin, PublishingWorkflowAdmin

	from blog.models import *


	# Article translation

	class ArticleTranslationInlineFormAdmin(forms.ModelForm):
		slug = forms.SlugField(label=_('Article URL'))
		content = forms.CharField(widget=RedactorEditor(redactor_css="/static/css/redactor-editor.css"), required=False)

		class Meta:
			model = ArticleTranslation

		def has_changed(self):
			""" Should returns True if data differs from initial.
			By always returning true even unchanged inlines will get validated and saved."""
			return True

	class ArticleTranslationInline(TranslationInline):
		model = ArticleTranslation
		form = ArticleTranslationInlineFormAdmin
		extra = 0 if settings.PREFIX_DEFAULT_LOCALE else 1
		prepopulated_fields = {'slug': ('title',)}
		template = 'admin/cmsbase/cms_translation_inline.html'



	# Article


	class ArticleAdminForm(PageFormAdmin):
		categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), widget=forms.CheckboxSelectMultiple)
		class Meta:
			model = Article



	class ArticleAdmin(reversion.VersionAdmin, PublishingWorkflowAdmin):
		form = ArticleAdminForm
		
		inlines = (ArticleTranslationInline, )
		ordering = ['-publish_date'] 

		# Override the list display from PublishingWorkflowAdmin
		def get_list_display(self, request, obj=None):
			if not settings.PREFIX_DEFAULT_LOCALE:
				return ['title', 'is_published', 'approval', 'publish_date', 'template']
			else:
				return ['title', 'is_published', 'approval', 'publish_date', 'template', 'languages']

		fieldsets = (

			
			('Settings', {
				#'description':_('The page template'),
				'classes': ('default',),
				'fields': ('template', 'publish_date', 'slug', 'categories')
			}),

		)

	admin.site.register(Article, ArticleAdmin)
	
Admin template
--------------

Copy the cmsbase admin templates and rename the folder with the same name as the app you created.

Eg:

	admin/
		blog/
			article/
				change_form.html
				
				
Views
-----

You can extend the views from CMSBase by using the `@page_processor` decorator.

`@page_processor(model_class, translation_class)` will do the fundamental following actions:

- Check whether the page is in preview mode or not
- Retrieve the model entry based on the `slug` and the `model_class` & `translation_class`
- Return a 404 error if the model entry can't be retrieved
- Redirect the page to another if set this way in the database using the `redirect_to` attribute
- Redirect to the right translated slug in the case of a language switch

The `@page_processor` decorator takes 2 arguments:
	- model_class: the model class for the main model
	- translation_class: the model translation class corresponsing the main model
	
By default, the arguments are set as `Page` and  `PageTranslation`:

	def page_processor(model_class=Page, translation_class=PageTranslation):
		...
		
The `@page_processor` will pass 3 arguments to the function it is annotated from:

- `request`: the Django request object
- `page`: the model entry instance
- `slug`: the current page slug

Example extension for the blog app:

	...
	from cmsbase.views import page_processor

	from blog.models import Article, ArticleTranslation

	@page_processor(model_class=Article, translation_class=ArticleTranslation)
	def article(request, page, slug):
		return render_to_response(page.template, {'page':page,}, context_instance=RequestContext(request))

