from pandas_datareader import data
import pandas as pd
import ta
import datetime


class StockData:
    def __init__(self, ticker, data_days, forecast):
        self.TICKER = ticker
        self.days_forecast = forecast
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=data_days)
        self.df_data = pd.DataFrame()
        self.prediction_input = pd.DataFrame()

    def set_stock_data(self):
        self.df_data = data.DataReader(self.TICKER, 'yahoo', self.start_date, self.end_date)

    def calculate_technical_indicators(self):
        self.df_data = ta.utils.dropna(self.df_data)
        self.df_data['MFI'] = ta.volume.MFIIndicator(high=self.df_data['High'], low=self.df_data['Low'], close=self.df_data['Close'], volume=self.df_data['Volume']).money_flow_index()
        self.df_data['ADI'] = ta.volume.AccDistIndexIndicator(high=self.df_data['High'], low=self.df_data['Low'], close=self.df_data['Close'], volume=self.df_data['Volume']).acc_dist_index() 
        self.df_data['SMA20'] = ta.trend.SMAIndicator(close=self.df_data['Close'], window=20).sma_indicator()
        self.df_data['CCI20'] = ta.trend.CCIIndicator(high=self.df_data['High'], low=self.df_data['Low'], close=self.df_data['Close'], window=20, constant=0.015).cci()
        self.df_data['RSI'] = ta.momentum.RSIIndicator(close=self.df_data['Close']).rsi()
        self.df_data = self.df_data[['Close', 'ADI', 'MFI', 'SMA20', 'CCI20', 'RSI']]

    #Used to predict 
    def set_last_day_data(self):
        self.prediction_input = self.df_data.tail(1)

    #Adding the Price Change n traiding days ahead
    def calculate_price_change(self):
        self.df_data['Price Change'] = -self.df_data['Close'].diff(periods=-self.days_forecast)
        self.df_data['Price Change'] = self.df_data['Price Change']/self.df_data['Close']
        self.df_data = self.df_data.dropna()
    
    def initialize(self):
        self.set_stock_data()
        self.calculate_technical_indicators()
        self.set_last_day_data()
        self.calculate_price_change()

if __name__ == "__main__":
    stock_data = StockData('NEL.OL', data_days=365, forecast=20)
    stock_data.initialize()
    print(stock_data.df_data)
