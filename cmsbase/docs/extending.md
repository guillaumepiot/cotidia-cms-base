Extending CMSBase
=================

To create new app that benefit from the same publishing workflow and multilingual support, you can extend the CMSBase models to inherit behaviour.

We will use the example of a blog as demonstration.

Models
------

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

		# Indicate which Translation class to use for content
		translation_class = ArticleTranslation

		class Meta:
			verbose_name=_('Article')
			verbose_name_plural=_('Articles')


Admin
-----

	from django.contrib import admin
	from django import forms
	from django.utils.translation import ugettext as _
	from django.conf import settings

	from multilingual_model.admin import TranslationInline

	from redactor.widgets import RedactorEditor

	from cmsbase.admin import PageAdmin, PageFormAdmin

	from blog.models import Article, ArticleTranslation


	# Translation

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
		class Meta:
			model = Article

	class ArticleAdmin(PageAdmin):
		form = ArticleAdminForm

		list_display = ["title", "is_published", "approval", 'template', 'languages']

		inlines = (ArticleTranslationInline, )

		fieldsets = (

			
			('Settings', {
				#'description':_('The page template'),
				'classes': ('default',),
				'fields': ('template', 'publish_date', 'slug', )
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