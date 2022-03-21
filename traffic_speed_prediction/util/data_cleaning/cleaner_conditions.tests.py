import unittest
from traffic_speed_prediction.util.data_cleaning.cleaner_conditions import *

if __name__ == '__main__':
    unittest.main()

class CleanerTests(unittest.TestCase):
    def conditions_for_road_number_given_no_or_none_features_returns_empty(self):
        j_obj = [{
            "features": None
        }, {
        }]
        self.assertEqual(clean(j_obj, conditions_for_roadNumber), [])


    def conditions_for_road_number_given_no_none_or_negative_feature_id_returns_empty(self):
        id = [{
            "features": [{
                "id": 1
            },
                {}]
        }, {
            "features": [{
                "id": 1,
            }, {
                "id": None
            }]
        }, {
            "features": [{
                "id": 2
            }, {
                "id": -1
            }]
        }]
        self.assertEqual(clean(id, conditions_for_roadNumber), [])


    def conditions_for_road_number_given_no_or_none_feature_properties_returns_empty(self):
        properties = [{
            "features": [{
                "id": 1,
                "properties": None
            }]
        }, {
            "features": [{
                "id": 1
            }]
        }]
        self.assertEqual(clean(properties, conditions_for_roadNumber), [])


    def condition_for_road_number_given_no_or_none_road_station_id_returns_empty(self):
        road_number_stations = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": None
                }
            }]
        }, {
            "features": [{
                "id": 2,
                "properties": {
                }
            }]
        }]
        self.assertEqual(clean(road_number_stations, conditions_for_roadNumber), [])


