from typing import List, Dict

EXACT_STRING_LENGTH = 0
MIN_STRING_LENGTH = 1
MAX_STRING_LENGTH = 2
NOT_NULL = 3
SUB_RULES = 4


class Rule:
    def __init__(self, type, determinant):
        self.type = type
        self.determinant = determinant

    def holds(self, val):
        if self.type == EXACT_STRING_LENGTH:
            return len(val) == self.determinant
        elif self.type == MIN_STRING_LENGTH:
            return len(val) >= self.determinant
        elif self.type == MAX_STRING_LENGTH:
            return len(val) <= self.determinant
        elif self.type == NOT_NULL:
            return val is not None
        elif self.type == SUB_RULES:
            return self.determinant.apply(val)


class Conditions:
    def __init__(self, rules):
        self.rules = rules

    def apply(self, jObj):
        for key, rules in self.rules.items():
            for rule in rules:
                try:
                    if not rule.holds(jObj[key]):
                        return False
                except KeyError:
                    return False
        return True


def clean(data: List[dict], condition):
    cleaned_data = []
    for jObj in data:
        if condition.apply(jObj):
            cleaned_data.append(jObj)
    return cleaned_data


condition1 = Conditions({
    "roadStationId": [Rule(NOT_NULL, None)],
    "sensorId": [Rule(NOT_NULL, None)],
    "sensorValue": [Rule(NOT_NULL, None)],
    "measuredTime": [Rule(NOT_NULL, None), Rule(EXACT_STRING_LENGTH, 20)],
    "roadAddress": [Rule(SUB_RULES, Conditions({
        "roadSection": [Rule(NOT_NULL, None)]
    }))]
})

if __name__ == "__main__":
    clean_data = clean([{
        "roadStationId": 4051,
        "sensorId": 9,
        "sensorValue": 0.0,
        "measuredTime": "2022-03-15T07:49:00Z"
    }, {
        "roadStationId": 4052,
        "sensorId": 126,
        "sensorValue": 0.0,
        "measuredTime": "2022-03-15T07:09:00Z",
        "roadAddress": {
            "roadSection": None
        }
    }, {
        "roadStationId": 4053,
        "sensorId": 125,
        "sensorValue": 0.82,
        "measuredTime": "2022-03-15T07:49:00Z",
        "roadAddress": {
            "roadSection": 1
        }
    }], condition1)

    for d in clean_data:
        print(d)
