import datetime, json, reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey
from cmsbase import settings as cms_settings
from multilingual_model.models import MultilingualModel, MultilingualTranslation
from filemanager.models import FileToObject

TARGET_CHOICES = (
    ('_self', 'the same window'),
    ('_blank', 'a new window'),
)

class BasePageManager(models.Manager):

    def get_published_live(self):
        return self.model.objects.filter(published=True).exclude(published_from=None)

    def get_published_original(self):
        return self.model.objects.filter(published=True, published_from=None)

    def get_originals(self):
        return self.model.objects.filter(published_from=None)


class BasePage(MPTTModel):
    home = models.BooleanField(default=False)
    published = models.BooleanField(_('Active'), default=False)
    approval_needed = models.BooleanField(default=False)
    template = models.CharField(max_length=250, choices=[], default='cms/page.html')

    #Display title
    display_title = models.CharField(max_length=250,  verbose_name="Display title")

    #MPTT parent
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # Publish version key
    published_from = models.ForeignKey('self', blank=True, null=True)

    #Page mask
    mask = models.ForeignKey('PageMask', blank=True, null=True)

    # A unique identifier
    slug = models.SlugField(max_length=60,  verbose_name="Unique Page Identifier", blank=True, null=True)

    # Ordering
    order_id = models.IntegerField(default=0)

    # Publishing
    publish = models.BooleanField(_('Publish this page. The page will also be set to Active.'), default=False)
    approve = models.BooleanField(_('Submit for approval'), default=False)

    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()

    # Optional redirect
    redirect_to = models.ForeignKey('self', blank=True, null=True, related_name='redirect_to_page')
    redirect_to_url = models.URLField(_('Redirect to URL'), blank=True, help_text=_('Redirect this page to a given URL'))
    target = models.CharField(_('Open page in'), max_length=50, choices=TARGET_CHOICES, default='_self')
    
    # Navigation
    hide_from_nav = models.BooleanField(_('Hide from navigation'), default=False)

    # Related pages / can be used for reading more about the same subject
    related_pages = models.ManyToManyField('self', blank=True)

    objects = BasePageManager()

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

    # def __init__(self, *args, **kwargs):
    #   # Set the templates choices base on the CMSMeta templates
    #   self._meta.get_field_by_name('template')[0]._choices = self.CMSMeta.templates
    #   print 'test'

    #   super(BasePage, self).__init__(*args, **kwargs)

    class Meta:
        # Make this class a reference only with no database, all models must be subclass from this
        abstract = True

    class MPTTMeta:
        #level_attr = 'mptt_level'
        order_insertion_by=['order_id']

    class CMSMeta:
        templates = cms_settings.CMS_PAGE_TEMPLATES
        # Must be provided on model extension
        #translation_class = PageTranslation
        model_url_name = 'cms:page'


    def unicode_wrapper(self, property, default=ugettext('Untitled')):
        """
        Wrapper to allow for easy unicode representation of an object by
        the specified property. If this wrapper is not able to find the
        right translation of the specified property, it will return the
        default value instead.

        Example::
            def __unicode__(self):
                return unicode_wrapper('name', default='Unnamed')

        """
        # TODO: Test coverage!
        try:
            value = getattr(self, property)
        except ValueError:
            logger.warn(
                u'ValueError rendering unicode for %s object.',
                self._meta.object_name
            )

            value = None

        if not value:
            value = default

        return value

    @property
    def title(self):
        return self.display_title

    # class MPTTMeta:
    #   order_insertion_by = ['order_id']

    def get_published(self):
        cls = self.__class__
        published = cls.objects.filter(published_from=self)
        if published.count() > 0:
            return published[0]
        else:
            return None

    def set_dynamic_attributes(self, obj):
        dynamic_attrs = []
        # Go through each fieldset
        for fieldset in self.mask.get_fields():
            fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
            for field in fieldset['fields']:

                # Get the name of the field
                field_name = '%s_%s' % (fieldset_id, field['name'])
                # print field_name
                setattr(obj, field_name, obj.get_attr(field_name))
        return obj

    def translated(self):
        from django.utils.translation import get_language

        try:
            translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self)
        except:
            translation = self.CMSMeta.translation_class.objects.get(language_code=settings.LANGUAGE_CODE, parent=self)

        translation = self.set_dynamic_attributes(translation)
        return translation

    def get_translations(self):
        return self.CMSMeta.translation_class.objects.filter(parent=self)

    def publish_translations(self):
        # Get translations
        for translation in self.CMSMeta.translation_class.objects.filter(parent=self):
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


    def get_absolute_url(self, current_language=False, urlargs=False):

        from django.utils import translation
        if not current_language:
            current_language = translation.get_language()

        if cms_settings.CMS_PREFIX and cms_settings.CMS_PREFIX.get(current_language, False):
            CMS_PREFIX = cms_settings.CMS_PREFIX[current_language]
        else:
            CMS_PREFIX = False


        if CMS_PREFIX and not CMS_PREFIX[len(CMS_PREFIX)-1] == '/':
            CMS_PREFIX = CMS_PREFIX + '/'

        if self.home:
            url = reverse('cms:home')
            if CMS_PREFIX:
                url = reverse('cms:home', prefix=CMS_PREFIX)
            else:
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
                translation = self.CMSMeta.translation_class.objects.filter(parent=ancestor.id, language_code=current_language)

                # If no translation available in the current language
                if not translation.count()>0:
                    translation = self.CMSMeta.translation_class.objects.get(parent=ancestor.id, language_code=settings.DEFAULT_LANGUAGE)
                else:
                    translation = translation[0]
                
                # Only add slug if the ansector is not home
                if not ancestor.home:
                    slug = "%s%s/" % (slug, translation.slug)

            translation = self.CMSMeta.translation_class.objects.filter(parent=self.id, language_code=current_language)
            
            if not translation.count()>0:
                translation = self.CMSMeta.translation_class.objects.get(parent=self.id, language_code=settings.DEFAULT_LANGUAGE)
            else:
                translation = translation[0]

            slug = "%s%s" % (slug, translation.slug)

            # Add extra prefixes if required
            default_args = {'slug':slug}
            if urlargs:
                reverse_args = dict(default_args.items() + urlargs.items())
            else:
                reverse_args = default_args

            # Create the full url based on the pattern
            if CMS_PREFIX:

                url = reverse(self.CMSMeta.model_url_name, kwargs=reverse_args, prefix=CMS_PREFIX)
            else:
                url = reverse(self.CMSMeta.model_url_name, kwargs=reverse_args)


        # Add prefix if required. Not compatible with localeurl redirect
        # if cms_settings.CMS_PREFIX:
        #   slugs = url.strip('/').split('/')
        #   if len(slugs)>0:
        #       if slugs[0] != cms_settings.CMS_PREFIX:
        #           url = '%s%s' % (cms_settings.CMS_PREFIX, url)


        return url

    def get_breadcrumbs(self):
        if self.home:
            breadcrumbs = []
        else:
            # if self.parent:
            #   slug = "%s/%s" % (self.parent.slug, self.slug)
            breadcrumbs = []

            # If is original
            if self.get_published():
                for ancestor in self.get_ancestors():
                    breadcrumbs.append(ancestor.get_published())
            # Else if it is the published version
            else:
                # if self.published_from != None:
                if self.published_from:
                    for ancestor in self.published_from.get_ancestors():
                        breadcrumbs.append(ancestor.get_published())
                else:
                    for ancestor in self.get_ancestors():
                        breadcrumbs.append(ancestor.get_published())
        return breadcrumbs

    def get_child_pages(self, include_self=False):
        if self.published_from:
            children = []
            for child in self.published_from.get_descendants(include_self=include_self):
                if child.published == True:
                    children.append(child)
            return children
        else:
            return self.get_descendants(include_self=include_self)

    def get_root_page(self):
        # TODO: improve
        if self.get_published():
            return self.get_root()
        else:
            if self.published_from:
                return self.published_from.get_root()
            else:
                return self.get_root()

    @property
    def has_published_version(self):
        try:
            page = self.__class__.objects.get(published_from=self, published=True)
            return True
        except:
            return False

    def images(self):
        from django.utils.translation import get_language

        images = []
        if self.published_from:
            # Get the the original translation in the right language
            translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self.published_from)
        else:
            # Get the the original translation in the right language
            translation = self.CMSMeta.translation_class.objects.get(language_code=get_language(), parent=self)
        
        images = FileToObject.objects.filter(content_type=ContentType.objects.get_for_model(translation), object_pk=translation.id, file__is_image=True).order_by('order_id')

        return images

    def feature_image(self):

        images = self.images()

        if images.count() > 0:
            return images[0]
        else:
            return False


    def documents(self):
        documents = []

        if self.published_from:
            if hasattr(self.CMSMeta, 'document_class'):
                documents = self.CMSMeta.document_class.objects.filter(parent=self.published_from).order_by('order_id')
        else:
            if hasattr(self.CMSMeta, 'document_class'):
                documents = self.CMSMeta.document_class.objects.filter(parent=self).order_by('order_id')

        return documents

    def links(self):
        links = []

        if self.published_from:
            if hasattr(self.CMSMeta, 'link_class'):
                links = self.CMSMeta.link_class.objects.filter(parent=self.published_from).order_by('order_id')
        else:
            if hasattr(self.CMSMeta, 'link_class'):
                links = self.CMSMeta.link_class.objects.filter(parent=self).order_by('order_id')

        return links


    # Since the MPTT method get_siblings doesn't include self by default
    # We need to use this method to all siblings including self in a template view
    @property
    def siblings(self):
        return self.get_siblings(include_self=True)


