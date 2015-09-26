# encoding: utf-8
from urllib import urlencode

from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model


def get_user(new_username):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(username=new_username)
    except UserModel.DoesNotExist:
        user = None

    return user


def get_messages(request):
    return messages.get_messages(request)


def add_message(request, level, message, extra_tags='', fail_silently=False, is_safe=False):
    result = False

    if is_safe:
        message = mark_safe(message)

    current_messages = [x.message for x in get_messages(request)._loaded_messages]

    if message not in current_messages:
        level = getattr(messages, level.upper(), messages.INFO)
        result = messages.add_message(request, level, message, extra_tags, fail_silently)

    return result


def get_clean_url(request, *args, **kwargs):
    url = request.path

    params = dict([(k.encode('utf-8'), v.encode('utf-8')) for k, v in request.GET.dict().items()])
    for k in kwargs.get('remove_keys', ()):
        params.pop(k, None)

    for k, v in kwargs.get('replace', {}).items():
        params[k] = v

    if params:
        url = '{0}?{1}'.format(url, urlencode(params))

    return url
