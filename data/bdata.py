"""
Processing the data
"""
import numpy as np  # Provides arrays, matrixies, and maths functions
import pandas as pd # Data analysis and manipulation


def process_data(data):
    # pandas DataFrame of boroondara data
    boroondara_df = pd.read_csv(data, encoding='utf-8').fillna(0)

    # Drop columns that are irrelevant to training the model
    boroondara_df = boroondara_df.drop(['CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY'], axis='columns')

    # Convert columns of values at times into rows
    boroondara_df = pd.melt(boroondara_df,
            id_vars=['SCATS Number', 'Location', 'Start Time'],
            var_name='Time', value_name='Traffic')

    # Sort rows
    boroondara_df = boroondara_df.sort_values(by=['SCATS Number', 'Location', 'Start Time'])
    # Reorder the index
    boroondara_df = boroondara_df.reset_index(drop=True)
    # Scale the traffic values
    boroondara_df['Traffic'] = (boroondara_df['Traffic'] - boroondara_df['Traffic'].min())/(boroondara_df['Traffic'].max()-boroondara_df['Traffic'].min())

if __name__ == '__main__':
    process_data("data/boroondara.csv")
