from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
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

class Study(generic.ListView):
    #model = PatientDetails
    template_name = 'polls/study.html'
    context_object_name = 'object_list'
    def get_queryset(self):
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

class HeaderView(generic.FormView):
    form_class = HeaderForm
    model = AdditionalHeaderInfo
    template_name = 'polls/detail.html'
    sucess_url = '/polls/search/'

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['PatientID',])

        found_entries = Entry.objects.filter(entry_query).order_by('-PatientID')

    return render_to_response('polls/results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))
