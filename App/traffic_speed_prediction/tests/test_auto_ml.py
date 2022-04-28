import unittest
from traffic_speed_prediction.traffic_speed_prediction.auto_ml import auto_ml
import pandas as pd
from sklearn.metrics import mean_squared_error as mse

if __name__ == '__main__':
    unittest.main()


class AutoMlTests(unittest.TestCase) :
    def setUp(self):
        auto_ml.train()
        self.model = auto_ml.getModel()

    #def test_data_two_hours_before_vs_automl_model(self):
        #dataset10 = pd.read_csv('BigData_10.csv')
        #dataset14 = pd.read_csv('BigData_14.csv')
        #dataset10 = dataset10['average_speed']
        #actual = dataset14['average_speed']
        #dataset14 = dataset14.drop(columns=['average_speed'])
        #predict_14 = self.model.predict(dataset14)

        #modelscore = mse(actual, predict_14)**0.5
        #dummyscore = mse(actual, dataset10)**0.5

        self.assertTrue(modelscore < dummyscore)