# Handle the publising workflow of a translation model
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

class PageTranslation(models.Model, PublishTranslation):
    parent = models.ForeignKey('Page', related_name='translations')
    title = models.CharField(_('Page title'), max_length=100)
    slug = models.SlugField(max_length=100)
    language_code = models.CharField(
        _('language'), max_length=7, choices=settings.LANGUAGES,
        blank=False, null=False
    )
    content = models.TextField(blank=True)

    #Meta data
    # meta_title = models.CharField(max_length=100, blank=True)
    # meta_description = models.TextField(blank=True)

    class Meta:
        unique_together = ('parent', 'language_code')

        if len(settings.LANGUAGES) > 1:
            verbose_name=_('Translation')
            verbose_name_plural=_('Translations')
        else:
            verbose_name=_('Content')
            verbose_name_plural=_('Content')

    def __unicode__(self):
        return u'%s - %s' % (self.title, dict(settings.LANGUAGES).get(self.language_code))

    @property
    def get_content(self):
        return json.loads(self.content)

    def get_attr(self, attr_name):
        try:
            return self.get_content[attr_name]
        except:
            return ''


reversion.register(PageTranslation)


class PageMask(models.Model):
    name = models.CharField(max_length=50)
    config = models.TextField()

    class Meta:
        verbose_name=_('Page Mask')
        verbose_name_plural=_('Page Masks')

    def __unicode__(self):
        return u'%s' % self.name

    def get_fields(self):
        try:
            return json.loads(self.config)
        except:
            raise Exception('JSON config could not be loaded from Page mask')

