# coding: utf-8
"""
Cauê Thenório - cauelt(at)gmail.com

This snippet makes Django do not create URL languages prefix (i.e. /en/)
for the default language (settings.LANGUAGE_CODE).

It also provides a middleware that activates the language based only on the URL.
This middleware ignores user session data, cookie and 'Accept-Language' HTTP header.

Your urls will be like:

In your default language (english in example):

    /contact
    /news
    /articles

In another languages (portuguese in example):

    /pt/contato
    /pt/noticias
    /pt/artigos

To use it, use the 'simple_i18n_patterns' instead the 'i18n_patterns'
in your urls.py:

    from this_sinppet import simple_i18n_patterns as i18n_patterns

And use the 'SimpleLocaleMiddleware' instead the Django's 'LocaleMiddleware'
in your settings.py:

    MIDDLEWARE_CLASSES = (
    ...
        'this_snippet.SimpleLocaleMiddleware'
    ...
    )

Works on Django >=1.4
"""

import re

from django.conf import settings
from django.conf.urls import patterns
from django.core.urlresolvers import LocaleRegexURLResolver
from django.middleware.locale import LocaleMiddleware
from django.utils.translation import get_language, get_language_from_path
from django.utils import translation


class SimpleLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):

        if self.is_language_prefix_patterns_used():
            lang_code = (get_language_from_path(request.path_info) or
                         translation.get_language())

            translation.activate(lang_code)
            request.LANGUAGE_CODE = translation.get_language()



class NoPrefixLocaleRegexURLResolver(LocaleRegexURLResolver):

    @property
    def regex(self):
        language_code = get_language()

        if language_code not in self._regex_dict:
            regex_compiled = (re.compile('', re.UNICODE)
                              if language_code == settings.LANGUAGE_CODE
                              else re.compile('^%s/' % language_code, re.UNICODE))

            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]


def simple_i18n_patterns(prefix, *args):
    """
    Adds the language code prefix to every URL pattern within this
    function, when the language not is the main language.
    This may only be used in the root URLconf, not in an included URLconf.

    """
    pattern_list = patterns(prefix, *args)
    if not settings.USE_I18N:
        return pattern_list
    return [NoPrefixLocaleRegexURLResolver(pattern_list)]