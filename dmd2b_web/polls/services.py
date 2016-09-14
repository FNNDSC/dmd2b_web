# This program is a new version of dmd2b project

import sys
import os
import codecs
import csv
from datetime import datetime
import re
import django

from django.db import models

# Import the project's settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("/neuro/users/yves.verpillieux/DicomInfoExtraction/prg/dmd2b_web")
os.environ["DJANGO_SETTINGS_MODULE"] = "dmd2b_web.settings"
django.setup()

from polls.models import PatientDetails, StudyDetails, SeriesDetails, AdditionalHeaderInfo

pydicomdir = os.path.join(os.getcwd(), "pydicom-master")

##dicomfiles = os.path.join("C:\Boston Children Hospital\DicomInfoExtraction\image", "sample")

os.chdir(r"/net/tautona/neuro/labs/grantlab/users/yves.verpillieux/DicomInfoExtraction/prg/dicom")

print (os.getcwd())

outputDir = os.path.join(r"/net/tautona/neuro/labs/grantlab/users/yves.verpillieux/DicomInfoExtraction", "output")

sys.path.append(pydicomdir)


from pydicom import dicomio



def retrieveDicomFiles():
    """Retrieves all DICOM files stored in folders.
    """
    lstFilesDCM = []
    for dirname, dirnames, filenames in os.walk('.', topdown=True, followlinks=True):

        for filename in filenames:

            if ".dcm" in filename.lower():

                lstFilesDCM.append(os.path.join(dirname,filename))

    return lstFilesDCM



############################ Extract the values ################################


def extractDicomData(inputImageFileList):
    """Reads and extracts Patient's Basic Info from a DICOM file.
    """
    data = {} # dictionary of patients

    for i, dfile in enumerate(inputImageFileList):
        pydicomFileData = dicomio.read_file(dfile)

############################## Patient Details #################################

        patientDetails = {}
        patientID = str(pydicomFileData.PatientID)

        if patientID in data:
            ''
        else:
            patientDetails["PatientName"]= str.replace(str(pydicomFileData.PatientName),'^',' ')
            patientDetails["PatientSex"]=pydicomFileData.PatientSex

            # some problems with that following tag, it miss some values in the DICOM files
            # Possibility to see an empty block in the database
            try:
                if pydicomFileData[0x00101010]:
                    patientDetails["PatientReportedAge"]=pydicomFileData.PatientAge
                else:
                    patientDetails["PatientReportedAge"]=''
            except KeyError:
                pass

            dob = datetime.strptime(pydicomFileData.PatientBirthDate , '%Y%m%d')
            sod = datetime.strptime(pydicomFileData.StudyDate, '%Y%m%d')
            patientDetails["PatientBirthDate"]= dob

            patientDetails['Age_Days']= str.replace(str(sod-dob),'days, 0:00:00','')

            data[patientID] = {}
            data[patientID]["patientInfo"] = patientDetails
            data[patientID]["studies"] = {}

############################## Study Details ###################################

        studyDetails = {}
        studyID=''

        if pydicomFileData[0x0020000d]:
            studyID = str(pydicomFileData.StudyInstanceUID)

            if studyID in data[patientID]["studies"]:
                ''
            else:
                studyDetails["StudyDescription"]=pydicomFileData.StudyDescription
                studyDetails["StudyDate"]= datetime.strptime(pydicomFileData.StudyDate, '%Y%m%d')

                data[patientID]["studies"][studyID] = {}
                data[patientID]["studies"][studyID]["studyInfo"] = studyDetails
                data[patientID]["studies"][studyID]["series"] = {}

############################## Series Details ##################################

            seriesDetails = {}
            seriesID = str(pydicomFileData.SeriesInstanceUID)

            if seriesID in data[patientID]["studies"][studyID]["series"]:
                ''
            else:
                seriesDetails["SeriesDescription"]=pydicomFileData.SeriesDescription
                if pydicomFileData[0x00080060]:
                    seriesDetails["Modality"]=pydicomFileData.Modality
                else:
                    seriesDetails["Modality"]=''

                data[patientID]["studies"][studyID]["series"][seriesID] = {}
                data[patientID]["studies"][studyID]["series"][seriesID]["seriesInfo"] = seriesDetails
                data[patientID]["studies"][studyID]["series"][seriesID]["headers"] = {}


    return data # it returns several dictionaries saved linearly


######################## Extract Additional Header Info ########################

