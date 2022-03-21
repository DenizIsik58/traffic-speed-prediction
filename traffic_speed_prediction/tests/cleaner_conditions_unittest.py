import unittest
from traffic_speed_prediction.util.data_cleaning.cleaner_conditions import *

if __name__ == '__main__':
    unittest.main()


class CleanerTests(unittest.TestCase):
    def test_conditions_for_road_number_given_no_or_none_features_returns_empty(self):
        data = [{
            "features": None
        }, {
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_conditions_for_road_number_given_no_none_or_negative_feature_id_returns_empty(self):
        data = [{
            "features": [{
                "id": None,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": -1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_conditions_for_road_number_given_no_or_none_feature_properties_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": None
            }]
        }, {
            "features": [{
                "id": 1
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_road_station_id_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": None,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": -1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_tms_number_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": None,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": -1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_free_flow_speed1_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": None,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": -1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_or_none_roadAddress_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": None
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_road_number_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": None,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": -1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_road_section_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": None,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": -1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_no_none_or_negative_road_maintenance_class_returns_empty(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": None
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1
                    }
                }
            }]
        }, {
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": -1
                    }
                }
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadNumber))

    def test_condition_for_road_number_given_acceptable_data_returns_the_data(self):
        data = [{
            "features": [{
                "id": 1,
                "properties": {
                    "roadStationId": 1,
                    "tmsNumber": 1,
                    "freeFlowSpeed1": 1,
                    "roadAddress": {
                        "roadNumber": 1,
                        "roadSection": 1,
                        "roadMaintenanceClass": 1
                    }
                }
            }]
        }]
        self.assertEqual(data, clean(data, conditions_for_roadNumber))

    def test_condition_for_road_conditions_given_acceptable_data_returns_the_data(self):
        data = [{
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }]
        self.assertEqual(data, clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_weather_data_returns_empty(self):
        data = [{
            "weatherData": None
        }, {

        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_none_or_negative_id_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": None,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }, {
            "weatherData": [{
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }, {
            "weatherData": [{
                "id": -1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_road_conditions_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": 1
            }]
        }, {
            "weatherData": [{
                "id": 1,
                "roadConditions": None
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_daylight_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }, {
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": None,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_road_temperature_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": None,
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }, {
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_weather_symbol_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": None,
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }, {
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "overAllRoadCondition": "NORMAL"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_road_conditions_given_no_or_none_over_all_road_condition_returns_empty(self):
        data = [{
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400",
                    "overAllRoadCondition": None
                }]
            }]
        }, {
            "weatherData": [{
                "id": 1,
                "roadConditions": [{
                    "daylight": True,
                    "roadTemperature": "+20",
                    "weatherSymbol": "d400"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_roadConditions))

    def test_condition_for_tms_data_given_acceptable_data_returns_the_data(self):
        data = [{
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }]
        self.assertEqual(data, clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_or_none_tms_stations_returns_empty(self):
        data = [{
            "tmsStations": None
        }, {
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_none_or_negative_id_returns_empty(self):
        data = [{
            "tmsStations": [{
                "id": None,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "id": -1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_or_none_sensor_values_returns_empty(self):
        data = [{
            "tmsStations": [{
                "id": 1
            }]
        }, {
            "tmsStations": [{
                "id": 1,
                "sensorValues": None
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_none_or_not_5122_sensor_values_id_returns_empty(self):
        data = [{
            "tmsStations": [{
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "sensorValues": [{
                    "id": None,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5121,
                    "sensorValue": 1,
                    "sensorUnit": "km/h"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_none_or_negative_sensor_value_returns_empty(self):
        data = [{
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": None,
                    "sensorUnit": "km/h"
                }]
            }]
        }, {
            "tmsStations": [{
                "id": -1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": -1,
                    "sensorUnit": "km/h"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

    def test_condition_for_tms_data_given_no_none_or_not_kmh_returns_empty(self):
        data = [{
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1
                }]
            }]
        }, {
            "tmsStations": [{
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": None
                }]
            }]
        }, {
            "tmsStations": [{
                "id": 1,
                "sensorValues": [{
                    "id": 5122,
                    "sensorValue": 1,
                    "sensorUnit": "kpl"
                }]
            }]
        }]
        self.assertEqual([], clean(data, conditions_for_tmsData))

