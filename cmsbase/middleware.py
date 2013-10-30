# from django.conf import settings
# import django.core.exceptions
# from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
# from django.utils.encoding import iri_to_uri

# from cmsbase import settings as cms_settings


# class PrefixURLMiddleware(object):
#     """
#     Middleware that sets adds a root prefix to all URLs
#     It is most commonly used when the site is being proxied from a url with a specific path
#     eg: www.example.com/path/
#     This middleware will add '/path/' at the root of each url to maintain the right location
#     """

#     def process_request(self, request):
#         print "process prefix middleware"
#         if cms_settings.CMS_PREFIX:
#             print request.path_info
#             slugs = request.path_info.strip('/').split('/')
#             print slugs
#             if len(slugs) > 0:
#                 print 'prefix', slugs[0]
#                 if not slugs[0] == cms_settings.CMS_PREFIX:
#                     request.path_info = "/%s%s" % (cms_settings.CMS_PREFIX, request.path_info)
#                     print request.path_info
#                     return HttpResponsePermanentRedirect(request.path_info)
#             # print 'path', path
#             # if localeurl_settings.USE_ACCEPT_LANGUAGE and not locale:
#             #     accept_langs = filter(lambda x: x, [utils.supported_language(lang[0])
#             #                                         for lang in
#             #                                         parse_accept_lang_header(
#             #                 request.META.get('HTTP_ACCEPT_LANGUAGE', ''))])
#             #     if accept_langs:
#             #         locale = accept_langs[0]
#             # locale_path = utils.locale_path(path, locale)
#             # if locale_path != request.path_info:
#             #     if request.META.get("QUERY_STRING", ""):
#             #         locale_path = "%s?%s" % (locale_path,
#             #                 request.META['QUERY_STRING'])
#             #     locale_url = utils.add_script_prefix(locale_path)
#             #     redirect_class = HttpResponsePermanentRedirect
#             #     if not localeurl_settings.LOCALE_REDIRECT_PERMANENT:
#             #         redirect_class = HttpResponseRedirect

#                 #return redirect_class(iri_to_uri(locale_url))
#             #request.path_info = path


