# encoding: utf-8
from django.contrib.auth import get_user_model

from admin_tools.dashboard.modules import DashboardModule


class SuDashboardModule(DashboardModule):
    template = 'admin_tools/dashboard/modules/su.html'
    title = u'Филиал Хогвартса'

    def is_empty(self):
        return self.users is None

    def init_with_context(self, context):
        self.users = None

        if context['request'].user.is_superuser:
            UserModel = get_user_model()
            self.users = UserModel.objects.filter(
                is_active=True
            ).order_by('last_name', 'first_name')
            self.original_user = None
            original_user = context['request'].session.get('su')
            try:
                self.original_user = self.users.get(username=original_user)
            except UserModel.DoesNotExist:
                pass
