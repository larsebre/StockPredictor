import datetime
from pandas_datareader import data
import pandas as pd

df_stocks = pd.read_excel('suggested_stocks.xlsx')
tickers = df_stocks['TICKER'].tolist()
price_change = df_stocks['Price Change'].tolist()
prediction_dates = df_stocks['Prediction Date'].tolist()

true_price_change = []
correct_prediction = []

count_true_pred = 0
for i, ticker in enumerate(tickers):
    start_date = datetime.datetime.strptime(prediction_dates[i], '%Y-%m-%d')
    end_date = start_date + datetime.timedelta(days=30)
    df_data = data.DataReader(ticker, 'yahoo', start_date, end_date)
    price_list = df_data['Adj Close'].tolist()
    change = (price_list[-1] - price_list[0]) / price_list[0]
    true_price_change.append(change)
    correct_prediction.append((change > 0.0))
    if (change > 0.0):
        count_true_pred += 1
    print('Finished : ' + ticker)

df_compare = pd.DataFrame({ 'TICKER' : tickers,
                            'Predicted Price Change' : price_change,
                            'Correct Prediction' : correct_prediction,
                            'True Price Change' : true_price_change})

print('Prediction Score: ', count_true_pred/len(tickers))
print()
print(df_compare)