# class PageTranslationDynamic(MultilingualTranslation, PublishTranslation):
#   parent = models.ForeignKey('PageDynamic', related_name='translations_dynamic')

#   class Meta:
#       unique_together = ('parent', 'language_code')

#       if len(settings.LANGUAGES) > 1:
#           verbose_name=_('Translation')
#           verbose_name_plural=_('Translations')
#       else:
#           verbose_name=_('Content')
#           verbose_name_plural=_('Content')

#   def __unicode__(self):
#       return u'%s' % (dict(settings.LANGUAGES).get(self.language_code))


class PageDocument(models.Model):

    def call_naming(self, instance=None):
        from cmsbase.widgets import get_media_upload_to

        # return get_media_upload_to(self.page.slug, 'pages')
        location = "cms/documents%s/%s"%(self.parent.slug, instance)
        return location

    parent = models.ForeignKey('Page')
    name = models.CharField(_('Name'), max_length=250, blank=True)
    document = models.FileField(upload_to=call_naming, max_length=100)
    # Ordering
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ('order_id',)
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def delete(self, *args, **kwargs):
        storage, path = self.document.storage, self.document.path
        super(PageDocument, self).delete(*args, **kwargs)
        # Physically delete the file
        storage.delete(path)

    def filename(self):
        if self.name:
            return self.name
        path = self.document.name.split('/')
        filename = path[len(path)-1]
        return filename


class PageLink(models.Model):

    parent = models.ForeignKey('Page')

    link_name = models.CharField(_('Link to (name)'), max_length=250, blank=True, help_text=_('Eg: Click here for more info'))
    url = models.URLField(_('Link to (URL)'), max_length=250, blank=True, help_text=_('Eg: http://example.com/info'))
    description = models.TextField(_('Description'), max_length=250, blank=True)

    # Ordering
    order_id = models.IntegerField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order_id','link_name',)
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __unicode__(self):
        return u'%s' % (self.link_name)


class Page(BasePage):

    class Meta:
        verbose_name=_('Page')
        verbose_name_plural=_('Pages')
        permissions = (
            ("can_publish", "Can publish"),
        )

    class CMSMeta:
        # A tuple of templates paths and names
        templates = cms_settings.CMS_PAGE_TEMPLATES
        # Indicate which Translation class to use for content
        translation_class = PageTranslation
        # Provide the url name to create a url for that model
        model_url_name = 'cms:page'

        # Provide the inline image model if necessary
        # if cms_settings.CMS_PAGE_IMAGES:
        #   image_class = PageImage

        # Provide the inline document model if necessary
        if cms_settings.CMS_PAGE_DOCUMENTS:
            document_class = PageDocument

        # Provide the inline link model if necessary
        if cms_settings.CMS_PAGE_LINKS:
            link_class = PageLink

# class PageDynamic(BasePage):

#   class Meta:
#       verbose_name=_('Page (dynamic)')
#       verbose_name_plural=_('Pages (dynamic)')
#       permissions = (
#           ("can_publish", "Can publish"),
#       )

#   class CMSMeta:
#       # A tuple of templates paths and names
#       templates = cms_settings.CMS_PAGE_TEMPLATES
#       # Indicate which Translation class to use for content
#       translation_class = PageTranslationDynamic
#       # Provide the url name to create a url for that model
#       model_url_name = 'cms:pagedynamic'

#       # Provide the inline image model if necessary
#       # if cms_settings.CMS_PAGE_IMAGES:
#       #   image_class = PageImage

#       # Provide the inline document model if necessary
#       if cms_settings.CMS_PAGE_DOCUMENTS:
#           document_class = PageDocument

#       # Provide the inline link model if necessary
#       if cms_settings.CMS_PAGE_LINKS:
#           link_class = PageLink


