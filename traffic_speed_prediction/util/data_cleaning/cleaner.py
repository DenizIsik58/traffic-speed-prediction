from typing import List

EXACT_STRING_LENGTH = 0  # int
MIN_STRING_LENGTH = 1  # int
MAX_STRING_LENGTH = 2  # int
NOT_NONE = 3  # Any
SUB_RULES = 4  # Condition
EQUALS = 5  # Any
LESS_THAN = 6  # Number
MORE_THAN = 7  # Number
IS_TYPE = 8  # type
IS_POSITIVE = 9  # Any
IS_ZERO = 10  # Any
IS_NEGATIVE = 11  # Any
NOT = 12  # Rule
OR = 13  # list[Rule]
FOR_ALL = 14  # Condition
EQUALS_FIELD = 15  # Key
LESS_THAN_FIELD = 16  # Key
MORE_THAN_FIELD = 17  # Key



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
        elif self.rule_type == NOT_NONE:
            return val is not None
        elif self.rule_type == SUB_RULES:
            return self.arg.apply(val)
        elif self.rule_type == EQUALS:
            return val == self.arg
        elif self.rule_type == LESS_THAN:
            return val < self.arg
        elif self.rule_type == MORE_THAN:
            return val > self.arg
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
            for rule in self.arg:
                if rule.holds(j_obj, val):
                    return True
            return False
        elif self.rule_type == FOR_ALL:
            for obj in val:
                if not self.arg.apply(obj):
                    return False
            return True
        elif self.rule_type == EQUALS_FIELD:
            return val == j_obj[self.arg]
        elif self.rule_type == LESS_THAN_FIELD:
            return val < j_obj[self.arg]
        elif self.rule_type == MORE_THAN_FIELD:
            return val > j_obj[self.arg]


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



