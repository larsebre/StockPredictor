# StockPredictor
This is a short docs for the different main files that I have made.

## calculate_bull_stocks.py
Loops through all the tickers in "TICKERS.xlxs" that I have stored on my local computer. For every ticker it trains the SVMPredictor() on historical data (Technical Indicators), use a validation set to validate if its performance is good enough, and if the performance is good enough it produce a prediction of the price change the next month. The prediction is a price change classification: Class 1: price < 5%, Class 2: 5% <= price < 10%, Class 3: 10% <= price. These classifications are stored in suggested_stocks.xlsx.

## optimize_portfolio.py
Define the stocks in the portfolio and their corresponding expected return. Then it calculates a coovariance matrix for the stocks.
It does 10 000 iterations where a random portfolio weighting (sum(weights) == 1) is chosen for every iteration. For this random weighting it calculates the risk of the portfolio. After the 10 000 iterations it plots the risk in a scatter where you can see the Efficient frontier. It also print the minimum risk portfolio.
I tried in the start to use an SQP algorithm to minimice the risk subject to a given expected return, but did not get the algorithm to converge properly. Therefore I used the brute force method (got it from https://www.machinelearningplus.com/machine-learning/portfolio-optimization-python-example/)
.<img width="1264" alt="Skjermbilde 2021-08-21 kl  11 07 02" src="https://user-images.githubusercontent.com/59867535/130316891-f4bc3573-283d-4351-b8e9-91bbc9104b3f.png">

