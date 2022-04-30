import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from autosklearn.classification import AutoSklearnClassifier
import autosklearn.regression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error as mse
import autosklearn.regression


class auto_ml:

    def __init__(self, isBeingTrained, isTrained):
        self.isBeingTrained = isBeingTrained
        self.isTrained = isTrained

    def train(self):
        global model
        self.isBeingTrained = True
        print("training model now!")
        try:
            dataset = pd.read_csv('traffic_speed_prediction/BigData.csv')
            x = dataset.drop(columns=['average_speed'])
            y = dataset['average_speed']
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            model = autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=30, per_run_time_limit=1)

            model.fit(x_train, y_train)
        except:
            print("Exception occured")
            self.isBeingTrained = False

        self.isTrained = True
        print("model has been trained and ready to predict")
        # print(x_train.describe())
        # print(y_train.describe())

        print("SCORE:")
        print("______________________________________________________________ ")
        print(model.score(x_test, y_test))
        y_test_predict = model.predict(x_test)
        print(mse(y_test, y_test_predict) ** 0.5)
        print("______________________________________________________________ ")
<<<<<<< HEAD
    @staticmethod
    def predict(road_section):
        dataset = pd.read_csv('traffic_speed_prediction/BigData.csv')
        x = dataset.drop(columns=['average_speed'])
        y = dataset['average_speed']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        model = autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=100, per_run_time_limit=30)
=======
>>>>>>> 43b56dd98f2898e3377ce69982db66d911c04c47

    def predict(road_section):
        return model.predict(np.array(
            [[road_section[0], road_section[1], road_section[2], road_section[3], road_section[4], road_section[5]]]))[
            0]

    def getModel(self):
        return model

    def isTrained(self):
        return self.isTrained

    def isBeingTrained(self):
        return self.isBeingTrained
