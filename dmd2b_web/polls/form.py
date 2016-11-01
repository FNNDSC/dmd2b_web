from django.views.generic import *
from django import forms
from polls.views import *
from polls.models import *



class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientDetails
        fields = ('PatientID', 'PatientSex', 'PatientBirthDate', 'Age_Days', 'PatientName', 'PatientReportedAge')


class StudyForm(forms.ModelForm):
    class Meta:
        model = StudyDetails
        fields = ('patient', 'StudyID', 'StudyDescription', 'StudyDate')


class SeriesForm(forms.ModelForm):
    class Meta:
        model = SeriesDetails
        fields = ('patient', 'study', 'SeriesID', 'SeriesDescription', 'Modality')


class HeaderForm(forms.ModelForm):
    class Meta:
        model = AdditionalHeaderInfo
        fields = ('ProtocolName', 'dimensions', 'PrimarySliceDirection', 'VoxelSizes', 'fov', 'PatientID')

        
class PatientSearchForm(forms.Form):
    """Form intended to be used in GET requests.
    The field name below (`search`) is passed in the url querystring.
    eg: http://mysite.com/slug/?name=foobar"""
    search = forms.CharField(label='Name')
