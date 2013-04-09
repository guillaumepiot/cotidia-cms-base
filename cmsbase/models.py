import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse
from localeurl.models import reverse
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType

PAGE_TEMPLATES = (
	('cms/page.html', 'Default page'),
)

from multilingual_model.models import MultilingualModel, MultilingualTranslation

class CMSManager(models.Manager):

    def get_published_live(self):
        return Page.objects.filter(published=True).exclude(published_from=None)

    def get_published_original(self):
        return Page.objects.filter(published=True, published_from=None)

    def get_originals(self):
        return Page.objects.filter(published_from=None)

class Page(MPTTModel, MultilingualModel):
	home = models.BooleanField(blank=True)
	published = models.BooleanField(_('Active'))
	approval_needed = models.BooleanField()
	template = models.CharField(max_length=250, choices=PAGE_TEMPLATES)

	#MPTT parent
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

	# Publish version key
	published_from = models.ForeignKey('self', blank=True, null=True)

	# title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=60,  verbose_name="Unique Page Identifier")

	#content = models.TextField(blank=True)

	#Meta data
	meta_title = models.CharField(max_length=100, blank=True)
	meta_keywords = models.CharField(max_length=100, blank=True)
	meta_description = models.TextField(blank=True)

	# Ordering
	order_id = models.IntegerField(blank=True, null=True)

	# Publishing
	publish = models.BooleanField(_('Publish this page. The page will also be set to Active.'))
	approve = models.BooleanField(_('Submit for approval'))

	date_created = models.DateTimeField()
	date_updated = models.DateTimeField()

	# Optional redirect
	redirect_to = models.ForeignKey('self', blank=True, null=True, related_name='redirect_to_page')

	objects = CMSManager()

	def get_content_type(self):
		content_type = ContentType.objects.get_for_model(Page)
		return content_type

	def __unicode__(self):
		return self.unicode_wrapper('title', default='Unnamed')

	def save(self, *args, **kwargs):
		if not self.date_created:
			self.date_created = datetime.datetime.now()

		self.date_updated = datetime.datetime.now()

		super(Page, self).save(*args, **kwargs)

	class Meta:
		#ordering = ()
		verbose_name = _('page')
		verbose_name_plural = _('pages')
		permissions = (
			("can_publish", "Can publish"),
		)

	class MPTTMeta:
		order_insertion_by = ['order_id']

	def get_published(self):
		published = Page.objects.filter(published_from=self)
		if published.count() > 0:
			return published[0]
		else:
			return None

	def translated(self):
		from django.utils.translation import get_language
		try:
			translation = PageTranslation.objects.get(language_code=get_language(), parent=self)
			return translation
		except:
			return PageTranslation.objects.get(language_code=settings.LANGUAGE_CODE, parent=self)

	def get_translations(self):
		return PageTranslation.objects.filter(parent=self)

	def publish_translations(self):
		# Get translations
		for translation in PageTranslation.objects.filter(parent=self):
			translation.publish_version()

	# Publish method
	# Create a clone of the current page state or update the current clone

	def publish_version(self):

		# Check if the page exist already
		try:
			page = Page.objects.get(published_from=self)
		except:
			page = Page()

		# Update data
		page.home = self.home
		page.published = self.published
		page.template = self.template
		page.parent = None
		page.published_from = self

		# page.title = self.title
		page.slug = self.slug
		#page.content = self.content
		page.meta_title = self.meta_title
		page.meta_keywords = self.meta_keywords
		page.meta_description = self.meta_description
		page.order_id = 0
		page.redirect_to = self.redirect_to
		page.save()

		return page

	def unpublish_version(self):

		# Check if the page exist already
		try:
			page = Page.objects.get(published_from=self)
		except:
			page = None

		if page:
			# Update data
			page.published = False
			page.save()

		return page

	def delete(self):

		published_version = Page.objects.filter(published_from=self)
		for version in published_version:
			version.delete()
		super(Page, self).delete()


	def get_absolute_url(self):

		from django.utils import translation

		current_language = translation.get_language()


		if self.home:
			url = reverse('home')
		else:
			# if self.parent:
			# 	slug = "%s/%s" % (self.parent.slug, self.slug)

			# set the default language to the current language
			slug = ''

			# If is original
			if self.get_published():
				for ancestor in self.get_ancestors():
					translation = PageTranslation.objects.filter(parent=ancestor.get_published().id, language_code=current_language)
					if translation.count()>0:

						slug = "%s%s/" % (slug, translation[0].slug)
					else:
						slug = slug + '%s/' % (ancestor.get_published().slug)

				translation = PageTranslation.objects.filter(parent=self.get_published().id, language_code=current_language)

				if translation.count()>0:
					slug = "%s%s" % (slug, translation[0].slug)

				else:
					slug = "%s%s" % (slug, self.get_published().slug)
			# Else if it is the published version
			else:
				if self.published_from != None:
					for ancestor in self.published_from.get_ancestors():
						slug = slug + '%s/' % (ancestor.get_published().slug)
					slug = "%s%s" % (slug, self.slug)
				else:
					slug = "%s%s" % (slug, self.slug)
			url = reverse('cms:page', kwargs={'slug':slug})

		return url

	def get_breadcrumbs(self):
		if self.home:
			breadcrumbs = []
		else:
			# if self.parent:
			# 	slug = "%s/%s" % (self.parent.slug, self.slug)
			breadcrumbs = []

			# If is original
			if self.get_published():
				for ancestor in self.get_ancestors():
					breadcrumbs.append(ancestor.get_published().translated().title)
			# Else if it is the published version
			else:
				# if self.published_from != None:
				for ancestor in self.published_from.get_ancestors():
					breadcrumbs.append(ancestor.get_published().translated().title)
		return breadcrumbs

	@property
	def has_published_version(self):
		try:
			page = Page.objects.get(published_from=self, published=True)
			return True
		except:
			return False

	# def images(self):
	# 	if self.published_from:
	# 		images = PageImage.objects.filter(page=self.published_from).order_by('order_id')
	# 	else:
	# 		images = PageImage.objects.filter(page=self).order_by('order_id')
	# 	return images

	# def feature_image(self):
	# 	images = self.images()
	# 	#print images
	# 	if images.count() > 0:
	# 		return images[0].image
	# 	else:
	# 		return False

	def get_default_url(self, slug=False):

		from django.utils import translation

		current_language = translation.get_language()

		if slug:
			slugs = slug.split('/')

			new_slug = []

			for s in slugs:
				pages = PageTranslation.objects.filter(slug=s)

				for p in pages:
					if p.parent.published_from == None:
						uri_page = p.parent

						page = PageTranslation.objects.filter(language_code=current_language, parent=uri_page)

						uri = uri_page.slug

						if page.count() > 0:
							uri = page[0].slug


						new_slug.append(uri)

				# translation = PageTranslation.objects.filter(language_code=current_language)

				# for t in translation:
				# 	print t.slug, t.id
				# if translation.count() > 0:

					# uri = translation[0].slug

				# new_slug.append(uri)

		str = '/'
		print str.join(new_slug)
		return str.join(new_slug)

