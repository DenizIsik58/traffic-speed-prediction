from .cleaner import *

conditions_for_roadNumber = Condition({
    # https://tie.digitraffic.fi/api/v3/metadata/tms-stations/road-number/78
    "id": [
        Rule(NOT_NONE, None)
    ],
    "properties": [
        Rule(NOT_NONE, None),
        Rule(SUB_RULES, Condition({
            "roadStationId": [
                Rule(NOT_NONE, None)
            ],
            "tmsNumber": [
                Rule(NOT_NONE, None)
            ],
            "freeFlowSpeed1": [
                Rule(NOT_NONE, None)
            ],
            "roadAddress": [
                Rule(NOT_NONE, None),
                Rule(SUB_RULES, Condition({
                    "roadNumber": [
                        Rule(NOT_NONE, None)
                    ],
                    "roadSection": [
                        Rule(NOT_NONE, None)
                    ],
                    "roadMaintenanceClass": [
                        Rule(NOT_NONE, None)
                    ]
                }))]
        }))]
})

conditions_for_roadConditions = Condition({  # det er kun den første
    # https://tie.digitraffic.fi/api/v3/data/road-conditions/54
    "id": [
        Rule(NOT_NONE, None),
        Rule(IS_POSITIVE, None)
    ],
    "roadConditions": [
        Rule(NOT_NONE, None),
        Rule(EXISTS, Condition({
            "daylight": [Rule(NOT_NONE, None)],
            "roadTemperature": [Rule(NOT_NONE, None)],
            "weatherSymbol": [Rule(NOT_NONE, None)],
            "overAllRoadCondition": [Rule(NOT_NONE, None)],
        }))]
})

conditions_for_tmsData = Condition({
    # https://tie.digitraffic.fi//api/v1/data/tms-data/23408
    "id": [
        Rule(NOT_NONE, None),
        Rule(IS_POSITIVE, None)
    ],
    "sensorValues": [
        Rule(NOT_NONE, None),
        Rule(EXISTS, Condition({
            "id": [
                Rule(EQUALS, 5122)
            ],
            "sensorValue": [
                Rule(NOT_NONE, None),
                Rule(IS_POSITIVE, None)
            ],
            "sensorUnit": [Rule(EQUALS, "km/h")]
        }))]
})
