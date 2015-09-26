# encoding: utf-8
from django.conf.urls import patterns, url

from admin_helper.views import PopupView, SuggestView


urlpatterns = patterns(
    'admin_helper.views',
    url(r'^suggest/$', SuggestView.as_view(), name='suggest'),
    url(r'^popup/$', PopupView.as_view(), name='popup')
)
