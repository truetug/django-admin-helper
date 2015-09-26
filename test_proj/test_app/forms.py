from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    error_messages = {
        'wrong_password': 'Sorry, this is wrong password',
        'inactive_account': 'Sorry, your account is disabled',
    }

    username = forms.CharField(label='Username', initial="admin")
    password = forms.CharField(label='Password', initial="admin", widget=forms.PasswordInput())

    def clean(self):
        data = self.cleaned_data

        self.user = authenticate(username=data.get('username'), password=data.get('password'))
        if not self.user or not self.user.is_active:
            self.add_error('__all__', self.error_messages['wrong_password'])
        elif not self.user.is_active:
            self.user = None
            self.add_error('__all__', self.error_messages['inactive_account'])

        return data


class LogoutForm(forms.Form):
    is_confirmed = forms.BooleanField(initial=True, widget=forms.HiddenInput())
