import datetime
import numpy as np
from pandas_datareader import data
import pandas as pd
import ta


class StockData:
    def __init__(self, ticker, forecast, start_date, end_date):
        self.TICKER = ticker
        self.days_forecast = forecast
        self.start_date = start_date
        self.end_date = end_date
        self.df_x_data = pd.DataFrame()
        self.df_y_data = pd.DataFrame()
        self.num_prediction_inputs = 3
        self.prediction_inputs = pd.DataFrame()
    
    def add_stock_index_data(self, DOW_JONES, SP500):
        self.df_dow_jones = DOW_JONES
        self.df_SP500 = SP500

    def set_stock_data(self):
        self.df_x_data = data.DataReader(self.TICKER, 'yahoo', self.start_date, self.end_date)

    def calculate_technical_indicators(self):
        self.df_x_data = ta.utils.dropna(self.df_x_data)
        self.df_x_data['SMA30'] = ta.trend.SMAIndicator(close=self.df_x_data['Adj Close'], window=30).sma_indicator()
        self.df_x_data['SMA30 PREV 1 WEEK'] = self.df_x_data['SMA30'].shift(periods=5)
        self.df_x_data['SMA30 PREV 2 WEEK'] = self.df_x_data['SMA30'].shift(periods=10)
        self.df_x_data['SMA30 PREV 3 WEEK'] = self.df_x_data['SMA30'].shift(periods=15)
        self.df_x_data['SMA30 PREV 4 WEEK'] = self.df_x_data['SMA30'].shift(periods=20)
        self.df_x_data['Adj Close PREV 1 WEEK'] = self.df_x_data['Adj Close'].shift(periods=5)
        self.df_x_data['Adj Close PREV 2 WEEK'] = self.df_x_data['Adj Close'].shift(periods=10)
        self.df_x_data['Adj Close PREV 3 WEEK'] = self.df_x_data['Adj Close'].shift(periods=15)
        self.df_x_data['Adj Close PREV 4 WEEK'] = self.df_x_data['Adj Close'].shift(periods=20)
        self.df_x_data['MACD'] = ta.trend.MACD(close=self.df_x_data['Adj Close']).macd()
        self.df_x_data['MACD PREV 1 WEEK'] = self.df_x_data['MACD'].shift(periods=5)
        self.df_x_data['MACD PREV 2 WEEK'] = self.df_x_data['MACD'].shift(periods=10)
        self.df_x_data['MACD PREV 3 WEEK'] = self.df_x_data['MACD'].shift(periods=15)
        self.df_x_data['MACD PREV 4 WEEK'] = self.df_x_data['MACD'].shift(periods=20)
        self.df_x_data['DOW JONES Close'] = self.df_dow_jones['Adj Close']
        self.df_x_data['DOW JONES SMA30'] = ta.trend.SMAIndicator(close=self.df_dow_jones['Adj Close'], window=30).sma_indicator()
        self.df_x_data['S&P 500 Close'] = self.df_SP500['Adj Close']
        self.df_x_data['S&P 500 SMA30'] = ta.trend.SMAIndicator(close=self.df_SP500['Adj Close'], window=30).sma_indicator()

        # Make new data frame for analysis
        self.df_x_data = self.df_x_data[[   'Adj Close', 'Adj Close PREV 1 WEEK', 'Adj Close PREV 2 WEEK', 'Adj Close PREV 3 WEEK', 'Adj Close PREV 4 WEEK',
                                            'SMA30', 'SMA30 PREV 1 WEEK', 'SMA30 PREV 2 WEEK', 'SMA30 PREV 3 WEEK', 'SMA30 PREV 4 WEEK', 
                                            'MACD', 'MACD PREV 1 WEEK', 'MACD PREV 2 WEEK', 'MACD PREV 3 WEEK', 'MACD PREV 4 WEEK', 
                                            'DOW JONES Close', 'DOW JONES SMA30', 
                                            'S&P 500 Close', 'DOW JONES SMA30']]
        self.df_x_data = self.df_x_data.dropna()

    #Used to predict 
    def set_prediction_inputs(self):
        self.prediction_inputs = self.df_x_data.tail(self.num_prediction_inputs)

    #Adding the Price Change n traiding days ahead
    def calculate_price_change(self):
        self.df_x_data['Price Change'] = -self.df_x_data['Adj Close'].diff(periods=-self.days_forecast)
        self.df_x_data['Price Change'] = self.df_x_data['Price Change']/self.df_x_data['Adj Close']
        self.df_x_data = self.df_x_data.dropna()
    
    def split_data_to_x_and_y(self):
        self.df_y_data = self.df_x_data[['Price Change']]
        self.df_x_data.drop(columns='Price Change', inplace=True)
    
    #Returns a numpy array to be used for training and predictions
    def get_X_data(self):
        return self.df_x_data.append(self.prediction_inputs).to_numpy()

    #Returns a numpy array of 0,1,2 depending on the 'Price Change': 
    #0 -> Price Change < 0.05, 1 -> 0.05 <= Price Change
    def get_Y_data(self, price_change):
        classes = []
        for change in self.df_y_data[['Price Change']].to_numpy():
            if (change[0] < price_change):
                classes.append(0)
            elif (change[0] >= price_change):
                classes.append(1)
        return np.array(classes)
    
    def initialize(self):
        self.set_stock_data()
        self.calculate_technical_indicators()
        self.set_prediction_inputs()
        self.calculate_price_change()
        self.split_data_to_x_and_y()

if __name__ == "__main__":
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=500)

    stock_data = StockData('KOA.OL', forecast=20, start_date=start_date, end_date=end_date)
    stock_data.initialize()
    stock_data.get_X_data()
    print(stock_data.get_Y_data())
