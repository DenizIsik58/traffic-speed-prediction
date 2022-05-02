from typing import List

# All rules supported by the cleaner
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
EXISTS = 15
EQUALS_FIELD = 16  # Key
LESS_THAN_FIELD = 17  # Key
MORE_THAN_FIELD = 18  # Key

# A rule for the cleaner
# rule_type: What the rule checks for
# arg: the constant which the rule depends on (e.g. a rule_type may be EQUALS and the arg may be 5)
class Rule:
    def __init__(self, rule_type, arg):
        self.rule_type = rule_type
        self.arg = arg

    # Checks if a given value holds for the rule
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
        elif self.rule_type == EXISTS:
            for obj in val:
                if self.arg.apply(obj):
                    return True
            return False
        elif self.rule_type == EQUALS_FIELD:
            return val == j_obj[self.arg]
        elif self.rule_type == LESS_THAN_FIELD:
            return val < j_obj[self.arg]
        elif self.rule_type == MORE_THAN_FIELD:
            return val > j_obj[self.arg]
        else:
            return False

    # Fix the rule
    def fix(self, val):
        if self.rule_type == IS_TYPE:
            return True, self.arg(val)
        elif self.rule_type == FOR_ALL:
            return True, clean_and_repair(val, self.arg)
        else:
            return False, val

# A condition
# rules: map of strings -> list of rules
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
    
    def enforce(self, j_obj):
        new_j_obj = {}
        for key, rules in self.rules.items():
            repaired = False
            for rule in rules:
                try:
                    repaired, new_val = rule.fix(j_obj[key])
                    if repaired:
                        new_j_obj[key] = new_val
                    elif not rule.holds(j_obj, j_obj[key]):
                        return False, None
                except KeyError:
                    print("KeyError! '", key, "' is not found")
                    return False, None
                except ValueError:
                    print("ValueError! Cannot cast '", j_obj[key], "' into '", rule.arg, "'")
                    return False, None
            if not repaired:
                new_j_obj[key] = j_obj[key]
        return True, new_j_obj

# Clean a list of data given by a condition 
def clean(data: List[dict], condition):
    cleaned_data = []
    for j_obj in data:

        if condition.apply(j_obj):
            cleaned_data.append(j_obj)

    return cleaned_data


def clean_and_repair(data: List[dict], condition):
    cleaned_data = []
    for j_obj in data:
        cleaned, cleaned_j_obj = condition.enforce(j_obj)
        if cleaned:
            cleaned_data.append(cleaned_j_obj)

    return cleaned_data
