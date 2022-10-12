"""
Processing the data
"""
#from xml.etree.ElementTree import _FileRead
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def process_data_from_one_file(filename, lags):

    #use the boorondara file and split it into train and test data

    df1 = pd.read_csv(filename, encoding='utf-8').fillna(0)

    #no idea what these 3 things are lolllll
    #scaler = MinMaxScaler(feature_range=(0, 1)).fit(df1[attr].values.reshape(-1, 1))
    #flow1 = scaler.transform(df1[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    #flow2 = scaler.transform(df2[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    
    trainArray, testArray = [], []
    trainArrayBigLongSingleColumn, testArrayBigLongSingleColumn = [], []

    fileRowIndex = 0
    columnIndexOfLocation = 1 #the 'location' column index 
    
    #make a new file with the dropped columns
    dfDataOnly = df1.drop(['SCATS Number','Location' , 'CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY', 'Start Time'], axis='columns')
    print("hi")
    #df1.iloc[row, column] reads the entry
    scanningFile = True
    while fileRowIndex < df1.shape[0]: 
        #first, get the amount of days in the scat site
        days = 0
        
        currentSiteName = df1.iloc[fileRowIndex, columnIndexOfLocation]

        print('site = ' + currentSiteName)
        #loop forward until we find out how many days are recorded for this site
        while df1.iloc[fileRowIndex + days, columnIndexOfLocation] == currentSiteName :
            
            days+=1
            if fileRowIndex + days == df1.shape[0] - 1:
                print("end!")
                break 
            

        #print("days = " + str(days))
        #split the data into 80% train and 20% test data
        for i in range(0, days):
            if i < round(days*0.8) : 
                trainArray.append(dfDataOnly.iloc[fileRowIndex]) 
                for b in range(0, 96):
                    trainArrayBigLongSingleColumn.append(dfDataOnly.iloc[fileRowIndex, b]) 
            else:  
                testArray.append(dfDataOnly.iloc[fileRowIndex]) 
                for b in range(0, 96):
                    testArrayBigLongSingleColumn.append(dfDataOnly.iloc[fileRowIndex, b]) 
            fileRowIndex+=1
            if fileRowIndex == df1.shape[0] - 1:
                fileRowIndex = df1.shape[0]
        print(fileRowIndex)
    print("done")
    #print(trainArray) 

    #convert to dataframe
    newTrainDf = pd.DataFrame(trainArray)
    newTestDf = pd.DataFrame(testArray)
    trainDfSingle = pd.DataFrame(trainArrayBigLongSingleColumn)
    testDfSingle = pd.DataFrame(testArrayBigLongSingleColumn)


    print("printing new train df")
    print(newTrainDf) 
    print("printing new test df")
    print(newTestDf) 

    print("printing new train df in single column form")
    print(trainDfSingle) 
    print("printing new test df in single column form")
    print(testDfSingle) 

    dfbruh = pd.read_csv("data/train.csv", encoding='utf-8').fillna(0)
    print("printing format of train.csv - df[attr]")
    print(dfbruh['Lane 1 Flow (Veh/5 Minutes)'])
    
    
    scaler1 = MinMaxScaler(feature_range=(0, 1)).fit(dfbruh['Lane 1 Flow (Veh/5 Minutes)'].values.reshape(-1, 1))
    scaler2 = MinMaxScaler(feature_range=(0, 1)).fit(dfDataOnly.iloc[0].values.reshape(-1, 1))
    print("scalar original: ")
    print(scaler1)
    print("new scaler")
    print(scaler2)


    print("original flow1")
    flow1 = scaler1.transform(dfbruh['Lane 1 Flow (Veh/5 Minutes)'].values.reshape(-1, 1)).reshape(1, -1)[0]
    print(flow1)

    print("new flow1")

    flow1New = scaler2.transform(trainDfSingle[0].values.reshape(-1, 1)).reshape(1, -1)[0]
    flow2New = scaler2.transform(testDfSingle[0].values.reshape(-1, 1)).reshape(1, -1)[0]
    print(flow1New)
    print("new flow2")
    print(flow2New)
    
    
    train, test = [], []
    for i in range(lags, len(flow1New)):
        train.append(flow1New[i - lags: i + 1])
    for i in range(lags, len(flow2New)):
        test.append(flow2New[i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = test[:, :-1]
    y_test = test[:, -1]
    

    return X_train, y_train, X_test, y_test, scaler2

def process_data(train, test, lags):
    return process_data_from_one_file('data/boroondara.csv', lags)
    print("done")
    exit;
    """Process data
    Reshape and split train\test data.

    # Arguments
        train: String, name of .csv train file.
        test: String, name of .csv test file.
        lags: integer, time lag.
    # Returns
        X_train: ndarray.
        y_train: ndarray.
        X_test: ndarray.
        y_test: ndarray.
        scaler: StandardScaler.
    """
    attr = 'Lane 1 Flow (Veh/5 Minutes)'
    df1 = pd.read_csv(train, encoding='utf-8').fillna(0)
    df2 = pd.read_csv(test, encoding='utf-8').fillna(0)

    # scaler = StandardScaler().fit(df1[attr].values)
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df1[attr].values.reshape(-1, 1))
    flow1 = scaler.transform(df1[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    flow2 = scaler.transform(df2[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    print("start")
    print(flow1)
    print("hi")
    exit
    train, test = [], []
    for i in range(lags, len(flow1)):
        train.append(flow1[i - lags: i + 1])
    for i in range(lags, len(flow2)):
        test.append(flow2[i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = test[:, :-1]
    y_test = test[:, -1]

    return X_train, y_train, X_test, y_test, scaler
