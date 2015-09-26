from django.conf.urls import patterns, url

from test_app.views import FrontpageView


urlpatterns = patterns(
    'test_app.views',
    url(r'^$', FrontpageView.as_view(), name='frontpage'),
)
