import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas_datareader import data
from scipy.optimize import minimize

def portfolio_variance(x, cov):

    decision_variables = len(x)
    sum = 0
    for i in range(decision_variables):
        for j in range(decision_variables):
            cov_ij = cov[i][j]
            sum += x[i]*x[j]*cov_ij     
    return sum

def expected_return(x, er):
    return np.dot(x, er)

if __name__ == "__main__":

    portfolio =     ['EQNR.OL', 'NEL.OL',   'YAR.OL',   'NHY.OL',   'SSG.OL']
    # Expected return single stock
    er = [0.05,       0.05,       0.05,       0.30,       0.10]
    # Expected portfolio return
    epf = 0.00

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=90)

    df = data.DataReader(portfolio, 'yahoo', start_date, end_date)
    df = df['Adj Close']

    cov_matrix = df.pct_change().apply(lambda x: np.log(1+x)).cov().to_numpy()

    # Find optimal portfolio with minimum variance
    portfolio_returns = []
    portfolio_volatility = []
    portfolio_weights = []

    num_assets = len(portfolio)
    num_portfolios = 10000

    # Simulate returns and volatility 10000 times for weights that add up to one and are positive
    for portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights = weights/np.sum(weights)
        portfolio_weights.append(weights)
        returns = expected_return(weights, er)
        portfolio_returns.append(returns)
        var = portfolio_variance(weights, cov_matrix)
        daily_std = np.sqrt(var)
        trading_days_month = 20
        monthly_std = daily_std*np.sqrt(trading_days_month) 
        portfolio_volatility.append(monthly_std)
   
    data = {'Returns' : portfolio_returns, 'Volatility' : portfolio_volatility}

    for counter, symbol in enumerate(df.columns.tolist()):
        data[symbol+' weight'] = [w[counter] for w in portfolio_weights]
    portfolios  = pd.DataFrame(data)
    
    # The portfolio with minimum variance
    min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
    print(min_vol_port)

    # The portfolio with highest sharp ratio
    rf = 0.01 # risk factor
    optimal_risk_portfolio = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
    print(optimal_risk_portfolio)

    # Plott portfolio simulation
    plt.subplots(figsize=(5, 5))
    plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=10, alpha=0.3)
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=100)
    plt.scatter(optimal_risk_portfolio[1], optimal_risk_portfolio[0], color='g', marker='*', s=100)
    plt.show()

    