from typing import List

EXACT_STRING_LENGTH = 0  # int
MIN_STRING_LENGTH = 1  # int
MAX_STRING_LENGTH = 2  # int
NOT_NULL = 3  # Any
SUB_RULES = 4  # Condition
EQUALS = 5  # Key
LESS_THAN = 6  # Key
MORE_THAN = 7  # Key
IS_TYPE = 8  # type
IS_POSITIVE = 9  # Number
IS_ZERO = 10  # Number
IS_NEGATIVE = 11  # Number
NOT = 12  # Rule
OR = 13  # (Rule, Rule)
FOR_ALL = 14  # Condition


class Rule:
    def __init__(self, rule_type, arg):
        self.rule_type = rule_type
        self.arg = arg

    def holds(self, j_obj, val):
        if self.rule_type == EXACT_STRING_LENGTH:
            return len(val) == self.arg
        elif self.rule_type == MIN_STRING_LENGTH:
            return len(val) >= self.arg
        elif self.rule_type == MAX_STRING_LENGTH:
            return len(val) <= self.arg
        elif self.rule_type == NOT_NULL:
            return val is not None
        elif self.rule_type == SUB_RULES:
            return self.arg.apply(val)
        elif self.rule_type == EQUALS:
            return val == j_obj[self.arg]
        elif self.rule_type == LESS_THAN:
            return val < j_obj[self.arg]
        elif self.rule_type == MORE_THAN:
            return val > j_obj[self.arg]
        elif self.rule_type == IS_TYPE:
            return type(val) == self.arg
        elif self.rule_type == IS_POSITIVE:
            return val > 0
        elif self.rule_type == IS_ZERO:
            return val == 0
        elif self.rule_type == IS_NEGATIVE:
            return val < 0
        elif self.rule_type == NOT:
            return not self.arg.holds(j_obj, val)
        elif self.rule_type == OR:
            return self.arg[0].holds(j_obj, val) or self.arg[1].holds(j_obj, val)
        elif self.rule_type == FOR_ALL:
            for obj in val:
                if not self.arg.apply(obj):
                    return False
            return True


class Condition:
    def __init__(self, rules):
        self.rules = rules

    def apply(self, j_obj):
        for key, rules in self.rules.items():
            for rule in rules:
                try:
                    if not rule.holds(j_obj, j_obj[key]):
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

condition1 = Condition({
    "roadStationId": [Rule(NOT_NULL, None)],
    "sensorId": [Rule(NOT_NULL, None)],
    "sensorValue": [Rule(NOT_NULL, None)],
    "measuredTime": [Rule(NOT_NULL, None), Rule(EXACT_STRING_LENGTH, 20)],
    "roadAddress": [Rule(SUB_RULES, Condition({
        "roadSection": [Rule(NOT_NULL, None)]
    }))],
    "roadSpeedLimit": [Rule(NOT_NULL, None)],
    "roadAverageSpeed": [Rule(LESS_THAN, "roadSpeedLimit")]
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
        },
        "roadSpeedLimit": 50,
        "roadAverageSpeed": 48
    }, {
        "roadStationId": 4053,
        "sensorId": 125,
        "sensorValue": 0.82,
        "measuredTime": "2022-03-15T07:49:00Z",
        "roadAddress": {
            "roadSection": 1
        },
        "roadSpeedLimit": 50,
        "roadAverageSpeed": 62
    }], condition1)

    for d in clean_data:
        print(d)
