from django.conf.urls import url
from . import views
from polls.views import *
from polls.models import *

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.PatientList.as_view(), name='patient'),
    
    url(r'^patient-search/$', views.PatientSearchView.as_view(), name='patient-search'),
    
    url(r'^patient-standalone-search/$',
        views.PatientStandaloneSearchView.as_view(),
        name='patient-standalone-search'),

    url(r'^(?P<pk>[0-1]+)/$', views.StudyList.as_view(), name='study'),

    url(r'^(?P<pk>[1-2]+)/$', views.SeriesList.as_view(), name='serie'),

    url(r'^(?P<pk>[2-3]+)/$', views.HeaderList.as_view(), name='header'),

    url(r'^patient/new/$', views.PatientFormView.as_view(), name='form'),

    url(r'^study/new/$', views.StudyFormView.as_view(), name='form'),

    url(r'^serie/new/$', views.SeriesFormView.as_view(), name='form'),

    url(r'^header/new/$', views.HeaderFormView.as_view(), name='form'),
]
