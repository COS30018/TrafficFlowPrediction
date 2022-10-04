"""
Processing the data
"""
import sys
import numpy as np  # Provides arrays, matrixies, and maths functions
import pandas as pd # Data analysis and manipulation
from sklearn.preprocessing import MinMaxScaler


def process_data(train,lags):
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

    print(df2.to_string())
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
    print(X_test.shape)
    return X_train, y_train, X_test, y_test, scaler
if __name__ == '__main__':
    process_data("boroondara.csv",12)
