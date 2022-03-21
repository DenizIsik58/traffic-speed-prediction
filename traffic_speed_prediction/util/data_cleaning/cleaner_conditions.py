from .cleaner import *

conditions_for_roadNumber = Condition({
    # https://tie.digitraffic.fi/api/v3/metadata/tms-stations/road-number/78
    "features": [
        Rule(NOT_NULL, None),
        Rule(FOR_ALL, Condition({
            "id": [
                Rule(NOT_NULL, None),
                Rule(IS_POSITIVE, None)
            ],
            "properties": [
                Rule(NOT_NULL, None),
                Rule(SUB_RULES, Condition({
                    "roadStationId": [
                        Rule(NOT_NULL, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "tmsNumber": [
                        Rule(NOT_NULL, None),
                        Rule(IS_POSITIVE, None),
                    ],
                    "freeFlowSpeed1": [
                        Rule(NOT_NULL, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "roadAddress": [
                        Rule(NOT_NULL, None),
                        Rule(SUB_RULES, Condition({
                            "roadNumber": [Rule(NOT_NULL, None), None],
                            "roadSection": [Rule(NOT_NULL, None), None],
                            "roadMaintenanceClass": [Rule(NOT_NULL, None)]
                        }))]
                }))]
        }))]
})

conditions_for_roadConditions = Condition({
    # https://tie.digitraffic.fi/api/v3/data/road-conditions/54
    "weatherData": [Rule(FOR_ALL, Condition({
        "id": [Rule(NOT_NULL, None)],
        "roadConditions": [Rule(FOR_ALL, Condition({
            "daylight": [Rule(NOT_NULL, None)],
            "roadTemperature": [Rule(NOT_NULL, None)],
            "weatherSymbol": [Rule(NOT_NULL, None)],
            "overAllRoadCondition": [Rule(NOT_NULL, None)],
        }))]
    }))]
})

conditions_for_tmsData = Condition({
    # https://tie.digitraffic.fi//api/v1/data/tms-data/23408
    # sensorValue id 5056
    "tmsStations": [
        Rule(NOT_NULL, None),
        Rule(FOR_ALL, Condition({
            "id": [
                Rule(NOT_NULL, None),
                Rule(IS_POSITIVE, None)
            ],
            "sensorValues": [
                Rule(NOT_NULL, None),
                Rule(FOR_ALL, Condition({
                    "id": [
                        Rule(EQUALS, 5122),
                        Rule(IS_POSITIVE, None)
                    ],
                    "sensorValue": [
                        Rule(NOT_NULL, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "sensorUnit": [Rule(EQUAL, "km/h")]
                }))]
        }))]
})
