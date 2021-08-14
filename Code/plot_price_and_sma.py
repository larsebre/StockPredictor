import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
import datetime
import ta
import plotly.graph_objects as go

if __name__ == "__main__":

    ticker = 'SASNO.OL'
    sma = 10

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=20*sma)
    df_stock = data.DataReader(ticker, 'yahoo', start_date, end_date)
    df_stock['SMA'] = ta.trend.SMAIndicator(close=df_stock['Adj Close'], window=sma).sma_indicator()
    df_stock = df_stock.dropna()

    fig = go.Figure(data=[go.Candlestick(x=df_stock.index,
                open=df_stock['Open'], high=df_stock['High'],
                low=df_stock['Low'], close=df_stock['Adj Close'])
                     ])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.add_trace(go.Scatter(x=df_stock.index, y=df_stock['SMA'], name='SMA',
                         line=dict(color='blue', width=4)))

    fig.update_layout(title= ticker + ' SMA' + str(sma),
                   xaxis_title='Days',
                   yaxis_title='Price')
    fig.show()