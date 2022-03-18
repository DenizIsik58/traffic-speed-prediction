from .cleaner import *

conditions_for_roadNumber = Condition({
    #id
    #roadStationId
    #tmsNumber
    #roadAddress
    #roadNumber
    #roadSectionId
    "features": [
        Rule(NOT_NULL, None),
        Rule(FOR_ALL, Condition({
            "id": [Rule(NOT_NULL, None)],
            "properties": [
                Rule(NOT_NULL, None),
                Rule(SUB_RULES, Condition({
                    "roadStationId": [Rule(NOT_NULL, None)],
                    "tmsNumber": [Rule(NOT_NULL, None)],
                    "roadAddress": [
                        Rule(NOT_NULL, None),
                        Rule(SUB_RULES, Condition({
                            "roadNumber": [Rule(NOT_NULL, None), None],
                            "roadSection": [Rule(NOT_NULL, None), None],
                        }))]
                }))]
        }))]
})



