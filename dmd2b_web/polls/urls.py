from django.conf.urls import url
from . import views
from polls.views import *
from polls.models import *

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.PatientList.as_view(), name='patient'),

    url(r'^(?P<pk>[0-1]+)/$', views.StudyList.as_view(), name='study'),

    url(r'^(?P<pk>[1-2]+)/$', views.SeriesList.as_view(), name='serie'),

    url(r'^(?P<pk>[2-3]+)/$', views.HeaderList.as_view(), name='header'),

    url(r'^study/new/$', views.StudyView.as_view(), name='detail'),

    url(r'^serie/new/$', views.SeriesView.as_view(), name='detail'),

    url(r'^header/new/$', views.HeaderView.as_view(), name='detail'),
]
