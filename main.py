#TODO this file is the driver code that contains the main function of the pipeline. This file shouuld be run first
from functions import ReadLinksSheet,ParseLinkerSheet,DicomContourPair,parsing,SaveImages,GenerateBatches
import os
import numpy as np
import datetime

#get time stamp for logging the tiemline steps
def getTimeStamp():
  ts  =  str(datetime.datetime.now()).replace(':','-')
  ts = ts.replace(' ','-')
  return ts
def main():

  #Define a nested dictionary with the patient ID is the key and the dicom-countor dictionary is the value
  patienFilePairs = {}

  batchSize = 8

  #define paths
  #Todo put them inexternal config file
  linkSheetPath = 'D:\\final_data\\final_data\\link.csv'
  dicomPath = 'D:\\final_data\\final_data\\dicoms'
  contourPath = 'D:\\final_data\\final_data\\contourfiles'
  outputPath = 'D:\\final_data\\OutputImage'


  # 2 numpy arrays, 1 one for the images and the second for the countours
  # The size of both of them will be l*w*number_of_images (l and w are the size of images)
  # both are initialized with zeros and they will be filled when parsing is complete
  images = None
  masks = None
  initFlag = False # initialization flag for the first time we fill the arrays


  #create log file
  log = open('log-'+getTimeStamp()+'.txt','a')
  # Read the sheet
  log.writelines('started parsing sheet @' + getTimeStamp() + '\n')
  linkerSheet = ReadLinksSheet.ReadSheet(linkSheetPath)

  # parse the sheet
  patientContourDict = ParseLinkerSheet.ParseSheet(linkerSheet)
  log.writelines('finsihed parsing sheet @' + getTimeStamp()+'\n')



  log.writelines('started creating  patients-files dictyionary @' + getTimeStamp()+'\n')
  #construct the nested dictionary of the patients-files pairs
  for patient, countour in patientContourDict.iteritems():
    patienFilePairs[patient] =  DicomContourPair.DicomContourPair(patient,countour,dicomPath,contourPath)
  log.writelines('Finished creating  patients-files dictyionary @' + getTimeStamp()+'\n')


  log.writelines('started creating  dicom-countor  dictyionary per patient  @' + getTimeStamp()+'\n')

  #for each patient: 1 -if dicom has countor, parse dicom
  # 2  parse countor
  # 3- create mask
  for patient in patienFilePairs:
    log.writelines('started patient ' + patient + '  @' + getTimeStamp()+'\n')
    for dicom,countor in patienFilePairs[patient].iteritems():
      # check if dicom has countor
      if countor:
        dcmDict = parsing.parse_dicom_file(os.path.join(os.path.join(dicomPath,patient,dicom)))
        img = dcmDict['pixel_data']
        l = img.shape[0]
        w = img.shape[1]



        cords = parsing.parse_contour_file(os.path.join(contourPath, patientContourDict[patient],'i-contours',countor))
        mask = parsing.poly_to_mask(cords,l,w)

        # fill the first image in images array
        if not initFlag:
          images = img
          masks = mask
          initFlag = True
        #append to the current images dataset
        else:
          images = np.dstack((images,img))
          masks = np.dstack((masks, mask))

        SaveImages.SaveImage(outputPath,patient,dicom,img,mask)
        log.writelines('Finsihed and Saved image for patient ' + patient + '  @' + getTimeStamp()+'\n')
  log.writelines('Finsished creating  dicom-countor  dictyionary per patient  @' + getTimeStamp()+'\n')

  log.writelines('started creating  batches  @' + getTimeStamp()+'\n')
  #Generate Batches
  batches = GenerateBatches.GenerateBatches(images,images,batchSize)

  log.writelines('Finsished creating  batches  @' + getTimeStamp()+'\n')
  log.close()
  # Now we can build learning model here using the batches generated









if __name__== "__main__":
  main()