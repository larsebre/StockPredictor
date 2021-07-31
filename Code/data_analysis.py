import get_stock_data as gsd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    stock_data = gsd.StockData('EQNR.OL', data_days=700, forecast=20)
    stock_data.initialize()

    #Scatter plot to see correlation
    plt.scatter(stock_data.df_data['CCI20'], stock_data.df_data['Price Change'])
    plt.show()

    print(stock_data.df_data)
