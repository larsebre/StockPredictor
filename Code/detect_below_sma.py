import datetime
import gc
from pandas_datareader import data
import yfinance as yf
import pandas as pd
import ta
import os
from slack import WebClienttou


class StockMonitor:
    def __init__(self, ticker, sma):
        self.ticker = ticker
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=300)
        self.df_stock = data.DataReader(self.ticker, 'yahoo', self.start_date, self.end_date)
        self.df_stock['SMA'] = ta.trend.SMAIndicator(close=self.df_stock['Adj Close'], window=sma).sma_indicator()
        self.sma = self.df_stock[['SMA']].dropna()

    def get_under_sma(self):
        latest_sma = self.sma.iloc[-1]['SMA']
        stock_data = yf.download(tickers=self.ticker, period='1t', interval='1m')
        latest_price = stock_data.iloc[-1]['Close']
        return (latest_price < latest_sma)


if __name__ == "__main__":
    df_owning = pd.read_excel('owning_stocks.xlsx')
    
    # Loop through owned stocks to see if they are below their sma
    below_stocks = []
    for index, row in df_owning.iterrows():
        monitor = StockMonitor(row['TICKER'], row['SMA Length'])
        
        if (monitor.get_under_sma()):
            below_stocks.append(row['TICKER'])
        
        del monitor
        gc.collect()

    print(below_stocks)
