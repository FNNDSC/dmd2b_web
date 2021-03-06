from django.http import *
from django.shortcuts import *
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import inlineformset_factory
from django import forms
from django.db.models import Q

from polls.models import PatientDetails, StudyDetails, SeriesDetails, AdditionalHeaderInfo
from polls.form import PatientForm, StudyForm, SeriesForm, HeaderForm, PatientSearchForm



####################### Generic ListView for each model ########################

class PatientList(generic.ListView): # it returns a list of patient
    #model = PatientDetails
    template_name = 'polls/patient.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        #The following command uses an 'AND' logic search and an 'OR' logic search which is represented by '|'
        return PatientDetails.objects.order_by('-PatientBirthDate').filter(Q(PatientName__startswith='P')|Q(PatientName__startswith='R'))



class StudyList(generic.ListView):
    #model = StudyDetails
    template_name = 'polls/study.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return StudyDetails.objects.filter(StudyDescription__contains='MR-Brain w/o Contrast').order_by('-StudyDate')



class SeriesList(generic.ListView):
    #model = SeriesDetails
    template_name = 'polls/serie.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return SeriesDetails.objects.filter(SeriesDescription__contains='FUJI Basic Text SR for HL7 Radiological Report')



class HeaderList(generic.ListView):
    #model = AdditionalHeaderInfo
    template_name = 'polls/header.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return AdditionalHeaderInfo.objects.filter(PrimarySliceDirection__contains='sagittal').filter(ProtocolName__contains='MEMPRAGE')



class PatientSearchView(generic.ListView):
    """This listview can be filtered thanks to the url querystring parameter.
    We could have inherited from PatientList view, bust for the sake of simplicty, it
    is implemented as this."""

    model = PatientDetails
    template_name = 'polls/patient-search.html'

    def get_filtering(self):
        """Get the optional filtering value (see PatientSearchForm)"""
        return self.request.GET.get('search', None)

    def get_queryset(self):
        """If we get a querystring parameter, we filter the queryset, else we return all Patients
        ordered by reverse BirthDate."""

        qs = super().get_queryset()
        filtering = self.get_filtering()
        if filtering:
            qs = qs.filter(PatientName__startswith=filtering)
        return qs.order_by('-PatientBirthDate')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # We inject a form instance and the query parameter to display in template.
        # we could pass an initial kwarg to the form iot display que query param
        # in the search field
        ctx.update({'search_form': PatientSearchForm(),
                    'search_query': self.get_filtering()})
        return ctx
    
    

############################ View for the forms ################################

class PatientFormView(generic.FormView): # PatientFormView is linked with the form PatientForm
    form_class = PatientForm
    model = PatientDetails
    template_name = 'polls/form.html'
    sucess_url = '/patient/new/' #go to /polls/patient/new/



class StudyFormView(generic.FormView): # StudyFormView is linked with the form StudyForm
    form_class = StudyForm
    model = StudyDetails
    template_name = 'polls/form.html'
    sucess_url = '/study/new/' #go to /polls/study/new/



class SeriesFormView(generic.FormView): # SeriesFormView is linked with the form SeriesForm
    form_class = SeriesForm
    model = SeriesDetails
    template_name = 'polls/form.html'
    sucess_url = '/serie/new/' #go to /polls/serie/new/



class HeaderFormView(generic.FormView): # HeaderFormView is linked with the form HeaderForm
    form_class = HeaderForm
    model = AdditionalHeaderInfo
    template_name = 'polls/form.html'
    sucess_url = '/header/new/' #go to /polls/header/new/
    
    
    
class PatientStandaloneSearchView(generic.FormView):
    """Basic view to display a search form."""
    form_class = PatientSearchForm
    template_name = 'polls/patient-standalone-search.html'

