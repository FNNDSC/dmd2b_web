from django.conf.urls import url
from . import views
from polls.views import *
from polls.models import *

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.Patient.as_view(), name='patient'),
    url(r'^(?P<pk>[0-1]+)/$', views.Study.as_view(), name='detail'),
    url(r'^(?P<pk>[1-2]+)/$', views.Series.as_view(), name='serie'),
    url(r'^(?P<pk>[2-3]+)/$', views.Header.as_view(), name='header'),
    url(r'^header/new/$', views.HeaderView.as_view()),
    url(r'^search/$', search, name='polls-search')
]
