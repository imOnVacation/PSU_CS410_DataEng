import pandas as pd
#import csv 
#import pandera as pa
import numpy as np
import pandas_schema 
from pandas_schema import Column 
from pandas_schema.validation import CustomElementValidation

def check_year(num):
    if num == 2019: return True
    return False

def check_uniqueID(id):
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
            usecols = ['Crash ID', 'Record Type'])
    data = data.loc[data['Record Type'] == 1]
    arr = data['Crash ID'].to_numpy()
    count = 0
    for i in arr:
        if i == id and count >= 2:
            count += 1
            if count >= 2: return False
    return True

def check_vehicle(id):
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
            usecols = ['Record Type', 'Vehicle ID'])
    data = data.loc[data['Record Type'] == 3]
    arr = data['Vehicle ID'].to_numpy()
    for i in arr:
        if i == id: return True
    return False  

def check_participant(id):
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
            usecols = ['Record Type', 'Participant ID'])
    data = data.loc[data['Record Type'] == 3]
    arr = data['Participant ID'].to_numpy()
    for i in arr:
        if i == id: return True
    return False  

null_validation = [CustomElementValidation(lambda d: d is not np.nan, 'Every crash occurred on a date')]
crashID_validation = [CustomElementValidation(lambda i: check_uniqueID(i), 'Every crash has a unique ID')]
year_validation = [CustomElementValidation(lambda i: check_year(i), 'Every crash occurred during the year 2019')]
vehicle_validation = [CustomElementValidation(lambda i: check_vehicle(i), 'Every vehicle ID listed in the crash data was part of a known crash.')]
participant_validation = [CustomElementValidation(lambda i: check_participant(i), 'Every participant ID listed in the crash data was part of a known crash')]

# In this validate_data123 function 
# We are able to validate the Existence, Limit, Intra-record Assertions
def validate_data123():
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
            usecols = ['Crash ID','Record Type', 'Crash Month', 'Crash Day', 'Crash Year'])
    data = data.loc[data['Record Type'] == 1]
    schema = pandas_schema.Schema([
        Column('Crash ID', crashID_validation),
        Column('Record Type', null_validation),
        Column('Crash Month', null_validation),
        Column('Crash Day', null_validation),
        Column('Crash Year', year_validation)
    ])
    errors = schema.validate(data)
    pd.DataFrame({'col':errors}).to_csv('errors.csv')

# In this validate_data4 function
# We are able to validate the Inter-record Assertion
def validate_data4():
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
        usecols = ['Crash ID','Record Type', 'Vehicle ID', 'Participant ID'])
    data = data.loc[data['Record Type'] == 3]
    schema = pandas_schema.Schema([
        Column('Crash ID', crashID_validation),
        Column('Record Type', null_validation),
        Column('Vehicle ID', vehicle_validation),
        Column('Participant ID', participant_validation)
    ])
    errors = schema.validate(data)
    pd.DataFrame({'col':errors}).to_csv('errors.csv')

# In this validate_data56 function
# We are able to validate the Summary and Statistical Assertions
def validate_data56():
    data = pd.read_csv('Oregon Hwy 26 Crash Data for 2019 - Crashes on Hwy 26 during 2019.csv', 
        usecols = ['Crash ID','Record Type', 'Vehicle ID'])
    data1 = data.loc[data['Record Type'] == 1]
    count_crash = data1.shape[0]
    data2 = data.loc[data['Record Type'] == 3]
    data2 = data2.apply(lambda x : True if x['Vehicle ID'] != 0 else False, axis = 1)
    count_vehicle = len(data2[data2 == True].index)
    if count_crash >= 1000000:
        print("There were thousands of crashes but not millions.")
    if count_vehicle >= 1000000:
        print("here were thousands of vehicles involved in crashes but not millions.")
    print("Number of Oregon Hwy 26 Crash for 2019: ", count_crash)
    print("Number of Oregon Hwy 26 Crash Vehicle for 2019: ", count_vehicle)
    ret1 = count_crash /12 
    ret2 = count_vehicle / 12
    if ret1 < 5 and ret1 > 50:
       print("Crashes are evenly/uniformly distributed throughout the months of the year.")
    if ret2 < 10 and ret2 > 100:
       print("The number of vehicles crashes are evenly/uniformly distributed throughout the months of the year.")
    print("Average Crash during a month: ", ret1)
    print("Average Vehicle crash during a month: ", ret2)

if __name__ == '__main__':
    validate_data123()
    validate_data4()
    validate_data56()