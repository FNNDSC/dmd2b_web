import datetime

from django.db import models
from django.utils import timezone
from django.utils.timezone import now

class PatientDetails(models.Model):
    PatientID = models.CharField(max_length=25)
    PatientSex = models.CharField(max_length=25)
    PatientBirthDate = models.DateTimeField(max_length=25)
    Age_Days = models.CharField(max_length=25)
    PatientName = models.CharField(max_length=25)
    PatientReportedAge = models.CharField(max_length=25)
    def __str__(self):
        return "{0}".format(self.PatientID)

class StudyDetails(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    StudyID = models.CharField(max_length=100)
    StudyDescription = models.CharField(max_length=100)
    StudyDate = models.DateTimeField(max_length=25)
    def __str__(self):
        return "{0}".format(self.StudyID)

class SeriesDetails(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    study = models.ForeignKey(StudyDetails, on_delete=models.CASCADE)
    SeriesID = models.CharField(max_length=100)
    SeriesDescription = models.CharField(max_length=100)
    Modality = models.CharField(max_length=25)
    def __str__(self):
        return "{0}".format(self.SeriesID)

class AdditionalHeaderInfo(models.Model):
    ProtocolName = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100)
    PrimarySliceDirection = models.CharField(max_length=100)
    VoxelSizes = models.CharField(max_length=100)
    fov = models.CharField(max_length=50)
    PatientID = models.CharField(max_length=25)
    def __str__(self):
        return "{0}".format(self.PatientID)
