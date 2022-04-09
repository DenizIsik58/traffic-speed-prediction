import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
#from autosklearn.classification import AutoSklearnClassifier
import autosklearn.regression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error as mse
import autosklearn.regression

class auto_ml:


    @staticmethod
    def train():
        global model

        dataset = pd.read_csv('BigData.csv')


        x = dataset.drop(columns=['average_speed'])
        y = dataset['average_speed']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        model = RandomForestRegressor()
        #autosklearn.regression.AutoSklearnRegressor(time_left_for_this_task=30, per_run_time_limit=1)

        model.fit(x_train, y_train)

        print("DONE")
        #print(y_train.describe())

        #print("SCORE:")
        #print("______________________________________________________________ ")
        #print(model.score(x_test, y_test))
        y_test_predict = model.predict(x_test)
        #print(x_test)
        print(mse(y_test, y_test_predict) ** 0.5)
        #print("______________________________________________________________ ")

        #y_test_predict = model.predict(x_test)
        #print(mse(y_test, y_test_predict)**0.5)
        return

    @staticmethod
    def predict(road_section):
        return model.predict(np.array([[road_section[0], road_section[1], road_section[2], road_section[3], road_section[4], road_section[5]]]))[0]

    @staticmethod
    def getModel():
        return model

    @staticmethod
    def twoHourTest():
        dataset10 = pd.read_csv('BigData_10.csv')
        dataset14 = pd.read_csv('BigData_14.csv')
        dataset10 = dataset10['average_speed']
        actual = dataset14['average_speed']
        dataset14 = dataset14.drop(columns=['average_speed'])
        predict_14 = model.predict(dataset14)

        print(mse(actual, predict_14)**0.5)
        print(mse(actual, dataset10)**0.5)

        max = np.argmax(actual - dataset10)
        print("max : " + str(max))
        print(actual[max] - dataset10[max])