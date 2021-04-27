import re
from arithmetic import Arithmetic
from variables_types import TypeVariable


class Comparison:
    @staticmethod
    def isnumber(str):
        if str is None:
            return False
        try:
            float(str)
            return True
        except ValueError:
            return False

    @staticmethod
    def isint(str):
        if str is None:
            return False
        try:
            int(str)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_val_in_array(val, name_var, vars, worker):
        if vars[name_var][1].value < TypeVariable.arrayNumbers.value:
            return None
        index_str = val[len(name_var) + 1:]
        index = Comparison.parse_val(index_str, vars, worker)
        if index is None:
            return None
        if not Comparison.isint(index):
            return None
        index = int(index) - 1
        if index < 0 or index >= len(vars[name_var][0]):
            return None
        return vars[name_var][0][index]

    @staticmethod
    def parse_val(val, vars, worker):
        if val in vars:
            return vars[val][0]
        name_var = worker.is_change_var(val)
        if name_var is not None:
            return_val = Comparison.get_val_in_array(
                val, name_var, vars, worker)
            if return_val is not None:
                return return_val
        if Comparison.isnumber(val):
            return float(val)
        if len(val) == 0:
            return None
        if ("\"" == val[0] and "\"" == val[-1] or
            "\'" == val[0] and "\'" == val[-1] and len(val) == 3) \
                and "add" not in val and "plus" not in val:
            return val[1:-1]
        if val == "yes" or val == "true" \
                or val == "right" or val == "correct":
            return True
        if val == "no" or val == "false" \
                or val == "wrong" or val == "incorrect":
            return False
        solution = Arithmetic.solve_expression(val, vars, worker)
        if solution is not None:
            return solution
        else:
            name_method = worker.find_method(val)
            if name_method is not None \
                    and worker\
                    .classes[worker.current_class][name_method][1] \
                    is not None:
                return worker.call_method("", val, vars)
        return None

    @staticmethod
    def solve_expression(str, vars, worker):
        expressions = re.split(r" or ", str)
        res = False
        for i in range(0, len(expressions)):
            operands = re.split(r" and ", expressions[i])
            solution_operands = Comparison\
                .solve_operands(operands, vars, worker)
            if solution_operands is None:
                return None
            if i == 0:
                res = solution_operands
                if res:
                    return True
            else:
                res = res or solution_operands
                if res:
                    return True
        return res

    @staticmethod
    def solve_operands(operands, vars, worker):
        res = False
        for i in range(0, len(operands)):
            val = Comparison.solve_operand(operands[i], vars, worker)
            if val is None:
                return None
            if i == 0:
                res = val
                if not res:
                    return False
            else:
                res = res and val
                if not res:
                    return False
        return res

    @staticmethod
    def solve_operand(operand, vars, worker):
        is_not = False
        if "it’s not the case that" in operand:
            is_not = True
            operand = operand[len("it’s not the case that "):]
        elif operand.find("not") == 0:
            is_not = True
            operand = operand[len("not "):]
        operation = Comparison.parse_type_operand(operand)
        if operation is None:
            val_operand = Comparison.parse_val(operand, vars, worker)
            if isinstance(val_operand, bool):
                if is_not:
                    return not val_operand
                return val_operand
            return None
        if operation == "Equal":
            vals = re.split(r" is | was | have | has | had | are | were ",
                            operand)
            val_one = Comparison.parse_val(vals[0], vars, worker)
            val_two = Comparison.parse_val(vals[1], vars, worker)
            if is_not:
                return val_one != val_two
            return val_one == val_two
        if operation == "Not equal":
            vals = re.split(r" isn\'t | is not | wasn\'t "
                            r"| was not | haven\'t | have not "
                            r"| hasn\'t | has not | hadn\'t | had not "
                            r"| aren't | are not | weren\'t | were not ",
                            operand)
            val_one = Comparison.parse_val(vals[0], vars, worker)
            val_two = Comparison.parse_val(vals[1], vars, worker)
            if is_not:
                return val_one == val_two
            return val_one != val_two
        val_one = Comparison.parse_val(
            re.split(r"is|was|have|has|had|are|were", operand)[0][:-1],
            vars, worker)
        val_two = Comparison.parse_val(
            operand[operand.find("than") + 5:], vars, worker)
        if operation == "Less":
            if is_not:
                return val_one >= val_two
            return val_one < val_two
        if operation == "Greater":
            if is_not:
                return val_one <= val_two
            return val_one > val_two
        if operation == "Greater or equal":
            if is_not:
                return val_one < val_two
            return val_one >= val_two
        if operation == "Less or equal":
            if is_not:
                return val_one > val_two
            return val_one <= val_two

    @staticmethod
    def parse_type_operand(operand):
        if "no less than " in operand or " not less than " in operand \
                or "n\'t less than " in operand:
            return "Greater or equal"
        if " not more than " in operand or "no more than " in operand \
                or "n\'t more " in operand \
                or " not greater than " in operand \
                or "no greater than " in operand \
                or "n\'t greater than " in operand:
            return "Less or equal"
        if " less than " in operand:
            return "Less"
        if " more than " in operand or " greater than " in operand:
            return "Greater"
        if "n\'t" in operand or operand.find("not") > 0:
            return "Not equal"
        if " is " in operand or " was " in operand or " had " in operand \
                or " were " in operand or " are " in operand \
                or " has " in operand or " have " in operand:
            return "Equal"
        return None
