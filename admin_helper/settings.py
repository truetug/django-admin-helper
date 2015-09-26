# encoding: utf-8
from django.conf import settings
from django.utils.importlib import import_module


SUGGEST_VIEW = getattr(
    settings,
    'ADMIN_HELPER_SUGGEST_VIEW',
    'admin_helper:suggest'
)

SU_KEY = getattr(
    settings,
    'ADMIN_HELPER_SU_KEY',
    'su'
)

SU_BACKEND = getattr(
    settings,
    'ADMIN_HELPER_SU_BACKEND',
    'admin_helper.backends.SuAuthBackend'
)

IGNORE_LIST = getattr(
    settings,
    'ADMIN_HELPER_IGNORE_LIST', (
        '/admin/jsi18n/',
    )
)

GET_USER_FUNC = getattr(
    settings,
    'ADMIN_HELPER_GET_USER_FUNC',
    'admin_helper.utils.get_user'
)

GET_USER_FUNC = GET_USER_FUNC.rsplit('.', 1)
GET_USER_FUNC = getattr(import_module(GET_USER_FUNC[0]), GET_USER_FUNC[1])
