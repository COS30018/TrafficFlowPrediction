"""
Processing the data
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def process_data(train="train.csv", test="test.csv", lags=12):
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
    #print("test")
    #print(df1)
    #print("printing df1[attr]")
    #print(df1[attr])

    names = ["Location", "CD_MELWAY", "NB_LATITUDE", "NB_LONGITUDE", "HF VicRoads Internal", "VR Internal Stat", "VR Internal Loc", "NB_TYPE_SURVEY", "Start Time"]

    cols = list(pd.read_csv("boroondara.csv", nrows=1))
    dftest = pd.read_csv("boroondara.csv", usecols=[i for i in cols if i not in names], encoding="utf-8").fillna(0)
    
    #print("printing iloc") 

    #there are 30 days (1 - 31), there are 4 entries? 
    #train data can be 3*30 days, test data can be 1*30
    
    currentRowIndex = 0 

    #loop through all rows in the dataset
    #while currentRowIndex != dftest.shape[0] :
        #looping through the shit
        #print(dftest.iloc[currentRowIndex]) #print the data
        #currentRowIndex+=1  
        
    #extract some test data from df.iloc[0]


    #load in the new train and test data

    print("loading train data")
    cols1 = list(pd.read_csv("boroondaraUpdatedTrain.csv", nrows=1))
    print("hi")
    dfTrainNew = pd.read_csv("boroondaraUpdatedTrain.csv", usecols=[i for i in cols1 if i not in names], encoding='utf-8').fillna(0)
    print("loading test data")
    cols2 = list(pd.read_csv("boroondaraUpdatedTest.csv", nrows=1))
    print("hi")
    dfTestNew = pd.read_csv("boroondaraUpdatedTest.csv", usecols=[i for i in cols2 if i not in names], encoding='utf-8').fillna(0)

    print("printing new test data:")

    print(dfTestNew.iloc[0])

    exit
    currentRowIndex = 0
    while currentRowIndex != dfTrainNew.shape[0] :
        print(dfTrainNew.iloc[currentRowIndex])
        currentRowIndex+=1

    print("Printing new train data:")

    currentRowIndex = 0

    while currentRowIndex != dfTestNew.shape[0] : 
        print(dfTestNew.iloc[currentRowIndex])
        currentRowIndex+=1

    #exit

    df2 = pd.read_csv(test, encoding='utf-8').fillna(0)

    # scaler = StandardScaler().fit(df1[attr].values)
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df1[attr].values.reshape(-1, 1))
    flow1 = scaler.transform(df1[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    flow2 = scaler.transform(df2[attr].values.reshape(-1, 1)).reshape(1, -1)[0]

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
process_data()
