import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import datetime
import ta
import plotly.graph_objects as go

if __name__ == "__main__":

    df_monitor = pd.read_excel('monitor_these_stocks.xlsx')

    # Change this if you want to plot single stock
    plot_monitored_stocks = False 
    # Change ticker and sma to get the right plot
    ticker = ['VOLUE.OL']
    sma = [10]

    if (plot_monitored_stocks):
        ticker = df_monitor['TICKER'].to_list()
        sma = df_monitor['SMA Length'].to_list()

    for i in range(len(ticker)):
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=20*sma[i])
        df_stock = data.DataReader(ticker[i], 'yahoo', start_date, end_date)
        df_stock['SMA'] = ta.trend.SMAIndicator(close=df_stock['Adj Close'], window=sma[i]).sma_indicator()
        df_stock = df_stock.dropna()

        fig = go.Figure(data=[go.Candlestick(x=df_stock.index,
                    open=df_stock['Open'], high=df_stock['High'],
                    low=df_stock['Low'], close=df_stock['Adj Close'])])

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.add_trace(go.Scatter(x=df_stock.index, y=df_stock['SMA'], name='SMA',
                            line=dict(color='blue', width=4)))

        fig.update_layout(title= ticker[i] + ' SMA' + str(sma[i]),
                    xaxis_title='Days',
                    yaxis_title='Price')
        fig.show()