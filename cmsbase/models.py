import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.core.urlresolvers import reverse
from localeurl.models import reverse
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.models import ContentType

PAGE_TEMPLATES = (
	('cmsbase/page.html', 'Default page'),
)

from multilingual_model.models import MultilingualModel, MultilingualTranslation


class BasePage(MPTTModel, MultilingualModel):
	home = models.BooleanField(blank=True)
	published = models.BooleanField(_('Active'))
	approval_needed = models.BooleanField()
	template = models.CharField(max_length=250, choices=PAGE_TEMPLATES, default='cms/page.html')

	#MPTT parent
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

	# Publish version key
	published_from = models.ForeignKey('self', blank=True, null=True)

	# A unique identifier
	slug = models.SlugField(max_length=60,  verbose_name="Unique Page Identifier", blank=True, null=True)

	# Ordering
	order_id = models.IntegerField(blank=True, null=True)

	# Publishing
	publish = models.BooleanField(_('Publish this page. The page will also be set to Active.'))
	approve = models.BooleanField(_('Submit for approval'))

	date_created = models.DateTimeField()
	date_updated = models.DateTimeField()

	# Optional redirect
	redirect_to = models.ForeignKey('self', blank=True, null=True, related_name='redirect_to_page')

	def get_content_type(self):
		content_type = ContentType.objects.get_for_model(self.__class__)
		return content_type

	def __unicode__(self):
		return self.unicode_wrapper('title', default='Unnamed')

	def save(self, *args, **kwargs):

		if not self.date_created:
			self.date_created = datetime.datetime.now()

		self.date_updated = datetime.datetime.now()

		super(BasePage, self).save(*args, **kwargs)

	class Meta:
		#ordering = ()
		permissions = (
			("can_publish", "Can publish"),
		)

		# Make this class a reference only with no database, all models must be subclass from this
		abstract = True

	# class MPTTMeta:
	# 	order_insertion_by = ['order_id']

	def get_published(self):
		cls = self.__class__
		published = cls.objects.filter(published_from=self)
		if published.count() > 0:
			return published[0]
		else:
			return None

	def translated(self):
		from django.utils.translation import get_language

		try:
			translation = self.translation_class.objects.get(language_code=get_language(), parent=self)
			return translation
		except:
			return self.translation_class.objects.get(language_code=settings.LANGUAGE_CODE, parent=self)

	def get_translations(self):
		return self.translation_class.objects.filter(parent=self)

	def publish_translations(self):
		# Get translations
		for translation in self.translation_class.objects.filter(parent=self):
			translation.publish_version()

	# Publish method
	# Create a clone of the current page state or update the current clone

	def publish_version(self):

		cls = self.__class__

		# Fields to ignore in duplication
		ignore_fields = ['id', 'approval_needed', 'parent_id', 'published_from_id', 'order_id', 'publish', 'approve', 'lft', 'rght', 'tree_id', 'level', 'page_ptr_id']

		# Check if the page exist already
		try:
			obj = cls.objects.get(published_from=self)
		except:
			obj = cls()

		# Update fields which are not ignored
		for field in cls._meta.fields:
			#print dir(field)
			if field.attname not in ignore_fields:
				obj.__dict__[field.attname] = self.__dict__[field.attname]

		# Override fields that are part of the publishing process
		obj.parent = None
		obj.published_from = self
		obj.order_id = 0
		
		obj.save()

		return obj

	def unpublish_version(self):

		cls = self.__class__

		# Check if the page exist already
		try:
			obj = cls.objects.get(published_from=self)
		except:
			obj = None

		if obj:
			# Update data
			obj.published = False
			obj.save()

		return obj

	def delete(self):

		published_version = Page.objects.filter(published_from=self)
		for version in published_version:
			version.delete()
		super(Page, self).delete()


	def get_absolute_url(self):
		from django.utils import translation
		current_language = translation.get_language()

		if self.home:
			url = reverse('cms:home')
		else:
			slug = ''

			# Get ancestor from original
			if self.get_published():
				ancestors = self.get_ancestors()
			elif self.published_from:
				ancestors = self.published_from.get_ancestors()
			else:
				ancestors = []

			# Go through the ancestor to get slugs
			for ancestor in ancestors:
				# Get the ancestor's slugs
				translation = self.translation_class.objects.filter(parent=ancestor.id, language_code=current_language)

				# If no translation available in the current language
				if not translation.count()>0:
					translation = self.translation_class.objects.get(parent=ancestor.id, language_code=settings.DEFAULT_LANGUAGE)
				else:
					translation = translation[0]
				
				# Only add slug if the ansector is not home
				if not ancestor.home:
					slug = "%s%s/" % (slug, translation.slug)

			translation = self.translation_class.objects.filter(parent=self.id, language_code=current_language)
			
			if not translation.count()>0:
				translation = self.translation_class.objects.get(parent=self.id, language_code=settings.DEFAULT_LANGUAGE)
			else:
				translation = translation[0]

			slug = "%s%s" % (slug, translation.slug)

			# Create the full url based on the pattern
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
			page = self.__class__.objects.get(published_from=self, published=True)
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
				pages = self.translation_class.objects.filter(slug=s)

				for p in pages:
					if p.parent.published_from == None:
						uri_page = p.parent

						page = self.translation_class.objects.filter(language_code=current_language, parent=uri_page)

						uri = uri_page.slug

						if page.count() > 0:
							uri = page[0].slug


						new_slug.append(uri)

				# translation = self.translation_class.objects.filter(language_code=current_language)

				# for t in translation:
				# 	print t.slug, t.id
				# if translation.count() > 0:

					# uri = translation[0].slug

				# new_slug.append(uri)

		str = '/'

		return str.join(new_slug)


# Handle the publisinh workflow of a translation model
class PublishTranslation(object):

	def save(self):

		published_page = self.parent.__class__.objects.filter(published_from=self.parent)

		try:
			if self.parent.publish_inlines:
				self.publish_version()
		except:
			pass

		super(PageTranslation, self).save()

	def publish_version(self):

		parent_cls = self.parent.__class__
		cls = self.__class__

		# Fields to ignore in duplication
		ignore_fields = ['id', 'parent_id', ]


		published_page = parent_cls.objects.filter(published_from=self.parent)
		if len(published_page)>0:
			published_page = published_page[0]
			try:
				obj = cls.objects.get(language_code=self.language_code, parent=published_page)
			except:
				obj = cls()

			# Update fields which are not ignored
			for field in cls._meta.fields:
				if field.attname not in ignore_fields:
					obj.__dict__[field.attname] = self.__dict__[field.attname]


			obj.parent = published_page

			obj.save()




	



# Create the working models


# And the translation model

class PageTranslation(MultilingualTranslation, PublishTranslation):
	parent = models.ForeignKey('Page', related_name='translations')
	title = models.CharField(_('Page title'), max_length=100)
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


class PageManager(models.Manager):

    def get_published_live(self):
        return Page.objects.filter(published=True).exclude(published_from=None)

    def get_published_original(self):
        return Page.objects.filter(published=True, published_from=None)

    def get_originals(self):
        return Page.objects.filter(published_from=None)

class Page(BasePage):

	objects = PageManager()

	# Indicate which Translation class to use for content
	translation_class = PageTranslation

	class Meta:
		verbose_name=_('Page')
		verbose_name_plural=_('Pages')

		




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