class PageTranslation(MultilingualTranslation):
	parent = models.ForeignKey('Page', related_name='translations')
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=60)
	content = models.TextField(blank=True)

	#Meta data
	meta_title = models.CharField(max_length=100, blank=True)
	meta_keywords = models.CharField(max_length=100, blank=True)
	meta_description = models.TextField(blank=True)

	class Meta:
		unique_together = ('parent', 'language_code')

	def __unicode__(self):
		return dict(settings.LANGUAGES).get(self.language_code)

	def save(self):

		published_page = Page.objects.filter(published_from=self.parent)

		#print "Saving related"

		try:
			if self.parent.publish_inlines:
				self.publish_version()
		except:
			pass




		super(PageTranslation, self).save()

	def publish_version(self):

		published_page = Page.objects.filter(published_from=self.parent)
		if len(published_page)>0:
			published_page = published_page[0]
			try:
				new_translation = PageTranslation.objects.get(language_code=self.language_code, parent=published_page)
			except:
				new_translation = PageTranslation()


			new_translation.parent = published_page
			new_translation.language_code = self.language_code
			new_translation.title = self.title
			new_translation.slug = self.slug
			new_translation.content = self.content

			#Meta data
			new_translation.meta_title = self.meta_title
			new_translation.meta_keywords = self.meta_keywords
			new_translation.meta_description = self.meta_description

			new_translation.save()

# class PageImage(models.Model):

# 	def call_naming(self, instance=None):
# 		from cms.widgets import get_media_upload_to

# 		# return get_media_upload_to(self.page.slug, 'pages')
# 		location = "cms/%s"%(self.page.slug)
# 		return get_media_upload_to(location, instance)

# 	page = models.ForeignKey(Page)
# 	image = models.ImageField(upload_to=call_naming, max_length=100)
# 	# Ordering
# 	order_id = models.IntegerField(blank=True, null=True)

# 	class Meta:
# 		ordering = ('order_id',)
# 		verbose_name = _('Image')
# 		verbose_name_plural = _('Images')

# 	def delete(self, *args, **kwargs):
# 		from sorl.thumbnail import get_thumbnail
# 		storage, path = self.image.storage, self.image.path
# 		super(PageImage, self).delete(*args, **kwargs)
# 		# Physically delete the file
# 		storage.delete(path)
