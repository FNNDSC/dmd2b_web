import sys
import os
import codecs
import csv
from datetime import datetime
import re

pydicomdir = os.path.join(os.getcwd(), "pydicom-master")

##dicomfiles = os.path.join("C:\Boston Children Hospital\DicomInfoExtraction\image", "sample")

os.chdir(r"/net/tautona/neuro/labs/grantlab/users/yves.verpillieux/DicomInfoExtraction/prg/dicom")

print (os.getcwd())

outputDir = os.path.join(r"/net/tautona/neuro/labs/grantlab/users/yves.verpillieux/DicomInfoExtraction", "output")

#dicomDirTopLevel = os.path.join(os.getcwd(), "SammyTestData")

sys.path.append(pydicomdir)


from pydicom import dicomio


def retrieveDicomFiles():
        """retireves all DICOM files stored in folders.
        """
        lstFilesDCM = []
        for dirname, dirnames, filenames in os.walk('.', topdown=True, followlinks=True):
             for filename in filenames:

                if ".dcm" in filename.lower():

                     lstFilesDCM.append(os.path.join(dirname,filename))
        return lstFilesDCM



def extractPatientDetails(inputImageFile):
    """Reads and extracts Patient's Basic Info from a DICOM file.
    """
    PatientList = []
    dicomfile = inputImageFile
    tracker = set()

    for i, dfile in enumerate(dicomfile):

        patientDetails = {}
        ds = dicomio.read_file(dfile)
        trackerID = str(ds.PatientID)
        if trackerID in tracker:
            ''
        else:
            patientDetails["PatientID"]=ds.PatientID
            patientDetails["PatientName"]= str.replace(str(ds.PatientName),'^',' ')
            patientDetails["PatientSex"]=ds.PatientSex
            if ds[0x00101010]:
                #print(ds[0x00101010])
                patientDetails["PatientReportedAge"]=ds.PatientAge
            else:
                patientDetails["PatientReportedAge"]=''

            dob = datetime.strptime(ds.PatientBirthDate , '%Y%m%d')
            sod = datetime.strptime(ds.StudyDate, '%Y%m%d')
            patientDetails["PatientBirthDate"]= dob

            patientDetails['Age_Days']= str.replace(str(sod-dob),'days, 0:00:00','')
            tracker.add(str(ds.PatientID))
            PatientList.append(patientDetails)

    return PatientList


def extractStudyDetails(inputImageFile):
    """Reads and extracts Patient's Basic Info from a DICOM file.
    """
    studyList = []
    dicomfile = inputImageFile
    tracker = set()
    trackerID=''
    for i, dfile in enumerate(dicomfile):

        studyDetails = {}
        ds = dicomio.read_file(dfile)

        if ds[0x0020000d]:
            #print(ds[0x0020000d])
            trackerID = str(ds.StudyInstanceUID)
            if trackerID in tracker:
                ''
            else:
                studyDetails["StudyID"]= ds.StudyInstanceUID
                studyDetails["StudyDescription"]=ds.StudyDescription
                studyDetails["StudyDate"]= datetime.strptime(ds.StudyDate, '%Y%m%d')
                studyDetails["PatientID"]=ds.PatientID
                tracker.add(str(ds.StudyInstanceUID))

                studyList.append(studyDetails)
        else:
            ''

    return studyList


def extractSeriesDetails(inputImageFile):
    """Reads and extracts Patient's Basic Info from a DICOM file.
    """
    seriesList = []
    dicomfile = inputImageFile
    tracker = set()

    for i, dfile in enumerate(dicomfile):

        seriesDetails = {}
        ds = dicomio.read_file(dfile)
        trackerID = str(ds.SeriesInstanceUID)
        if trackerID in tracker:
            ''
        else:
            seriesDetails["SeriesID"]=ds.SeriesInstanceUID
            seriesDetails["SeriesDescription"]=ds.SeriesDescription
            if ds[0x00080060]:
                seriesDetails["Modality"]=ds.Modality
            else:
                seriesDetails["Modality"]=''

            if ds[0x00200010]:
                seriesDetails["StudyID"]=ds.StudyID
            else:
                seriesDetails["StudyID"]=''

         #   if ds[0x00181030]:
         #      seriesDetails["ProtocolName"]=ds.ProtocolName
       #     else:
         #      seriesDetails["ProtocolName"]=''

        #    if ds[0x00540500]:
        #        seriesDetails["SliceProgressionDirection"]=ds.SliceProgressionDirection
         #   else:
         #       seriesDetails["SliceProgressionDirection"]=''

         #   if ds[0x00280010]:
          #      seriesDetails["Rows"]=ds.Rows
         #   else:
         #       seriesDetails["Rows"]=''

          #  if ds[0x00280011]:
          #      seriesDetails["Columns"]=ds.Columns
         #   else:
           #     seriesDetails["Columns"]=''


            seriesDetails["PatientID"]=ds.PatientID


            tracker.add(str(ds.SeriesInstanceUID))


            seriesList.append(seriesDetails)

    return seriesList



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
                #print(xx[24:])
                inforDict["PrimarySliceDirection"]=''.join(xx[24:])

            if "ProtocolName" in xx:

                inforDict["ProtocolName"]=''.join(xx[14:])
                print(xx)

            if "voxel sizes" in xx:

                inforDict["VoxelSizes"]=''.join(xx[15:])
                print(xx)

            if "fov" in xx:
                inforDict["fov"]=''.join(xx[15:])

            if "dimensions" in xx:

                inforDict["dimensions"]=''.join(xx[15:])

            if "SeriesInstanceUID" in xx:
                print(xx[19:])

                inforDict["SeriesID"]=''.join(xx[19:])



        headerInfoList.append(inforDict)


    return headerInfoList



def saveToFile(inputFile, outputFileName):
        """Writes to a csv file.
        """
        outputFile = outputFileName
        inputfile = inputFile
        output= codecs.open(os.path.join(outputDir, outputFile) +  '.csv' ,'w') #open a file in a directory


        Fieldnames = inputfile[0].keys()

        wr = csv.DictWriter(output, delimiter=',', lineterminator='\n', fieldnames=Fieldnames) # write in a csv file
        wr.writeheader()
        for d in [x for x in inputfile if x.keys() == Fieldnames]:
             wr.writerow(d)


        output.close()



if __name__ == "__main__":

    saveToFile(extractPatientDetails(retrieveDicomFiles()),'TestingOutputFile_PatientDetails')
    saveToFile(extractStudyDetails(retrieveDicomFiles()),'TestingOutputFile_Study')
    saveToFile(extractSeriesDetails(retrieveDicomFiles()),'TestingOutputFile_Series')
    saveToFile(extractAdditionalHeaderInfo(),'TestingOutputFile_AdditionalInfo')

    print('Done!')
