#Todo parse the linkersheet and return a dictionary with patient ID as key  and original ID (contour ID) as value

import pandas as pd
def ParseSheet(sheet):
    #param: sheet dataframe
    #return: dictionary with patient ID as key and original ID (contour ID) as value
    patientContourDict = {}
    # check if sheet is None
    if  sheet.empty:
        raise ValueError("Sheet in None")

    if sheet.columns[0] != 'patient_id' or sheet.columns[1]!='original_id':
        raise ValueError("Invalid Column names in the sheets")
    for index, row in sheet.iterrows():
        patientContourDict[row['patient_id']] = row['original_id']
    return patientContourDict

'''
#Driver code to be used in unit test
#Test cases
# TC 1: Read valid sheet
# TC2 : Read empty sheet (already handled by pandas)
# Tc3: Read sheet with incorrect column names

df = pd.read_csv('D:\\final_data\\final_data\\link.csv')
ParseSheet(df)
'''
