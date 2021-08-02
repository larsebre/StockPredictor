import get_stock_data as gsd
import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

class SVMPredictor:
    def __init__(self, ticker):
        self.stock = gsd.StockData(ticker, data_days=400, forecast=20)
        self.stock.initialize()

        self.classifier = svm.SVC(kernel='rbf', C=3)
        
        self.X_transform = self.stock.get_X_data()
        self.Y = self.stock.get_Y_data()
        print(self.Y)
        
        self.scaler = MinMaxScaler()
        self.X_transform = self.scaler.fit_transform(self.X_transform)
        self.X = self.X_transform[:-self.stock.num_prediction_inputs]
        self.X_pred = self.X_transform[-self.stock.num_prediction_inputs:]

    def train_model(self):
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, train_size=0.7, shuffle=True)
        self.classifier.fit(X_train, Y_train)
        svm.SVC()

        Y_pred = self.classifier.predict(X_test)
        print(Y_pred)
        print(confusion_matrix(Y_test, Y_pred, labels=[1, 0]))

if __name__ == "__main__":
    predictor = SVMPredictor('EQNR.OL')
    predictor.train_model()



