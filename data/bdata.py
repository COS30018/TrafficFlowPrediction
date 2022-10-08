"""
Processing the data
"""
import numpy as np  # Provides arrays, matrixies, and maths functions
import pandas as pd # Data analysis and manipulation


def process_data(train, test):
    # pandas DataFrame of boroondara data
    train_df = pd.read_csv(train, encoding='utf-8').fillna(0)
    test_df  = pd.read_csv(test,  encoding='utf-8').fillna(0)

    # Drop columns that are irrelevant to training the model
    train_df = train_df.drop(['CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY'], axis='columns')
    test_df = test_df.drop(['CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY'], axis='columns')

    # Convert columns of values at times into rows
    train_df = pd.melt(train_df,
            id_vars=['SCATS Number', 'Location', 'Start Time'],
            var_name='Time', value_name='Traffic')
    test_df = pd.melt(test_df,
            id_vars=['SCATS Number', 'Location', 'Start Time'],
            var_name='Time', value_name='Traffic')

    # Sort rows
    train_df = train_df.sort_values(by=['SCATS Number', 'Location', 'Start Time'])
    test_df = test_df.sort_values(by=['SCATS Number', 'Location', 'Start Time'])
    # Reorder the index
    train_df = train_df.reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)
    # Scale the traffic values
    train_df['Traffic'] = (
            train_df['Traffic'] - train_df['Traffic'].min()) / \
            (train_df['Traffic'].max()-train_df['Traffic'].min()
    )
    test_df['Traffic'] = (
            test_df['Traffic'] - test_df['Traffic'].min()) / \
            (test_df['Traffic'].max()-test_df['Traffic'].min()
    )


if __name__ == '__main__':
    process_data('data/boroondaraTrain.csv', 'data/boroondaraTest.csv')
