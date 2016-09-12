from django.conf.urls import url
from . import views
from polls.views import *
from polls.models import *

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.PatientView.as_view(), name='patient'),
    url(r'^(?P<pk>[0-1]+)/$', views.StudyView.as_view(), name='detail'),
    url(r'^(?P<pk>[1-2]+)/$', views.SeriesView.as_view(), name='serie'),
    url(r'^(?P<pk>[2-3]+)/$', views.Header.as_view(), name='header'),
    url(r'^header/new/$', views.HeaderView.as_view()),
    #url(r'^header/new/search/$', search, name='search')
]
