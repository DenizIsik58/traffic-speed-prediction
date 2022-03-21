import unittest
from traffic_speed_prediction.util.data_cleaning.cleaner import *

if __name__ == '__main__':
    unittest.main()

ENTITY1 = {  # no radAddress
    "roadStationId": 4051,
    "sensorId": 9,
    "sensorValue": 0.0,
    "measuredTime": "2022-03-15T07:49:00Z",
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 30
}
ENTITY2 = {  # sensorValue is None
    "roadStationId": 4052,
    "sensorId": 126,
    "sensorValue": None,
    "measuredTime": "2022-03-15T07:49:00Z",
    "roadAddress": {
        "roadSection": 8
    },
    "roadSpeedLimit": 50,
    "roadAverageSpeed": 50
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

    def test_Rule_ExactStringLength_given_shorter_string_returns_1_2_4_5(self):
        con = Condition({
            "measuredTime": [Rule(EXACT_STRING_LENGTH, 20)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY2, ENTITY4, ENTITY5])

    def test_Rule_MinStringLength_given_shorter_string_returns_1_2_4_5(self):
        con = Condition({
            "measuredTime": [Rule(MIN_STRING_LENGTH, 18)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY2, ENTITY4, ENTITY5])

    def test_Rule_MaxStringLength_given_longer_string_returns_3(self):
        con = Condition({
            "measuredTime": [Rule(MAX_STRING_LENGTH, 13)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY3])

    def test_Rule_NotNone_given_None_returns_1_3_4_5(self):
        con = Condition({
            "sensorValue": [Rule(NOT_NONE, None)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY3, ENTITY4, ENTITY5])

    def test_Rule_SubRules_given_missing_field_returns_2_3_4_5(self):
        con = Condition({
            "roadAddress": [Rule(SUB_RULES, Condition({
                "roadSection": [Rule(NOT_NONE, None)]
            }))]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY2, ENTITY3, ENTITY4, ENTITY5])

    def test_Rule_Equals_given_another_field_returns_1_2_4_5(self):
        con = Condition({
            "measuredTime": [Rule(EQUALS, "2022-03-15T07:49:00Z")]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY2, ENTITY4, ENTITY5])

    def test_Rule_LessThan_given_another_field_returns_1(self):
        con = Condition({
            "roadAverageSpeed": [Rule(LESS_THAN, 40)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1])

    def test_Rule_MoreThan_given_another_field_returns_4(self):
        con = Condition({
            "roadSpeedLimit": [Rule(MORE_THAN, 70)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY4])

    def test_Rule_IsType_given_string_on_int_field_returns_empty(self):
        con = Condition({
            "sensorValue": [Rule(IS_TYPE, str)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [])

    def test_Rule_IsPositive_given_negative_number_returns_3_5(self):
        con = Condition({
            "sensorValue": [Rule(NOT_NONE, None), Rule(IS_POSITIVE, 0)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY3, ENTITY5])

    def test_Rule_IsZero_given_other_numbers_returns_1(self):
        con = Condition({
            "sensorValue": [Rule(NOT_NONE, None), Rule(IS_ZERO, 0)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1])

    def test_Rule_IsNegative_given_positive_number_returns_4(self):
        con = Condition({
            "sensorValue": [Rule(NOT_NONE, None), Rule(IS_NEGATIVE, 0)]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY4])

    def test_Rule_Not_given_Equals_and_other_field_returns_1_3_4_5(self):
        con = Condition({
            "roadSpeedLimit": [Rule(NOT_NONE, None), Rule(NOT, Rule(EQUALS_FIELD, "roadAverageSpeed"))]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY3, ENTITY4, ENTITY5])

    def test_Rule_Or_given_IsNegative_and_IsZero_returns_1_4(self):
        con = Condition({
            "sensorValue": [Rule(NOT_NONE, None), Rule(OR, [
                Rule(IS_NEGATIVE, 0),
                Rule(IS_ZERO, 0)
            ])]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY4])

    # def

    def test_Rule_EqualsField_given_another_field_returns_2(self):
        con = Condition({
            "roadSpeedLimit": [Rule(EQUALS_FIELD, "roadAverageSpeed")]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY2])

    def test_Rule_LessThanField_given_another_field_returns_1_3_5(self):
        con = Condition({
            "roadAverageSpeed": [Rule(LESS_THAN_FIELD, "roadSpeedLimit")]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY1, ENTITY3, ENTITY5])

    def test_Rule_MoreThanField_given_another_field_returns_4(self):
        con = Condition({
            "roadAverageSpeed": [Rule(MORE_THAN_FIELD, "roadSpeedLimit")]
        })

        cleaned = clean(self.data, con)

        self.assertEqual(cleaned, [ENTITY4])


FOR_ALL = 14  # Condition
