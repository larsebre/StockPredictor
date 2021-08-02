import datetime
import numpy as np
from pandas_datareader import data
import pandas as pd
import ta


class StockData:
    def __init__(self, ticker, data_days, forecast):
        self.TICKER = ticker
        self.days_forecast = forecast
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=data_days)
        self.df_x_data = pd.DataFrame()
        self.df_y_data = pd.DataFrame()
        self.df_dow_jones = data.DataReader('^DJI', 'yahoo', self.start_date, self.end_date)
        self.df_SP500 = data.DataReader('^GSPC', 'yahoo', self.start_date, self.end_date)
        self.num_prediction_inputs = 3
        self.prediction_inputs = pd.DataFrame()

    def set_stock_data(self):
        self.df_x_data = data.DataReader(self.TICKER, 'yahoo', self.start_date, self.end_date)

    def calculate_technical_indicators(self):
        self.df_x_data = ta.utils.dropna(self.df_x_data)
        self.df_x_data['MFI'] = ta.volume.MFIIndicator(high=self.df_x_data['High'], low=self.df_x_data['Low'], close=self.df_x_data['Close'], volume=self.df_x_data['Volume']).money_flow_index()
        self.df_x_data['ADI'] = ta.volume.AccDistIndexIndicator(high=self.df_x_data['High'], low=self.df_x_data['Low'], close=self.df_x_data['Close'], volume=self.df_x_data['Volume']).acc_dist_index() 
        self.df_x_data['SMA20'] = ta.trend.SMAIndicator(close=self.df_x_data['Close'], window=20).sma_indicator()
        self.df_x_data['CCI20'] = ta.trend.CCIIndicator(high=self.df_x_data['High'], low=self.df_x_data['Low'], close=self.df_x_data['Close'], window=20, constant=0.015).cci()
        self.df_x_data['MACD'] = ta.trend.MACD(close=self.df_x_data['Close']).macd()
        self.df_x_data['RSI'] = ta.momentum.RSIIndicator(close=self.df_x_data['Close']).rsi()
        self.df_x_data['DOW JONES Close'] = self.df_dow_jones['Close']
        self.df_x_data['DOW JONES SMA20'] = ta.trend.SMAIndicator(close=self.df_dow_jones['Close'], window=20).sma_indicator()
        self.df_x_data['S&P 500 Close'] = self.df_SP500['Close']
        self.df_x_data['DOW JONES SMA20'] = ta.trend.SMAIndicator(close=self.df_SP500['Close'], window=20).sma_indicator()
        self.df_x_data = self.df_x_data[['Close', 'ADI', 'MFI', 'SMA20', 'CCI20', 'MACD', 'RSI', 'DOW JONES Close', 'DOW JONES SMA20', 'S&P 500 Close', 'DOW JONES SMA20']]

    #Used to predict 
    def set_prediction_inputs(self):
        self.prediction_inputs = self.df_x_data.tail(self.num_prediction_inputs)

    #Adding the Price Change n traiding days ahead
    def calculate_price_change(self):
        self.df_x_data['Price Change'] = -self.df_x_data['Close'].diff(periods=-self.days_forecast)
        self.df_x_data['Price Change'] = self.df_x_data['Price Change']/self.df_x_data['Close']
        self.df_x_data = self.df_x_data.dropna()
    
    def split_data_to_x_and_y(self):
        self.df_y_data = self.df_x_data[['Price Change']]
        self.df_x_data.drop(columns='Price Change', inplace=True)
    
    #Returns a numpy array to be used for training
    def get_X_data(self):
        self.df_x_data = self.df_x_data.append(self.prediction_inputs)
        return self.df_x_data.to_numpy()

    #Returns a numpy array of 0,1,2 depending on the 'Price Change': 
    #0 -> Price Change < 0.05, 1 -> 0.05 <= Price Change
    def get_Y_data(self):
        classes = []
        for change in self.df_y_data[['Price Change']].to_numpy():
            if (change[0] < 0.1):
                classes.append(0)
            elif (change[0] >= 0.1):
                classes.append(1)
        return np.array(classes)
    
    def initialize(self):
        self.set_stock_data()
        self.calculate_technical_indicators()
        self.set_prediction_inputs()
        self.calculate_price_change()
        self.split_data_to_x_and_y()

if __name__ == "__main__":
    stock_data = StockData('KOA.OL', data_days=365, forecast=20)
    stock_data.initialize()
    stock_data.get_X_data()
    print(stock_data.get_Y_data())
