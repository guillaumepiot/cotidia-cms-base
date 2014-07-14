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
def add_edit_translation(request, page_id, language_code, recover_id=False, model_class=Page, translation_class=PageTranslation, translation_form_class=TranslationForm):

    if not language_code in [lang[0] for lang in settings.LANGUAGES]:
        raise ImproperlyConfigured('The language code "%s" is not included in the project settings.' % language_code)
    if not request.user.has_perm('cmsbase.add_'+translation_class.__class__.__name__.lower()):
        raise PermissionDenied
    page = get_object_or_404(model_class, id=page_id)

    translation = translation_class.objects.filter(parent=page, language_code=language_code).first()

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
        form = translation_form_class(page=page, initial=initial)
    else:
        title = _('Edit translation')
        if not request.user.has_perm('cmsbase.change_'+translation_class.__class__.__name__.lower()):
            raise PermissionDenied

        form = translation_form_class(instance=translation, page=page, initial=initial)

    if request.method == 'POST':
        if not translation:
            form = translation_form_class(data=request.POST, files=request.FILES, page=page)
        else:
            form = translation_form_class(data=request.POST, files=request.FILES, instance=translation, page=page)
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
            return HttpResponseRedirect(reverse('admin:'+page._meta.app_label+'_'+page._meta.model_name+'_changelist'))




    template = 'admin/cmsbase/add_edit_translation.html'
    context={
        'form':form,
        'title':title,
        'page':page,
        'translation':translation,
        'recover':recover,
        'app_label':page._meta.app_label,
        'model_name':page._meta.model_name,
        'verbose_name_plural':page._meta.verbose_name_plural
    }
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
def translation_revision(request, page_id, language_code, translation_id, model_class=Page, translation_class=PageTranslation):
    template = 'admin/cmsbase/translation_revision.html'
    page = get_object_or_404(model_class, id=page_id)
    translation = get_object_or_404(translation_class, parent=page, language_code=language_code, id=translation_id)

    version_list = reversion.get_unique_for_object(translation)

    context={
        'page':page,
        'translation':translation,
        'version_list':version_list,
        'app_label':page._meta.app_label,
        'model_name':page._meta.model_name,
        'verbose_name_plural':page._meta.verbose_name_plural
    }

    return render_to_response(template, context, context_instance=RequestContext(request))