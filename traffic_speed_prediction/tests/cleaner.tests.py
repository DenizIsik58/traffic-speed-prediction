import unittest
from ..util.data_cleaning.cleaner import *

if __name__ == '__main__':
    unittest.main()

ENTITY1 = {  # no radAddress
    "roadStationId": 4051,
    "sensorId": 9,
    "sensorValue": 0.0,
    "measuredTime": "2022-03-15T07:49:00Z",
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 48
}
ENTITY2 = {  # roadSection is None
    "roadStationId": 4052,
    "sensorId": 126,
    "sensorValue": 3.5,
    "measuredTime": "2022-03-15T07:09:00Z",
    "roadAddress": {
        "roadSection": None
    },
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 48
}
ENTITY3 = {  # measuredTime is too short
    "roadStationId": 4053,
    "sensorId": 125,
    "sensorValue": 0.8,
    "measuredTime": "2022-03-15T07",
    "roadAddress": {
        "roadSection": 7
    },
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 48
}
ENTITY4 = {  # roadAverageSpeed is greater than roadSpeedLimit
    "roadStationId": 4054,
    "sensorId": 38,
    "sensorValue": -6.4,
    "measuredTime": "2022-03-15T07:49:00Z",
    "roadAddress": {
        "roadSection": 6
    },
    "roadSpeedLimit": 80,
    "roadAverageSpeed": 81
}
ENTITY5 = {  # perfect
    "roadStationId": 4055,
    "sensorId": 92,
    "sensorValue": 3.8,
    "measuredTime": "2022-03-15T07:49:00Z",
    "roadAddress": {
        "roadSection": 5
    },
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 48
}


class CleanerTests(unittest.TestCase):
    def setUp(self):
        self.data = [ENTITY1, ENTITY2, ENTITY3, ENTITY4, ENTITY5]

    # def test_ExactStringLength(self):
