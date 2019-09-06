#Todo create a dictionary that contains the DICOM path as key and the corresponding contour file as value
# if no contour for a dicom, the value is et to None
import os
def GetDicomSeq(dicomName):
    #This function get the sequence number of dicom
    #param: The dicom name
    # return The dicom sequence number

    dicomSeq = dicomName.replace('.dcm','')

    #check if the provided name follows the expected pattern of the data
    if dicomSeq.isdigit() :
        dicomSeq = int(dicomSeq)
    else:
        return -1
    return dicomSeq
def GetCountorSeq(countorName):
    #This function uses the pattern in the data presented
    #in the future work, this pattern could be obtained in a dynamic way
    #This function get the sequence number of dicom
    #param: The dicom name
    # return The dicom sequence number

    countorSeq = countorName.replace('IM-0001-','')
    countorSeq = countorSeq.replace('-icontour-manual.txt', '')

    #check if the provided name follows the expected pattern of the data
    if countorSeq.isdigit():
        countorSeq  = int(countorSeq)
    else:
        return -2
    return countorSeq

def DicomContourPair(patientID,ContourID,dicomPath,countorPath):
    #params: 1- The patient ID
    # The countor ID
    # The path to dicom directory
    # The path to countor directory
    # return: dictionary with dicom file path and corresponding path as value

    #dictionary  of dcmSeq >> dcmFiles
    dcmFiles = {}

    # dictionary  of CountourSeq >> CountorFiles
    cntFiles = {}
    dicomCountor = {}

    if not os.path.exists(dicomPath):
        raise ValueError('Dicom path doesnot exist')
    if not os.path.exists(countorPath):
        raise ValueError('Countor path doesnot exist')
    patientDicom = os.path.join(dicomPath,patientID)
    if not os.path.exists(patientDicom):
        raise ValueError('Patient Dicom path doesnot exist')
    patientCountor = os.path.join(countorPath, ContourID,'i-contours')
    if not os.path.exists(patientCountor):
        raise ValueError('Patient Countor path doesnot exist')
    for dcmFile in os.listdir(patientDicom):
        dcmSeq = GetDicomSeq(dcmFile)
        if dcmSeq != -1:
            dcmFiles[dcmSeq] = dcmFile
    for cntFile in os.listdir(patientCountor):
        cntSeq = GetCountorSeq(cntFile)
        if cntSeq != -2:
            cntFiles[cntSeq] = cntFile

    # Use the 2 dictionaries to construct the dicom- countor dictionary
    # The ideda behind using dictionaries is to make the search for matches in O(1) time for each dicom file
    for dKey, dVal in dcmFiles.iteritems():
        if dKey in cntFiles:
            dicomCountor[dVal] = cntFiles[dKey]
        else:
            dicomCountor[dVal] = None
    return  dicomCountor





'''

#Driver code for unit testing
#Test cases:
# TC1: all parameters are valid
# TC2:  in valid path for dicoms
# TC3 : in valid path for countors
# TC4: Different pattern in naming countor (Fails, due to the fixed pattern)
# TC5: unmatched sequence number if countors that does not have dicoms
DicomContourPair('SCD0000301','SC-HF-I-4','D:\\final_data\\final_data\\dicoms','D:\\final_data\\final_data\\contourfiles')
'''