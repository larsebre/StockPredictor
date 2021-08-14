import datetime
import numpy as np
import gc
from pandas_datareader import data
import pandas as pd
import ta


if __name__ == "__main__":

    path = 'TICKERS.xlsx'
    ticker_list = pd.read_excel('TICKERS.xlsx')['TICKER'].values.tolist()
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=700)
    filter_date_start = end_date - datetime.timedelta(days=465)

    df_stocks_best_sma = pd.DataFrame({ 'TICKER' : [], 
                                        'SMA Length' : [],
                                        'Trading Score' : [], 
                                        'Return' : [], 
                                        'Number of Trades' : [], 
                                        'Number of Winning Trades' : [], 
                                        'Average Winning Trade' : [],
                                        'Average Loosing Trade' : []})

    #Loop through stocks in 'TICKERS.xlsx'
    stock_i = 0
    for ticker in ticker_list:
        try:
            # Get Stock data
            ticker = ticker + '.OL'
            df = data.DataReader(ticker, 'yahoo', start_date, end_date)
            df = ta.utils.dropna(df) 
            
            df_returns = pd.DataFrame({ 'SMA Length' : [],
                                        'Trading Score' : [], 
                                        'Return' : [], 
                                        'Number of Trades' : [], 
                                        'Number of Winning Trades' : [], 
                                        'Average Winning Trade' : [],
                                        'Average Loosing Trade' : []})
            winning_trades = []
            loosing_trades = []
            
            # Loop through SMA lengths and calculate return 
            for sma_length in range(10, 201):
                df['SMA'] = ta.trend.SMAIndicator(close=df['Adj Close'], window=sma_length).sma_indicator()
                df_compare = df[['Adj Close', 'SMA']].dropna()
                df_compare = df_compare[df_compare.index >= filter_date_start]

                start_price_i = df_compare.iloc[0]['Adj Close']
                sma_i = df_compare.iloc[0]['SMA']
                above_sma = (start_price_i > sma_i)
                stock_return = 1
                num_increases = 0
                num_trades = 0

                # Simulate return: Buy when price goes over sma and sell when it goes under
                for index, row in df_compare.iterrows():
                    if (row['Adj Close'] > row['SMA']):
                        if (above_sma == False):
                            start_price_i = row['Adj Close']
                        above_sma = True
                    else:
                        if (above_sma == True):
                            gain = row['Adj Close']/start_price_i
                            stock_return *= gain
                            if (gain > 1.0):
                                num_increases += 1
                                winning_trades.append(gain)
                            else:
                                loosing_trades.append(gain)
                            num_trades += 1
                        above_sma = False
                if (num_trades == 0):
                    earning_percentage = None
                else:
                    earning_percentage = num_increases/num_trades
                
                df_returns = df_returns.append({    'SMA Length' : sma_length,
                                                    'Trading Score' : stock_return/(df_compare.iloc[-1]['Adj Close']/df_compare.iloc[0]['Adj Close']) ,
                                                    'Return' : stock_return, 
                                                    'Number of Trades' : num_trades, 
                                                    'Number of Winning Trades' : earning_percentage, 
                                                    'Average Winning Trade' : np.average(np.array(winning_trades)),
                                                    'Average Loosing Trade' : np.average(np.array(loosing_trades))}, ignore_index=True)

            df_returns = df_returns.dropna()
            best_sma = df_returns[df_returns['Return'] == df_returns['Return'].max()]
            df_stocks_best_sma = df_stocks_best_sma.append({    'TICKER' : ticker, 
                                                                'SMA Length' : best_sma.iloc[0]['SMA Length'],
                                                                'Trading Score' : best_sma.iloc[0]['Trading Score'],
                                                                'Return' : best_sma.iloc[0]['Return'], 
                                                                'Number of Trades' : best_sma.iloc[0]['Number of Trades'], 
                                                                'Number of Winning Trades' : best_sma.iloc[0]['Number of Winning Trades'], 
                                                                'Average Winning Trade' : best_sma.iloc[0]['Average Winning Trade'],
                                                                'Average Loosing Trade' : best_sma.iloc[0]['Average Loosing Trade']}, ignore_index=True)
            
            del df_returns
            gc.collect()
                                                                
            stock_i += 1
            print('SUCCESS: Finished calculating ' + ticker + ': ' + str(stock_i) + ' of ' + str(len(ticker_list)))
        except:
            stock_i += 1
            print('ERROR: Could not calculate for ' + ticker)

    df_stocks_best_sma = df_stocks_best_sma.sort_values(by=['Trading Score'], ascending=False)
    df_stocks_best_sma.to_excel('sma_trading_stocks.xlsx') 
    print(df_stocks_best_sma)       


