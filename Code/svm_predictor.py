import get_stock_data as gsd
import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

class SVMPredictor:
    def __init__(self):
        self.stock_data = None
        self.classifier = svm.SVC(kernel='rbf', C=3)
        self.model_trust = False
        self.Y = []
        self.X = []
        self.X_pred = []

    def generate_model_data(self, price_change):
        X_transform = self.stock_data.get_X_data()
        self.Y = self.stock_data.get_Y_data(price_change)
        scaler = MinMaxScaler()
        X_transform = scaler.fit_transform(X_transform)
        self.X = X_transform[:-self.stock_data.num_prediction_inputs]
        self.X_pred = X_transform[-self.stock_data.num_prediction_inputs:]

    def train_and_validate_model(self):
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.Y, train_size=0.7, shuffle=True)
        self.classifier.fit(X_train, Y_train)
        Y_val = self.classifier.predict(X_test)
        score = accuracy_score(Y_val, Y_test)
        if (score >= 0.75):
            self.model_trust = True
        #print(score)
        #print(confusion_matrix(Y_test, Y_val, labels=[1, 0]))

    def get_predicted_price_class(self):
        predictions = [0, 0, 0]
        if (self.model_trust == True):
            predictions = self.classifier.predict(self.X_pred)
        return predictions

if __name__ == "__main__":
    predictor = SVMPredictor('EQNR.OL')
    predictor.generate_model_data(price_change=0.05)
    predictor.train_and_validate_model()
    list = predictor.get_predicted_price_class()
    predictor.generate_model_data(price_change=0.1)
    predictor.train_and_validate_model()
    list = predictor.get_predicted_price_class()



