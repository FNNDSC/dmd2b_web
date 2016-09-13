from django.http import *
from django.shortcuts import *
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import inlineformset_factory
from django import forms
from django.db.models import Q

from polls.models import PatientDetails, StudyDetails, SeriesDetails, AdditionalHeaderInfo
from polls.form import *

class Patient(generic.ListView):
    #model = PatientDetails
    template_name = 'polls/patient.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        return PatientDetails.objects.order_by('-PatientBirthDate')
        #return PatientDetails.objects.get(Q(PatientName__startswith='R')|Q(PatientName__startswith='P'))

class Study(generic.ListView):
    #model = PatientDetails
    template_name = 'polls/study.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        #return PatientDetails.objects.order_by('-PatientBirthDate')
        return StudyDetails.objects.filter(StudyDescription__contains='MR-Brain w/o Contrast').order_by('-StudyDate')

class Series(generic.ListView):
    #model = SeriesDetails
    template_name = 'polls/serie.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        return SeriesDetails.objects.filter(SeriesDescription__contains='FUJI Basic Text SR for HL7 Radiological Report')

class Header(generic.ListView):
    #model = AdditionalHeaderInfo
    template_name = 'polls/header.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        return AdditionalHeaderInfo.objects.filter(PrimarySliceDirection__contains='sagittal').filter(ProtocolName__contains='MEMPRAGE')

class StudyView(generic.FormView):
    form_class = StudyForm
    model = StudyDetails
    template_name = 'polls/detail.html'
    sucess_url = '/study/new/'

class SeriesView(generic.FormView):
    form_class = SeriesForm
    model = SeriesDetails
    template_name = 'polls/detail.html'
    sucess_url = '/serie/new/'

class HeaderView(generic.FormView): # HeaderView is linked with the form HeaderForm
    form_class = HeaderForm
    model = AdditionalHeaderInfo
    template_name = 'polls/detail.html'
    sucess_url = '/header/new/' #go to /polls/header/new/
