from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth import get_user_model, login, logout
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages


from test_app.forms import LoginForm, LogoutForm


class FrontpageView(FormView):
    template_name = 'base.html'
    success_url = reverse_lazy('test_app:frontpage')

    def get_form_class(self):
        user = self.request.user
        result = LogoutForm if user and user.is_authenticated() else LoginForm

        return result

    def form_valid(self, form):
        user = self.request.user
        if user and user.is_authenticated():
            logout(self.request)
        else:
            if form.user:
                login(self.request, form.user)
                messages.info(
                    self.request, 
                    'You are logged in as {0}. Thank you for using our site.'.format(
                        form.user.username
                    )
                )
            else:
                messages.error(self.request, 'Oops, something went wrong')


        return super(FrontpageView, self).form_valid(form)