# encoding: utf-8
from django import template
from django.core.urlresolvers import reverse

from ..settings import SUGGEST_VIEW, SU_KEY


register = template.Library()


@register.inclusion_tag('admin_helper/admin_helper.html', takes_context=True)
def admin_helper(context):
    data, request = {}, context.get('request')
    if request and request.user and request.user.is_authenticated():
        data.update({
            'suggest_url': reverse(SUGGEST_VIEW),
            'init_url': reverse('admin_helper:popup'),
            'current_username': request.user.username,
            'current_fullname': request.user.get_full_name(),
            'original_username': request.session.get(SU_KEY, ''),
            'is_sudoer': request.user.is_superuser or SU_KEY in request.session,
        })

    return data
