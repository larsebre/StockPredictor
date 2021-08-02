import get_stock_data as gsd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    stock_data = gsd.StockData('EQNR.OL', data_days=1400, forecast=20)
    stock_data.initialize()

    #Scatter plot to see correlation
    plt.scatter(stock_data.df_x_data['S&P 500 Close'], stock_data.df_y_data['Price Change'])
    plt.show()

    print(stock_data.df_data)
