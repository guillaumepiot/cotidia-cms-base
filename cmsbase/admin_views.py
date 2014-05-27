from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect  
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.db import transaction
from django.contrib import messages

from .models import *
from .admin_forms import *

@login_required
@transaction.atomic()
@reversion.create_revision()
def add_edit_translation(request, page_id, language_code, recover_id=False):
    if not language_code in [lang[0] for lang in settings.LANGUAGES]:
        raise ImproperlyConfigured('The language code "%s" is not included in the project settings.' % language_code)
    if not request.user.has_perm('cmsbase.add_pagetranslation'):
        raise PermissionDenied
    page = get_object_or_404(Page, id=page_id)

    translation = PageTranslation.objects.filter(parent=page, language_code=language_code).first()

    initial = {
        'parent':page,
        'language_code':language_code
    }

    # Check is we are in revision mode
    if recover_id:
        recover = True
        for version in reversion.get_unique_for_object(translation):
            if version.id == int(recover_id):
                # Set values from revision
                translation.title = version.field_dict['title']
                translation.slug = version.field_dict['slug']
                translation.content = version.field_dict['content']
    else:
        recover = False

    if not translation:
        title = _('Add translation')
        form = TranslationForm(page=page, initial=initial)
    else:
        title = _('Edit translation')
        if not request.user.has_perm('cmsbase.change_pagetranslation'):
            raise PermissionDenied

        form = TranslationForm(instance=translation, page=page, initial=initial)

    if request.method == 'POST':
        if not translation:
            form = TranslationForm(data=request.POST, files=request.FILES, page=page)
        else:
            form = TranslationForm(data=request.POST, files=request.FILES, instance=translation, page=page)
        if form.is_valid():
            translation = form.save()
            reversion.set_user(request.user)

            # Notify the parent page that new content needs to be approved
            translation.parent.approval_needed = 1
            translation.parent.save()

            if recover:
                messages.add_message(request, messages.SUCCESS, _('The content for "%s" has been recovered' % translation.title))
            else:
                messages.add_message(request, messages.SUCCESS, _('The content for "%s" has been saved' % translation.title))
            return HttpResponseRedirect(reverse('admin:cmsbase_page_changelist'))




    template = 'admin/cmsbase/add_edit_translation.html'
    return render_to_response(template, {'form':form, 'title':title, 'page':page, 'translation':translation, 'recover':recover}, context_instance=RequestContext(request))

@login_required
def translation_revision(request, page_id, language_code, translation_id):
    template = 'admin/cmsbase/translation_revision.html'
    page = get_object_or_404(Page, id=page_id)
    translation = get_object_or_404(PageTranslation, parent=page, language_code=language_code, id=translation_id)

    version_list = reversion.get_unique_for_object(translation)

    return render_to_response(template, {'page':page, 'translation':translation, 'version_list':version_list}, context_instance=RequestContext(request))