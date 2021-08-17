import datetime
import gc
from pandas_datareader import data
import pandas as pd
import ta
import send_slack_msg as ssm
import putenv


class StockMonitor:
    def __init__(self, ticker, sma):
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=200)
        self.df_stock = data.DataReader(ticker, 'yahoo', self.start_date, self.end_date)
        self.df_stock['SMA'] = ta.trend.SMAIndicator(close=self.df_stock['Adj Close'], window=sma).sma_indicator()
        self.df_stock = self.df_stock[['Adj Close', 'SMA']].dropna()

    # Returns True/False if the stock price has exceeded the sma since yesterday (from under to above)
    def get_exceeded_sma(self):
        condition_past_days = (self.df_stock.iloc[-3]['Adj Close'] < self.df_stock.iloc[-3]['SMA'])
        condition_today = (self.df_stock.iloc[-1]['Adj Close'] > self.df_stock.iloc[-1]['SMA'])
        return (condition_past_days and condition_today)


if __name__ == "__main__":
    PATH_MONITORING = putenv.os.getenv('FILE_PATH_MONITORING')
    PATH_OWNING = putenv.os.getenv('FILE_PATH_OWNING')
    df_monitor = pd.read_excel(PATH_MONITORING)
    df_owning = pd.read_excel(PATH_OWNING)
    df_monitor = pd.concat([df_monitor, df_owning]).drop_duplicates(keep=False)
    
    # Loop through monitored stocks that is not owned from before and see if they have exceeded their given sma
    exceeded_stocks = []
    for index, row in df_monitor.iterrows():
        monitor = StockMonitor(row['TICKER'], row['SMA Length'])
        
        if (monitor.get_exceeded_sma()):
            exceeded_stocks.append(row['TICKER'])
        
        del monitor
        gc.collect()

    # Send Slack msg
    message = 'BUY SIGNAL:\n\n'
    for stock in exceeded_stocks:
        message += (stock + ' is above its SMA\n') 
    
    if (message != 'BUY SIGNAL:\n\n'):
        ssm.send_slack_message(message)
    
    ssm.send_slack_message('IT WORKED: DELETE THIS LINE')

    