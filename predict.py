"""
Made individual predictions from SCATS and datatime
"""
from time import strftime
import warnings
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime as dt

warnings.filterwarnings("ignore")

def process_data(filename='data/boroondara.csv'):
    # Get dataframe data, while converting Start Time to timestamp
    data_df = pd.read_csv(filename, encoding='utf-8', parse_dates=['Start Time']).fillna(0)

    # Drop columns that are irrelevant to making predictions
    data_df = data_df.drop(['CD_MELWAY' ,'NB_LATITUDE', 'NB_LONGITUDE', 'HF VicRoads Internal', 'VR Internal Stat', 'VR Internal Loc', 'NB_TYPE_SURVEY'], axis='columns')

    # Convert columns of values at times into rows
    data_df = pd.melt(data_df,
            id_vars=['SCATS Number', 'Location', 'Start Time'],
            var_name='Time', value_name='Traffic')

    # Sort rows
    data_df = data_df.sort_values(by=['SCATS Number', 'Location', 'Start Time'])
    # Reorder the index
    data_df = data_df.reset_index(drop=True)

    # Convert Time to TimeDelta
    data_df['Time'] = pd.to_timedelta(data_df['Time'])

    # Add Time to Start Time. This effectively combines the Start Time and Time columns
    data_df['Start Time'] = data_df['Start Time'] + data_df['Time']
    # print(data_df)
    # data_df = data_df.drop(['Time'], axis='columns')
    # print(data_df)
    # Scale traffic values
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(data_df['Traffic'].values.reshape(-1, 1))
    data_df['Traffic'] = scaler.transform(data_df['Traffic'].values.reshape(-1, 1)).reshape(1, -1)[0]
    
    return data_df, scaler


def precict(scats, datetime, data_df, scaler,model):
    
    scats_str = str(scats)
    
    datetime = datetime.strftime("%H:%M:%S")
    matching_rows = data_df.index[(data_df['SCATS Number'] == scats) & (data_df['Time'] == datetime)]
    input_df = data_df.iloc[matching_rows[0]-13:matching_rows[0]-1]
    
    input_array = input_df['Traffic'].to_numpy()
    input_array = np.reshape(input_array, (-1, 12))
    
    model_pred = model.predict(input_array)
    # gru_pred  = gru.predict(input_array)
    # saes_pred = saes.predict(input_array)
    # rnn_pred  = rnn.predict(input_array)
    
    model_pred = scaler.inverse_transform(model_pred.reshape(-1, 1)).reshape(1, -1)[0]
    # gru_pred  = scaler.inverse_transform(gru_pred.reshape(-1, 1)).reshape(1, -1)[0]
    # saes_pred = scaler.inverse_transform(saes_pred.reshape(-1, 1)).reshape(1, -1)[0]
    # rnn_pred  = scaler.inverse_transform(rnn_pred.reshape(-1, 1)).reshape(1, -1)[0]
    
    return model_pred[0]
    # , gru_pred[0], saes_pred[0], rnn_pred[0]

def load_model_file(model_type,scats):
    scats_str = str(scats)
    
    model = load_model('model/'+model_type+'/'+scats_str+'.h5')
    
    return model

if __name__ == '__main__':
    data_df, scaler = process_data()
    # lstm, gru, saes, rnn = precict(970, dt(2006, 10, 10, 23, 45),data_df,scaler)
    
    # print(lstm)
    # print(gru)
    # print(saes)
    # print(rnn)

