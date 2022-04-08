import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


class auto_ml:


    @staticmethod
    def train():
        global model


            
        dataset = pd.read_csv("traffic_speed_prediction/BigData.csv")

        x = dataset.drop(columns=['average_speed'])
        y = dataset['average_speed']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        model = DecisionTreeRegressor()
        model.fit(x_train, y_train)
        #print(x_train.describe())
        #print(y_train.describe())

        print("SCORE:")
        print("______________________________________________________________ ")
        print(model.score(x_test, y_test))
        print("______________________________________________________________ ")

        #print("DATASET:")
        #print(dataset)

        #print("RESULTS:")
        #print(road_section[0], road_section[1], road_section[2], road_section[3], road_section[4], road_section[5])
        #print(model.predict([road_section[0], road_section[1], road_section[2], road_section[3], road_section[4], road_section[5]]))

    @staticmethod
    def predict(road_section):
        return model.predict([[road_section[0], road_section[1], road_section[2], road_section[3], road_section[4], road_section[5]]])

    @staticmethod
    def print_model():
        pass




