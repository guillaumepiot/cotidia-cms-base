from django.conf import settings

# The default page templates
CMS_PAGE_TEMPLATES = getattr(settings, 'CMS_PAGE_TEMPLATES', (('cmsbase/page.html', 'Default page'),))

# Enable inline images for pages
CMS_PAGE_IMAGES = getattr(settings, 'CMS_PAGE_IMAGES', False)

# Enable inline documents for pages
CMS_PAGE_DOCUMENTS = getattr(settings, 'CMS_PAGE_DOCUMENTS', False)

# Enable inline links for pages
CMS_PAGE_LINKS = getattr(settings, 'CMS_PAGE_LINKS', False)

# Enable related pages
CMS_PAGE_RELATED_PAGES = getattr(settings, 'CMS_PAGE_RELATED_PAGES', False)

# Hash uploaded file
CMS_HASH_FILE_NAMES = getattr(settings, 'CMS_HASH_FILE_NAMES', True)