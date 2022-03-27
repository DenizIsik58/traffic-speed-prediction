import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score

global model

def train():
    dataset = pd.read_csv('BigData.csv')

    x = dataset.drop(columns=['average_speed'])
    y = dataset['average_speed']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    model = DecisionTreeRegressor()
    model.fit(x_train, y_train)


def predict():
    return model.predict([[847, 2.3, 0, 400, 2, 75.0], [15, -1.7, 0, 0, 3, 74.0], [65, -0.1, 0, 0, 1, 50.0]])


def print_model():
    print("SCORE:")
    print("______________________________________________________________ ")
    print(model.score(x_test, y_test))
    print("______________________________________________________________ ")

    print()
    print()

    print("DATASET:")
    print(dataset)

    print()
    print()

    print("RESULTS:")
    print(predictions)



