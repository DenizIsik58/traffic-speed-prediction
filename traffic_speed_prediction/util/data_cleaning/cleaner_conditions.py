from .cleaner import *

conditions_for_roadNumber = Condition({
    # https://tie.digitraffic.fi/api/v3/metadata/tms-stations/road-number/78
    "features": [
        Rule(NOT_NONE, None),
        Rule(FOR_ALL, Condition({
            "id": [
                Rule(NOT_NONE, None),
                Rule(IS_POSITIVE, None)
            ],
            "properties": [
                Rule(NOT_NONE, None),
                Rule(SUB_RULES, Condition({
                    "roadStationId": [
                        Rule(NOT_NONE, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "tmsNumber": [
                        Rule(NOT_NONE, None),
                        Rule(IS_POSITIVE, None),
                    ],
                    "freeFlowSpeed1": [
                        Rule(NOT_NONE, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "roadAddress": [
                        Rule(NOT_NONE, None),
                        Rule(SUB_RULES, Condition({
                            "roadNumber": [
                                Rule(NOT_NONE, None),
                                Rule(IS_POSITIVE, None)
                            ],
                            "roadSection": [
                                Rule(NOT_NONE, None),
                                Rule(IS_POSITIVE, None)
                            ],
                            "roadMaintenanceClass": [
                                Rule(NOT_NONE, None),
                                Rule(IS_POSITIVE, None)
                            ]
                        }))]
                }))]
        }))]
})

conditions_for_roadConditions = Condition({
    # https://tie.digitraffic.fi/api/v3/data/road-conditions/54
    "weatherData": [
        Rule(NOT_NONE, None),
        Rule(FOR_ALL, Condition({
            "id": [
                Rule(NOT_NONE, None),
                Rule(IS_POSITIVE, None)
            ],
            "roadConditions": [
                Rule(NOT_NONE, None),
                Rule(FOR_ALL, Condition({
                    "daylight": [Rule(NOT_NONE, None)],
                    "roadTemperature": [Rule(NOT_NONE, None)],
                    "weatherSymbol": [Rule(NOT_NONE, None)],
                    "overAllRoadCondition": [Rule(NOT_NONE, None)],
                }))]
        }))]
})

conditions_for_tmsData = Condition({
    # https://tie.digitraffic.fi//api/v1/data/tms-data/23408
    # sensorValue id 5056
    "tmsStations": [
        Rule(NOT_NONE, None),
        Rule(FOR_ALL, Condition({
            "id": [
                Rule(NOT_NONE, None),
                Rule(IS_POSITIVE, None)
            ],
            "sensorValues": [
                Rule(NOT_NONE, None),
                Rule(FOR_ALL, Condition({
                    "id": [
                        Rule(EQUALS, 5122)
                    ],
                    "sensorValue": [
                        Rule(NOT_NONE, None),
                        Rule(IS_POSITIVE, None)
                    ],
                    "sensorUnit": [Rule(EQUALS, "km/h")]
                }))]
        }))]
})
