"""
Processing the data
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def process_data(train, test, lags):
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
def test_process_data(train,lags):
    # pandas DataFrame of boroondara data
    boroondara_df = pd.read_csv(train, encoding='utf-8').fillna(0)

    # Drop columns that are irrelevant to training the model
    boroondara_df = boroondara_df.drop(['CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY'], axis='columns')

    
    # Convert columns of values at times into rows
    boroondara_df = pd.melt(boroondara_df,
            id_vars=['SCATS Number', 'Location', 'Start Time'],
            var_name='Time', value_name='Traffic')

    # Sort rows
    boroondara_df = boroondara_df.sort_values(by=['SCATS Number', 'Location', 'Start Time'])
    attr = "Traffic"
    
    #Take data for SCATS 970 only
    boroondara_df = boroondara_df.loc[boroondara_df['SCATS Number']==970]
    
    #Data for 1 days
    limit = 96
    
    num_of_days = 2
    
    split_limit = limit*num_of_days
    
    df1 = boroondara_df.iloc[:-split_limit]
    #The rest is for testing
    df2 = boroondara_df.iloc[-split_limit:]

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
    
