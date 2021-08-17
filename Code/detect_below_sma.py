import datetime
import gc
from pandas_datareader import data
import yfinance as yf
import pandas as pd
import ta
import send_slack_msg as ssm
import putenv


class StockMonitor:
    def __init__(self, ticker, sma):
        self.ticker = ticker
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=300)
        self.df_stock = data.DataReader(self.ticker, 'yahoo', self.start_date, self.end_date)
        self.df_stock['SMA'] = ta.trend.SMAIndicator(close=self.df_stock['Adj Close'], window=sma).sma_indicator()
        self.sma = self.df_stock[['SMA']].dropna()
        self.latest_price = None
        self.latest_sma = None

    def get_under_sma(self):
        self.latest_sma = self.sma.iloc[-1]['SMA']
        stock_data = yf.download(tickers=self.ticker, period='1t', interval='1m')
        self.latest_price = stock_data.iloc[-1]['Close']
        return (self.latest_price < self.latest_sma)


if __name__ == "__main__":
    PATH = putenv.os.getenv('FILE_PATH')
    df_owning = pd.read_excel(PATH)
    
    # Loop through owned stocks to see if they are below their sma
    message = 'SELL SIGNAL:\n\n'
    for index, row in df_owning.iterrows():
        monitor = StockMonitor(row['TICKER'], row['SMA Length'])
        
        if (monitor.get_under_sma()):
            message += (row['TICKER'] + ' is under SMA' + str(row['SMA Length']) + ' (' + str(round(monitor.latest_price, 2)) + ' < ' + str(round(monitor.latest_sma, 2)) + ')\n')
        
        del monitor
        gc.collect()

    if (message != 'SELL SIGNAL:\n\n'):
        ssm.send_slack_message(message)
