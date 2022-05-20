from typing import List

# All rules types supported by the cleaner (in int enum format).
# The comments describe the type of the argument that must be given along with the rule type.
# "Any" implies that the argument is never used - None will be a good substitute.
# "Key" implies that the argument must be of type string and must be a key that exists on the json object.
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
EXISTS = 15  # Condition
EQUALS_FIELD = 16  # Key
LESS_THAN_FIELD = 17  # Key
MORE_THAN_FIELD = 18  # Key


# A rule is a certain requirement that must be hold for a single value in the data to be cleaned.
# The rule has a rule_type, which describes what the rule is,
# and an argument, which will influence if the rule is holding.
# When the rule is evaluated [holds()] it will be given an additional argument,
# that is the one that needs to live up to the rule type, for its data to be clean.
class Rule:
    def __init__(self, rule_type, arg):
        self.rule_type = rule_type
        self.arg = arg

    # Given a value that needs to live up to the requirement of the rule type,
    # returns a bool, describing if the rule holds.
    # When evaluating the rule, the rule type will be switched (elif-compared), and the value
    # (and argument, if the rule type required one) will be checked.
    # The j_obj parameter is used if the value has to be asserted against the value of another key.
    # If the given rule type, is not specified here, the default return value is False.
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

    # Given a value returns a bool describing if the value was fixed (or if it was unable to be)
    # and a new value that has been fixed according to the rule type.
    # Not all rule types support fixing.
    def fix(self, val):
        if self.rule_type == IS_TYPE:
            return True, self.arg(val)
        elif self.rule_type == FOR_ALL:
            return True, clean_and_repair(val, self.arg)
        else:
            return False, val


# A condition is a set of requirements that must be applied to all values
# in a json object for it to be clean.
# The rule parameter is a dictionary of string keys to List[Rule] values, where each key is a field
# on the json objects, and the list has all the rules that must hold for the specified field.
# An empty list implies that the field must exist, but does not have to live up to any requirements.
class Condition:
    def __init__(self, rules):
        self.rules = rules

    # Given a json object, will return a bool describing if all rules applies for that object.
    # By looping over the keys for the rules and the rules applying to that key,
    # the values of the corresponding keys fields on the json objects, are evaluated
    # with all the rules. If a single rule do not hold,
    # then the whole json object are not clean. If all rules holds, then the data is clean.
    # A "KeyError" indicates that the current key, do not exist on the json object,
    # and the data is therefor not clean.
    def apply(self, j_obj):
        for key, rules in self.rules.items():
            for rule in rules:
                try:
                    if not rule.holds(j_obj, j_obj[key]):
                        return False
                except KeyError:
                    print("KeyError! '", key, "' is not found")
                    return False
        return True

    # Given a json object, will return a bool describing if all rules applies for that object,
    # and a cleaned version of the data.
    # By looping over the keys for the rules and the rules applying to that key, the values of the
    # corresponding keys fields on the json objects, are evaluated with all the rules. If a value
    # can be fixed by the rules rule type, it will be updated. If it can not be fixed, then
    # it will be evaluated to hold. If a single rule do not hold,
    # then the whole json object are not clean. If all rules holds, then the data is clean.
    # A "KeyError" indicates that the current key, do not exist on the json object,
    # and the data is therefor not clean.
    # A "ValueError" indicates that there is a value, that were tried to be cast into
    # another type, that it could not be converted to.
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


# Given a list of json objects (in dictionary format), will remove any element that do not
# live up to a set of conditions to apply on each field (value of a specific key)
def clean(data: List[dict], condition):
    cleaned_data = []
    for j_obj in data:
        if condition.apply(j_obj):
            cleaned_data.append(j_obj)

    return cleaned_data


# Given a list of json objects (in dictionary format), will try to keep as much data as possible
# when given a set of conditions to apply on each field (value of a specific key). If the condition
# is not satisfied, then the fields (values) are updated to meet the required condition. The new
# json object is kept if it were either clean or could be fixed.
def clean_and_repair(data: List[dict], condition):
    cleaned_data = []
    for j_obj in data:
        cleaned, cleaned_j_obj = condition.enforce(j_obj)
        if cleaned:
            cleaned_data.append(cleaned_j_obj)

    return cleaned_data