def extractAdditionalHeaderInfo():
    lstFilesDCM = []
    headerInfoList =[]
    for dirname, dirnames, filenames in os.walk('.', topdown=True, followlinks=True):

        for filename in filenames:

            if "0.info" in filename.lower():

                lstFilesDCM.append(os.path.join(dirname,filename))

    tracker = set()

    for i, dfile in enumerate(lstFilesDCM):

        x = open(dfile,'r').readlines()
        inforDict ={}

        y =x[3:]

        for xx in y:
            if "PatientID" in xx:
                inforDict["PatientID"]=''.join(xx[12:])

            if "Primary Slice Direction" in xx:
                inforDict["PrimarySliceDirection"]=''.join(xx[24:])

            if "ProtocolName" in xx:
                inforDict["ProtocolName"]=''.join(xx[14:])

            if "voxel sizes" in xx:
                inforDict["VoxelSizes"]=''.join(xx[15:])

            if "fov" in xx:
                inforDict["fov"]=''.join(xx[15:])

            if "dimensions" in xx:
                inforDict["dimensions"]=''.join(xx[15:])



        headerInfoList.append(inforDict)


    return headerInfoList   # it returns a list of dictionary


################### Saving the values in a django database #####################


def saveTodb(data):
    """Save in a django database created by the models
    """
    #print(data)

############### Saving Patient Details in a django database ####################

    for patientID in data: #extract the key patientID from data

        patient = data[patientID]
        pa = PatientDetails()

        pa.PatientID = patientID
        pa.PatientSex = patient['patientInfo']['PatientSex']
        pa.PatientBirthDate = patient['patientInfo']['PatientBirthDate']
        pa.Age_Days = patient['patientInfo']['Age_Days']
        pa.PatientName = patient['patientInfo']['PatientName']

        try:
            pa.PatientReportedAge = patient['patientInfo']['PatientReportedAge']
        except KeyError:
            pass

        pa.save()

################ Saving Study Details in a django database #####################

        studies = patient['studies'] # access to studies of that patient

        for studyID in studies: # extract values of the key studyID from studies

            study = studies[studyID]
            sa = StudyDetails()

            sa.StudyID = studyID
            sa.StudyDate = study['studyInfo']['StudyDate']
            sa.StudyDescription = study['studyInfo']['StudyDescription']

            sa.patient = pa

            sa.save()

################ Saving Series Details in a django database ####################

            series = study['series'] # access to series of that study

            for serieID in series: # extract values of the key serieID from series

                serie = series[serieID]
                se = SeriesDetails()

                se.SeriesID = serieID
                se.SeriesDescription = serie['seriesInfo']['SeriesDescription']
                se.Modality = serie['seriesInfo']['Modality']

                se.patient = pa
                se.study = sa

                se.save()

############## Saving Additional Header Info in a django database ##############

def saveDB(headerInfoList, outputFile): # This is not the best solution
    """Writes to a csv file.
    """
    #print(headerInfoList)

    output= codecs.open(os.path.join(outputDir, outputFile) +  '.csv' ,'w') #open a file in a directory
                                                                            #and write data in it

    Fieldnames = headerInfoList[0].keys()

    wr = csv.DictWriter(output, delimiter=',', lineterminator='\n', fieldnames=Fieldnames)
    wr.writeheader()

    for d in [x for x in headerInfoList if x.keys() == Fieldnames]:

        wr.writerow(d)

    output.close()


    with open('/net/tautona/neuro/labs/grantlab/users/yves.verpillieux/DicomInfoExtraction/output/Header.csv', 'r') as csvfile:

        # Read the csv file which is stored in the folder "output"
        reader = csv.DictReader(csvfile, delimiter=',', lineterminator='\n', fieldnames=Fieldnames)

        for row in reader:

            hi = AdditionalHeaderInfo()

            hi.ProtocolName = row['ProtocolName']
            hi.PatientID = row['PatientID']
            hi.dimensions = row['dimensions']
            hi.PrimarySliceDirection = row['PrimarySliceDirection']
            hi.VoxelSizes = row['VoxelSizes']
            hi.fov = row['fov']

            hi.save()

        csvfile.close()


'''
def savedb(headerInfoList):

    print(headerInfoList)

    for hi in headerInfoList:

        hi = AdditionalHeaderInfo()

        hi.PatientID = headerInfoList['PatientID']
        hi.SeriesID = headerInfoList['SeriesID']
        hi.fov = headerInfoList['fov']
        hi.dimensions = headerInfoList['dimensions']
        hi.VoxelSizes = headerInfoList['VoxelSizes']
        hi.PrimarySliceDirection = headerInfoList['PrimarySliceDirection']
        hi.ProtocolName = headerInfoList['ProtocolName']

        hi.save()
'''


if __name__ == "__main__":

    saveTodb(extractDicomData(retrieveDicomFiles()))
    saveDB(extractAdditionalHeaderInfo(),'Header')
    #savedb(extractAdditionalHeaderInfo())

    print('Done!')
