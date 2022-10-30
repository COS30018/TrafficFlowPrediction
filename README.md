# COS30018 - Option A Topic 3

- Harrison Sheppard - 101613496 
- Duy Anh Vuong - 102603197 
- Christian De Groot - 102106227
- Nelson Hain - 101533031 

## Traffic Flow Prediction
Traffic Flow Prediction with Neural Networks (SAEs, LSTM, GRU, RNN).


## Requirement
```
pip install -r requirements.txt
```

## Train the model

```
python train.py --model model_name
```

You can choose "lstm", "gru", "saes", or "rnn" as arguments. The ```.h5``` weight file was saved at model folder.

Models included in the repo have been trained on 100 epochs.
Seperate models have been trained for each SCATS site

## Generate evaluations
```
python main.py
```

## Use the GUI
```
python gui.py
```
