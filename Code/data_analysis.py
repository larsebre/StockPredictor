import datetime
import get_stock_data as gsd
import matplotlib.pyplot as plt
import pandas as pd
import ta
from pandas_datareader import data

class DataAnalysis: 
    
    def __init__(self, ticker, days_forecast, start_date, end_date):
        self.TICKER = ticker
        self.days_forecast = days_forecast
        self.start_date = start_date
        self.end_date = end_date
        self.TI = pd.DataFrame()
        self.TI_past_day = pd.DataFrame()
        self.price_data = pd.DataFrame()

    def generate_data(self):
        self.TI = data.DataReader(self.TICKER, 'yahoo', self.start_date, self.end_date)
        self.TI = ta.utils.dropna(self.TI)
        self.TI['SMA30'] = ta.trend.SMAIndicator(close=self.TI['Adj Close'], window=20).sma_indicator()
        
        mask = (self.TI.index >= (self.end_date  - datetime.timedelta(days=90)))
        self.price_data = self.TI[['Adj Close', 'SMA30']][mask]
        
        self.TI['MFI'] = ta.volume.MFIIndicator(high=self.TI['High'], low=self.TI['Low'], close=self.TI['Adj Close'], volume=self.TI['Volume']).money_flow_index()
        self.TI['ADI'] = ta.volume.AccDistIndexIndicator(high=self.TI['High'], low=self.TI['Low'], close=self.TI['Adj Close'], volume=self.TI['Volume']).acc_dist_index() 
        self.TI['RSI'] = ta.momentum.RSIIndicator(close=self.TI['Adj Close']).rsi()
        self.TI['CCI'] = ta.trend.CCIIndicator(high=self.TI['High'], low=self.TI['Low'], close=self.TI['Close']).cci()
        self.TI_past_day = self.TI.tail(1)
        self.TI = self.TI.dropna()

        self.TI['Price Change'] = -self.TI['Adj Close'].diff(periods=-self.days_forecast)
        self.TI['Price Change'] = self.TI['Price Change']/self.TI['Adj Close']
        self.TI = self.TI.dropna()
        self.TI = self.TI[['MFI', 'ADI', 'RSI', 'CCI', 'Price Change']]

    def plot_data(self, TI):
        fig, axs = plt.subplots(3)
        fig.suptitle(self.TICKER)
        
        axs[0].plot(self.price_data)
        axs[0].legend(['Price', 'SMA30'])

        min = self.TI[TI].min()
        max = self.TI[TI].max()
        val_range = (max - min)
        
        axs[1].scatter(self.TI[TI], self.TI['Price Change'])
        axs[1].vlines(self.TI_past_day[TI], self.TI['Price Change'].min(), self.TI['Price Change'].max(), colors='r', linestyles='solid')
        axs[1].vlines(self.TI_past_day[TI] + val_range*0.025, self.TI['Price Change'].min(), self.TI['Price Change'].max(), colors='r', linestyles='dashed')
        axs[1].vlines(self.TI_past_day[TI] - val_range*0.025, self.TI['Price Change'].min(), self.TI['Price Change'].max(), colors='r', linestyles='dashed')
        axs[1].hlines(0, min, max, colors='grey', linestyles='dashed', label= TI + ' now')
        axs[1].set_title('Price Change vs ' + TI)

        mask = (self.TI[TI] >= (self.TI_past_day[TI].mean() - val_range*0.025))
        TI_hist = self.TI[mask]
        mask = (self.TI[TI] <= (self.TI_past_day[TI].mean() + val_range*0.025))
        TI_hist = TI_hist[mask]
        axs[2].hist(TI_hist[['Price Change']])

if __name__ == "__main__":
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1000)

    analyst = DataAnalysis('EQNR.OL', days_forecast=20, start_date=start_date, end_date=end_date)
    analyst.generate_data()
    analyst.plot_data('ADI')
    plt.show()
    
