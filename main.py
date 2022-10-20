"""
Traffic Flow Prediction with Neural Networks(SAEs、LSTM、GRU).
"""
import math
import warnings
import numpy as np
import pandas as pd
from data.data import process_data
from keras.models import load_model
from keras.utils.vis_utils import plot_model
import sklearn.metrics as metrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
warnings.filterwarnings("ignore")


def MAPE(y_true, y_pred):
    """Mean Absolute Percentage Error
    Calculate the mape.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    # Returns
        mape: Double, result data for train.
    """

    y = [x for x in y_true if x > 0]
    y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

    num = len(y_pred)
    sums = 0

    for i in range(num):
        tmp = abs(y[i] - y_pred[i]) / y[i]
        sums += tmp

    mape = sums * (100 / num)

    return mape


def eva_regress(y_true, y_pred):
    """Evaluation
    evaluate the predicted resul.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    """

    mape = MAPE(y_true, y_pred)
    vs = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    print('explained_variance_score:%f' % vs)
    print('mape:%f%%' % mape)
    print('mae:%f' % mae)
    print('mse:%f' % mse)
    print('rmse:%f' % math.sqrt(mse))
    print('r2:%f' % r2)


def plot_results(y_true, y_preds, names, scats_str):
    """Plot
    Plot the true data and predicted data.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
    """
    d = '2016-3-4 00:00'
    x = pd.date_range(d, periods=276, freq='5min')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y_true, label='True Data')
    for name, y_pred in zip(names, y_preds):
        ax.plot(x, y_pred, label=name)

    plt.legend()
    plt.grid(True)
    plt.xlabel('Time of Day')
    plt.ylabel('Flow')

    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    plt.show()

    plt.savefig('images/'+scats_str+'/Result.png')


def main():

    data_df = pd.read_csv('data/boroondara.csv', encoding='utf-8').fillna(0)

    # Iterate over each unique SCATS
    for scats in data_df['SCATS Number'].unique():
        scats_str = str(scats)

        # Load models for the currect SCATS
        lstm = load_model('model/lstm/'+scats_str+'.h5')
        gru = load_model('model/gru/'+scats_str+'.h5')
        saes = load_model('model/saes/'+scats_str+'.h5')
        rnn = load_model('model/rnn/'+scats_str+'.h5')
        models = [lstm, gru, saes, rnn]
        names = ['LSTM', 'GRU', 'SAEs', 'RNN']

        # Get a datafram filtered on just the current SCATS
        scats_df = data_df.loc[data_df['SCATS Number'] == scats]
        lag = 12

        _, _, X_test, y_test, scaler = process_data(scats_df, lag)
        y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]
    
        y_preds = []
        for name, model in zip(names, models):
            if name == 'SAEs':
                X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))
            else:
                X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
            
            # Make folders for the plot images
            if not os.path.exists('images/'+scats_str):
                os.makedirs('images/'+scats_str)
            file = 'images/' + scats_str + '/' + name + '.png'
            # Plot the model
            plot_model(model, to_file=file, show_shapes=True)

            predicted = model.predict(X_test)
            predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
            y_preds.append(predicted[:276])
            print(name)
            
            eva_regress(y_test, predicted)
    
        plot_results(y_test[: 276], y_preds, names, scats_str)


if __name__ == '__main__':
    main()
