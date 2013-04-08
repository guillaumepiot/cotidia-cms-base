from django.contrib.sitemaps import Sitemap
from cms.models import Page

class CMSSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Page.objects.get_published_live()

    def lastmod(self, obj):
        return obj.date_updated