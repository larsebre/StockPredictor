import datetime
import gc
from pandas_datareader import data
import pandas as pd
import ta


class StockMonitor:
    def __init__(self, ticker, sma):
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=200)
        self.df_stock = data.DataReader(ticker, 'yahoo', self.start_date, self.end_date)
        self.df_stock['SMA'] = ta.trend.SMAIndicator(close=self.df_stock['Adj Close'], window=sma).sma_indicator()
        self.df_stock = self.df_stock[['Adj Close', 'SMA']].dropna()

    # Returns True/False if the stock price has exceeded the sma since yesterday (from under to above)
    def get_exceeded_sma(self):
        condition_past_week = (self.df_stock.iloc[-7]['Adj Close'] < self.df_stock.iloc[-7]['SMA'])
        condition_today = (self.df_stock.iloc[-1]['Adj Close'] > self.df_stock.iloc[-1]['SMA'])
        return (condition_past_week and condition_today)


if __name__ == "__main__":
    df_monitor = pd.read_excel('monitor_these_stocks.xlsx')
    df_owning = pd.read_excel('owning_stocks.xlsx')
    df_monitor = pd.concat([df_monitor, df_owning]).drop_duplicates(keep=False)
    
    # Loop through monitored stocks that is not owned from before and see if they have exceeded their given sma
    exceeded_stocks = []
    for index, row in df_monitor.iterrows():
        monitor = StockMonitor(row['TICKER'], row['SMA Length'])
        
        if (monitor.get_exceeded_sma()):
            exceeded_stocks.append(row['TICKER'])
        
        del monitor
        gc.collect()

    print(exceeded_stocks)

    