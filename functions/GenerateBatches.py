#Todo: Take the entire dataset parsed dicom and mask files and generate batches
import numpy as np
def GenerateBatches(images, masks, batchSize):
    #get the number of images and maskes n
    if np.shape(images) != np.shape(masks):
        raise ValueError('images and masks should have the same shape')
    l,w,n = np.shape(images)

    #check if batch size is valid
    if batchSize <=0:
        raise ValueError('Batch size should be positive and greater than zero  ')
    if batchSize > n:
        raise ValueError('Batch size is greater than the number of images ')

    batches = []

    # randomly shuffle the images and masks in the same order
    rng = range(n)
    np.random.shuffle(rng)
    images = images[:, :, rng]
    masks = masks[:,:,rng]

    # create batches, and append a the tuple of image batch and mask batch to the batches array
    # if the number of image is not divisble by the batch size, the last batch will be with smaller size (the remainder)
    for i in range(0,(n//batchSize)+1):
        imgBatch = images[:,:,i*batchSize:(i+1)*batchSize]
        mskBatch = masks[:,:,i*batchSize:(i+1)*batchSize]
        batches.append((imgBatch,mskBatch))
    return batches



'''
driver code for unit testing
TC1: all parameters are valid (pass)
TC2 : images and and masks with different shapes (pass)
TC3: batch size = 0 (pass)
TC4 : batch size < 0 (pass)
TC5: batch size greater than the number of images (pass)
GenerateBatches(np.zeros((256,256,96)), np.zeros((256,256,96)),100)
'''

