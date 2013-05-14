from django.conf import settings

# The default page templates
CMS_PAGE_TEMPLATES = getattr(settings, 'CMS_PAGE_TEMPLATES', (('cmsbase/page.html', 'Default page'),))

CMS_PAGE_IMAGES = getattr(settings, 'CMS_PAGE_IMAGES', False)