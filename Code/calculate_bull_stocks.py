import datetime
import get_stock_data as gsd
import gc
import numpy as np
from pandas_datareader import data
import pandas as pd
import svm_predictor


if __name__ == "__main__":

    path = 'TICKERS.xlsx'
    ticker_list = pd.read_excel('TICKERS.xlsx')['TICKER'].values.tolist()
    bull_stocks = {}

    predictor = svm_predictor.SVMPredictor()
    
    # Market indeces to be used for all stocks data
    end_date = datetime.datetime.now() #- datetime.timedelta(days=30)
    start_date = end_date - datetime.timedelta(days=600)
    print(start_date)
    print(end_date)
    df_dow_jones = data.DataReader('^DJI', 'yahoo', start_date, end_date)
    df_SP500 = data.DataReader('^GSPC', 'yahoo', start_date, end_date)

    num_stocks = len(ticker_list)
    i = 1
    for ticker in ticker_list:
        if (path == 'TICKERS.xlsx'):     
            ticker = ticker + '.OL'
        
        try: 
            # Initialize the new StockData class for the specific ticker
            predictor.stock_data = gsd.StockData(ticker, forecast=20, start_date=start_date, end_date=end_date)
            predictor.stock_data.add_stock_index_data(df_dow_jones, df_SP500)
            predictor.stock_data.initialize()

            # Train, validate model and predict feature price change
            predictor.generate_model_data(price_change=0.05)
            predictor.train_and_validate_model()
            predictions = predictor.get_predicted_price_class()

            # Check if we predict three 5% from the last three days.
            if (np.sum(predictions) == 3):
                bull_stocks[ticker] = 0.05

                predictor.generate_model_data(price_change=0.10)
                predictor.train_and_validate_model()
                predictions = predictor.get_predicted_price_class()

                if (np.sum(predictions) == 3):
                    bull_stocks[ticker] = 0.10
            
            del predictor.stock_data
            gc.collect()
            print('Finished calculating ' + ticker + ': ' + str(i) + ' of ' + str(num_stocks) + ' stocks')
        
        except:
            print('ERROR: Could not calculate for ' + ticker)
        
        i = i + 1
    print(bull_stocks)
    