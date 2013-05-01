Extending CMSBase
=================

To create new app that benefit from the same publishing workflow and multilingual support, you can extend the CMSBase models to inherit behaviour.

We will use the example of a blog as demonstration.

Models
------

	from django.db import models
	from django.utils.translation import ugettext as _

	from cmsbase.models import Page, PageTranslation


	# Subclass the Page model to create the article model

	class Article(Page):

		class Meta:
			verbose_name=_('Article')
			verbose_name_plural=_('Articles')


	# Subclass the PageTranslation model to create the article translation

	class ArticleTranslation(Page):

		def __init__(self, *args, **kwargs):
			super(self, ArticleTranslation).__init__(*args, **kwargs)
			# Parent has to be reassigned
			parent = models.ForeignKey('Article', related_name='translations')
			parent.contribute_to_class('parent', self)

		class Meta:
			verbose_name=_('Article content')
			verbose_name_plural=_('Article content')


Admin
-----

	from django.contrib import admin

	from cmsbase.admin import PageAdmin

	from blog.models import Article

	class ArticleAdmin(PageAdmin):
		pass

	admin.site.register(Article, ArticleAdmin)
	
Admin template
--------------

Copy the cmsbase admin templates and rename the folder with the same name as the app you created.

Eg:

	admin/
		blog/
			article/
				change_form.html