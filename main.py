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
import tkinter as tk
from PIL import Image, ImageTk
import folium

warnings.filterwarnings("ignore")
  
canvasCoords = [0, 0]
canvasCoordsMove = [0, 0] 
coordsOnClick = [0,0]
root = tk.Tk() 
canvas = tk.Canvas(root, width = 5000, height = 5000)    

#canvas location (change these to move all scats sites, if we end up making the map larger.)
baseX = 0 
baseY = 0

baseXCoord = -37.86548 #xcoord of scat site 970, 'WARRIGAL_RD N of HIGH STREET_RD'
baseYCoord = 144.09272 #ycoord of scat site 970, 'WARRIGAL_RD N of HIGH STREET_RD'

sites = [] 


#sites.append([970,'WARRIGAL_RD N of HIGH STREET_RD', baseX + 1010,baseY + 1030])


#sites.append([2000,baseX + 1030,baseY + 870])

#open the file
#search through the scat sites and append them to sites

df1 = pd.read_csv('data/boroondara.csv', encoding='utf-8').fillna(0)
fileRowIndex = 0 #start from row 32, because we place the first SCATS site manually.
print("first row checking = " + df1.iloc[32, 1])
while fileRowIndex < df1.shape[0]: 
    print(fileRowIndex)
    currentSiteXCoord = df1.iloc[fileRowIndex, 3] #column 3 is the x coord column
    currentSiteYCoord = df1.iloc[fileRowIndex, 4] #column 4 is the y coord column
    
    currentSCATS = df1.iloc[fileRowIndex, 0] #site 970
    currentRoadName = df1.iloc[fileRowIndex, 1]  #road name (Because SCATS site 970 has 4 different sites. Used for identification)
    
    #append this site to the sites array

    #formula for x position => xPosition = 1302.93159*xCoordinate + 50346.13029
    finalXPos = -2986.93217*currentSiteXCoord-112618.11698

    finalYPos = 26837.06070*currentSiteYCoord-3891155.87538
    #finalXPos = -18283.70735*currentSiteXCoord - 691010.75521
    #finalYPos = -58055.15239*currentSiteYCoord + 8424409.97103 
    #finalYPos = 4637.05459*currentSiteYCoord - 671945.64423
    print(str(currentSCATS) + ", " + currentRoadName)
    print(str(currentSiteXCoord) + ", " + str(currentSiteYCoord))
     
    #print("site = " + currentRoadName + ", x=" + str(finalXPos) + ", y=" + str(finalYPos))

    sites.append([currentSCATS, currentRoadName, finalXPos , finalYPos])
    
    #move to the next site
    while df1.iloc[fileRowIndex, 1] == currentRoadName :
        fileRowIndex+=1
        if fileRowIndex >= df1.shape[0] - 1:
            fileRowIndex = df1.shape[0]
            break;

    #append this site to the sites array

sites.append([970,'Last', baseX + 322,baseY + 471])
sites.append([4812,'SWAN_ST SW of MADDEN_GV', baseX + 370,baseY + 639])



     

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


def plot_results(y_true, y_preds, names):
    """Plot
    Plot the true data and predicted data.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
    """
    d = '2016-3-4 00:00'
    x = pd.date_range(d, periods=96, freq='15min')

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

#easier code to create a circle
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def moveMapInDirection(xMove, yMove):
    canvasCoords[0] += xMove
    canvasCoords[1] += yMove 
    #check for bounds of map so the map doesn't move too far

def mapMovement(speed):
    xMove = 0
    yMove = 0 
    if root.winfo_pointerx()  < 100 : xMove = speed
    if root.winfo_pointerx() > 1000 : xMove = -speed
    if root.winfo_pointery() < 100 : yMove = speed
    if root.winfo_pointery()  > 500 : yMove = -speed
    moveMapInDirection(xMove, yMove)

def mousePress(canvas, root, objectList, event):
    print(str(event.x) + ", " + str(event.y)) 
    
def mouseDrag(root, e) :  
    abs_coord_x = root.winfo_pointerx() 
    abs_coord_y = root.winfo_pointery() 
    canvas.place(x=abs_coord_x - coordsOnClick[0] , y=abs_coord_y - coordsOnClick[1] )

def mouseRelease(e): 
    canvasCoords[0] = e.x - coordsOnClick[0]
    canvasCoords[1] = e.y - coordsOnClick[1]
    canvasCoordsMove[0] = 0
    canvasCoordsMove[1] = 0

def main(): 


    center = [-0.023559, 37.9061928]
    map_kenya = folium.Map(location=center, zoom_start=8)
    #display map
    map_kenya
    return
    objectList = []
    img1 = canvas.create_rectangle(50, 50, 50, 50, fill="red", outline = 'blue') 
    img = tk.PhotoImage(file="images/mapFull.png")      #load image
    mapImg = canvas.create_image(20,20, anchor=tk.NW, image=img) #create image on canvas
    objectList.append(mapImg) 
    objectList.append(img1) 
    canvas.bind("<Button-1>", lambda e: mousePress(canvas, root, objectList, e)) 
    #canvas.bind("<B1-Motion>", lambda e: mouseDrag(root, e)) 
    #canvas.bind("<ButtonRelease-1>", mouseRelease) 

    for site in sites: 
        canvas.create_circle(site[2], site[3], 5, fill='red', outline='blue', width=2) 
    
    canvas.pack()

    while True:  
        #canvasCoords[0] = (canvasCoordsGoto[0] - canvasCoords[0])/100
        #canvasCoords[1] = (canvasCoordsGoto[1] - canvasCoords[1])/100 
        mapMovement(10)
        canvas.place(x=canvasCoords[0], y=canvasCoords[1])
        root.update()
    #root.mainloop()  
    """ 
    lstm = load_model('model/lstm.h5')
    gru = load_model('model/gru.h5')
    saes = load_model('model/saes.h5')
    models = [lstm, gru, saes]
    names = ['LSTM', 'GRU', 'SAEs']

    lag = 12
    file1 = 'data/train.csv'
    file2 = 'data/test.csv'
    _, _, X_test, y_test, scaler = process_data(file1, file2, lag)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

    y_preds = []
    for name, model in zip(names, models):
        if name == 'SAEs':
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))
        else:
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        file = 'images/' + name + '.png'
        plot_model(model, to_file=file, show_shapes=True)
        predicted = model.predict(X_test)
        predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
        y_preds.append(predicted[:96])
        print(name)
        eva_regress(y_test, predicted)

    plot_results(y_test[: 96], y_preds, names)
    """


if __name__ == '__main__':
    main()
