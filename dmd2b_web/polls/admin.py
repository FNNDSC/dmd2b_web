from django.contrib import admin

from .models import PatientDetails, StudyDetails, SeriesDetails, AdditionalHeaderInfo

admin.site.register(PatientDetails)
admin.site.register(StudyDetails)
admin.site.register(SeriesDetails)
admin.site.register(AdditionalHeaderInfo)
