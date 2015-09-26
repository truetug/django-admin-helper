# encoding: utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

import logging

logger = logging.getLogger(__name__)


class SuAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
