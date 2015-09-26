# encoding: utf-8
import logging

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib.auth import logout, login, get_user_model

from admin_helper.utils import get_clean_url
from admin_helper.settings import SU_KEY, SU_BACKEND, IGNORE_LIST, GET_USER_FUNC


logger = logging.getLogger(__name__)


class CheckSuMiddleware(object):
    """
    Check for necessary settings
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        need_check = not (request.is_ajax() or request.path in IGNORE_LIST)
        if need_check and SU_KEY in request.session:
            url = get_clean_url(request, replace={
                SU_KEY: request.session.get(SU_KEY)
            })

            msg = _('You work under someone else\'s account. Be extremely careful!')
            full_msg = mark_safe(u'{message} <a href="{url}">{title}</a>'.format(
                message=msg,
                url=url,
                title=_('Return to your account')
            ))

            replaced, storage = False, messages.get_messages(request)
            for msg_obj in storage._loaded_messages:
                if msg_obj.message.startswith(msg):
                    msg_obj.message = full_msg
                    replaced = True

            if not replaced:
                messages.add_message(request, messages.WARNING, full_msg)

        return None


class SuMiddleware(object):
    def process_request(self, request):
        result = None

        if not request.user.is_authenticated():
            return result

        current_username = request.user.get_username()

        is_key_exist = SU_KEY in request.session and request.session[SU_KEY]
        original_username = is_key_exist or current_username

        new_username = request.GET.get('su')

        need_su = new_username and new_username != current_username
        can_su = request.user.is_superuser or settings.DEBUG or original_username == new_username

        if need_su and can_su:
            logger.info(
                'Authorize %s "%s" as "%s"',
                'superuser' if request.user.is_superuser else 'user',
                original_username,
                new_username,
            )

            UserModel = get_user_model()
            try:
                user = GET_USER_FUNC(new_username)

                # Remove su_key from user session
                if SU_KEY in request.session:
                    logger.debug('Delete original "%s"', original_username)
                    del request.session[SU_KEY]

                UserModel.backend = SU_BACKEND

                logout(request)
                login(request, user)

                # Set session key for new user
                if new_username != original_username:
                    logger.debug('Set user "%s" as original', current_username)
                    request.session[SU_KEY] = original_username
            except UserModel.DoesNotExist:
                logger.warning('No such user in system "%s"', new_username)

            url = get_clean_url(request, remove_keys=[SU_KEY])
            result = HttpResponseRedirect(url)

        return result
