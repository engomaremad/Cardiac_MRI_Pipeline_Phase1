#Todo: For each patient, save the images that has countors, the countors and an overlay of the image and countour. This is useful for visual inspection

from PIL import Image, ImageFilter
import numpy as np
import os
def SaveImage(outputPath,patientID,dicomID,dcm,Countor):
    #if outpath path does not exist, create it
    imgName = os.path.join(outputPath,patientID)
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    if not os.path.exists(imgName):
        os.mkdir(imgName)

    #remove the '.dcm' from image name
    dicomID = dicomID.split('.')[0]

    # add dicom ID to the path
    imgName = os.path.join(imgName,dicomID+'.png')

    # Normalize image from array
    # needs to be checked that no division by zero occures if the image is empty
    if np.max(dcm) != np.min(dcm):
        dcm = 255.0* (dcm-np.min(dcm))/((np.max(dcm) - np.min(dcm)))
    else:
        raise ValueError('Can not normalize the image '+patientID+' '+ dicomID )
    #create an image from the array and store in  8 bits mode
    im = Image.fromarray(dcm)
    im = im.convert('L')

    # convert image to RGB
    rgbimg = Image.new("RGBA", im.size)
    rgbimg.paste(im)


    #Create pixel map
    rgbimgPixels = rgbimg.load()

    # find edges in the countor image to get only the boundary of the myocardium
    cnt = Image.fromarray(Countor)
    cnt = cnt.convert('L')
    cntEdge = cnt.filter(ImageFilter.FIND_EDGES)

    # loop over the image and mark the countor boundary with red
    cntEdge = cntEdge.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if cntEdge[i,j]!= 0  :
                rgbimgPixels[i,j] = (255,0,0)

    # save the image
    rgbimg.save(imgName)
    x = 0


'''
driver code for unit testing 
Test cases: 
TC1: Call the function with all valid inputs (pass) 
TC2: call the function with empty dicom image (pass)
TC3 :  call the function with empty mask image (pass)
TC4: Call the function with mask and dicom images with different sizes (does not pass), the pipeline does not suppoty images size problems 
To create invalid inputs, custom numpy arrays were used
SaveImage('D:/','test','dcm',np.random.rand(256,256),np.random.rand(256,256))

'''
