# StockPredictor
This is a short docs for the different main files that I have made.

## calculate_bull_stocks.py
Loops through all the tickers in "TICKERS.xlxs" that I have stored on my local computer. For every ticker it trains the SVMPredictor() on historical data (Technical Indicators), use a validation set to validate if its performance is good enough, and if the performance is good enough it produce a prediction of the price change the next month. The prediction is a price change classification: Class 1: price < 5%, Class 2: 5% <= price < 10%, Class 3: 10% <= price. These classifications are stored in suggested_stocks.xlsx.

## optimize_portfolio.py
Define the stocks in the portfolio and their corresponding expected return. Then it calculates a coovariance matrix for the stocks.
It does 10 000 iterations where a random portfolio weighting (sum(weights) == 1) is chosen for every iteration. For this random weighting it calculates the risk of the portfolio. After the 10 000 iterations it plots the risk in a scatter plot where you can see the Efficient frontier. It also print the minimum risk portfolio.
I tried in the start to use an SQP algorithm to minimice the risk subject to a given expected return, but did not get the algorithm to converge properly. Therefore I used the brute force method (got it from https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/)
.<img width="1264" alt="Skjermbilde 2021-08-21 kl  11 07 02" src="https://user-images.githubusercontent.com/59867535/130316891-f4bc3573-283d-4351-b8e9-91bbc9104b3f.png">

## optimize_sma_indicator.py
Loops through every ticker in TICKERS.xlsx and reads the stock price data 700 days back in time. Here it loops through and calculates the Simple Moving Aveage(SMA) from SMA10 to SMA200. For every SMA it simulates the return we would get if we bought the stock when the price exceeds the SMA and sell when the price goes lower than the SMA. This simulation use data from the last 465 days. For every stock, we now have stored the SMA X that gives the highest return for this trading strategy. The results are stored in sma_trading_stocks.xlsx together with the number of trades, average return and "Trading Score". The "Trading Score" is (Return with strategy/ Return from just owning the stock). This means that if the "Trading Score" is more than 1 for a stock, the trading strategy has outperformed the return of just owning the stock without buying or selling. The Excel file sma_trading_stocks.xlsx can be used to find the best stocks to trade with SMA<img width="1279" alt="Skjermbilde 2021-08-21 kl  11 38 49" src="https://user-images.githubusercontent.com/59867535/130317763-ab416c96-5e66-4add-b3ae-6696cc53e083.png">

## detect_above_sma.py
Reads from the Excel file "monitored_stocks.xlsx" (path hidden with environmental variable), where the most interesting trading stocks are stored together with their optimal SMA. The python file loops through these stocks and detects if the price has exceeded the SMA the past 3 days. If so, it alerts me on Slack what stocks have exceeded. This is nice to know as soon as possible since it is a buy signal for the trading strategy.

## detect_below_sma.py
This file does the same thing as "detect_above_sma.py", but detects when a stock price goes under the optimal SMA. This signals a sell signal. It monitores just the stocks that I own my self. I am alerted on Slack if this happens.<img width="731" alt="Skjermbilde 2021-08-21 kl  11 48 58" src="https://user-images.githubusercontent.com/59867535/130318064-f10c8635-fbc1-40bc-924d-60f01a2154ae.png">
