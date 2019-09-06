#Todo read the link sheet between the images and the countor files
import pandas as pd
import os

def ReadSheet(sheetPath):
    # check if path is valid
    #param: the path to the linker sheet
    # return: dataframe containg the sheet data
    if not os.path.exists(sheetPath):
        raise ValueError ("Sheet path is not valid")
    # load sheet
    sheet = pd.read_csv(sheetPath)
    return sheet

'''
# driver code to be used in unit testing (could be called alone outside the pipeline) with any custom input
#Test cases
# TC1: Read valid file path
# TC2 read invalid file path
path = 'D:\\final_data\\final_data\\link.csv'
pd = ReadSheet(path)
print()
'''
