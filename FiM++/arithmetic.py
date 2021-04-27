import re
from variables_types import TypeVariable


class Arithmetic:
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
    def get_val_by_method(operand, vars, worker):
        name_method = worker.find_method(operand)
        if name_method is not None:
            if worker.classes[worker.current_class][name_method][1] \
                    == TypeVariable.number:
                return worker.call_method("", operand, vars)
            else:
                raise ValueError("Invalid type of value: " + operand)
        else:
            raise ArithmeticError("Can not understand a term: " +
                                  operand)

    @staticmethod
    def get_name_var_and_index(operand, vars, worker):
        index = None
        if operand not in vars:
            name_var = worker.is_change_var(operand)
            if name_var is None:
                return None, None
            else:
                index_str = operand[len(name_var) + 1:]
                if not Arithmetic.isint(index_str):
                    if index_str in vars:
                        if vars[index_str][1] == TypeVariable.number \
                                and Arithmetic.isint(vars[index_str][0]):
                            index = int(vars[index_str][0]) - 1
                            if index < 0 or index >= len(vars[name_var][0]):
                                return None, None
                            return name_var, index
                        return None, None
                    return None, None
                index = int(index_str) - 1
        else:
            name_var = operand
        return name_var, index

    @staticmethod
    def change_var(expr, vars, worker):
        operation = Arithmetic.find_arithmetic_operation(expr)
        not_parsed_expr = expr
        if operation == "Addition":
            if expr.find("add") == 0:
                expr = expr[len("add "):]
                if "to" not in expr or "added" in expr or "plus" in expr:
                    return False
                operands = re.split(r" to ", expr)
                if len(operands) != 2:
                    return False
                name_var, index = Arithmetic.get_name_var_and_index(
                    operands[1], vars, worker)
                if name_var is None:
                    return False
                if vars[name_var][2]:
                    raise ArithmeticError("Can not change value "
                                          "of the const: " + not_parsed_expr)
                value = Arithmetic.sum_operands(operands, vars, worker)
                if TypeVariable.get_type_by_val(value) \
                        != vars[name_var][1] \
                        and len(vars[name_var]) == 3 \
                        or len(vars[name_var]) == 4 \
                        and TypeVariable.get_type_by_val(value) \
                        != vars[name_var][3]:
                    return False
                if index is not None:
                    vars[name_var][0][index] = value
                    return True
                vars[name_var] = (value, vars[name_var][1], False)
                return True
            else:
                return False
        elif operation == "Subtraction":
            if expr.find("subtract") == 0:
                expr = expr[len("subtract "):]
                if "from" not in expr or "minus" in expr:
                    return False
                operands = re.split(r" from ", expr)
                if len(operands) != 2:
                    return False
                name_var, index = Arithmetic.get_name_var_and_index(
                    operands[1], vars, worker)
                if name_var is None:
                    return False
                if vars[name_var][2]:
                    raise ArithmeticError("Can not change value "
                                          "of the const: " + not_parsed_expr)
                value = Arithmetic.sub_operands(operands[::-1], vars, worker)
                if TypeVariable.get_type_by_val(value) \
                        != vars[name_var][1] \
                        and len(vars[name_var]) == 3 \
                        or len(vars[name_var]) == 4 \
                        and TypeVariable.get_type_by_val(value) \
                        != vars[name_var][3]:
                    return False
                if index is not None:
                    vars[name_var][0][index] = value
                    return True
                vars[name_var] = (value, vars[name_var][1], False)
                return True
            else:
                return False
        elif operation == "Multiplication":
            if expr.find("multiply") == 0:
                expr = expr[len("multiply "):]
                if "to" not in expr or "times" in expr:
                    return False
                operands = re.split(r" to ", expr)
                if len(operands) != 2:
                    return False
                name_var, index = Arithmetic.get_name_var_and_index(
                    operands[0], vars, worker)
                if name_var is None:
                    return False
                if vars[name_var][2]:
                    raise ArithmeticError("Can not change value "
                                          "of the const: " + not_parsed_expr)
                value = Arithmetic.mult_operands(operands, vars, worker)
                if TypeVariable.get_type_by_val(value) \
                        != vars[name_var][1] \
                        and len(vars[name_var]) == 3 \
                        or len(vars[name_var]) == 4 \
                        and TypeVariable.get_type_by_val(value) \
                        != vars[name_var][3]:
                    return False
                if index is not None:
                    vars[name_var][0][index] = value
                    return True
                vars[name_var] = (value, vars[name_var][1], False)
                return True
            else:
                return False
        if operation == "Division":
            if expr.find("divide") == 0:
                expr = expr[len("divide "):]
                if "by" not in expr or "divided by" in expr:
                    return False
                operands = re.split(r" by ", expr)
                if len(operands) != 2:
                    return False
                name_var, index = Arithmetic.get_name_var_and_index(
                    operands[0], vars, worker)
                if name_var is None:
                    return False
                if vars[name_var][2]:
                    raise ArithmeticError("Can not change value "
                                          "of the const: " + not_parsed_expr)
                value = Arithmetic.div_operands(operands, vars, worker)
                if TypeVariable.get_type_by_val(value) \
                        != vars[name_var][1] \
                        and len(vars[name_var]) == 3 \
                        or len(vars[name_var]) == 4 \
                        and TypeVariable.get_type_by_val(value) \
                        != vars[name_var][3]:
                    return False
                if index is not None:
                    vars[name_var][0][index] = value
                    return True
                vars[name_var] = (value, vars[name_var][1], False)
                return True
            else:
                return False
        return False

    @staticmethod
    def find_arithmetic_operation(str):
        if str.find("add") == 0 or "plus" in str \
                or "added to" in str or "Add" in str \
                or "got one more" in str:
            return "Addition"
        elif "minus" in str or "without" in str \
                or "subtract" in str or "the difference between" in str \
                or "got one less" in str:
            return "Subtraction"
        elif "times" in str or "multiplied with" in str \
                or "multiply" in str:
            return "Multiplication"
        elif "divided" in str or "by" in str or "divide" in str:
            return "Division"
        return None

    @staticmethod
    def find_sum_strs(operands, vars, worker):
        for operand in operands:
            if operand.find("\"") == 0 \
                    and operand.rfind("\"") == len(operand) - 1 \
                    and len(operand) > 1:
                return True
            if operand.find("\'") == 0 \
                    and operand.rfind("\'") == len(operand) - 1 \
                    and len(operand) > 1:
                return True
            if operand in vars \
                    and vars[operand][1] == TypeVariable.phrase:
                return True
            name_var = worker.is_change_var(operand)
            if name_var is not None:
                if len(vars[name_var]) == 4:
                    if vars[name_var][3] == TypeVariable.phrase \
                            or vars[name_var][3] == TypeVariable.char:
                        return True
        return False

    @staticmethod
    def sum_operands(operands, vars, worker):
        res = 0
        is_str = Arithmetic.find_sum_strs(operands, vars, worker)
        if is_str:
            res = ""
        for operand in operands:
            if Arithmetic.isnumber(operand) and not is_str:
                res += float(operand)
                continue
            if operand in vars and not is_str \
                    and vars[operand][1] == TypeVariable.number:
                res += vars[operand][0]
                continue
            name_var, index = Arithmetic.get_name_var_and_index(
                operand, vars, worker)
            if name_var is not None and not is_str:
                if vars[name_var][3] == TypeVariable.number:
                    res += vars[name_var][0][index]
                else:
                    raise ArithmeticError("Operand is not a number: " +
                                          operand)
            elif not is_str:
                res += Arithmetic.get_val_by_method(operand, vars, worker)
            else:
                if operand in vars:
                    res += str(vars[operand][0])
                elif name_var is not None:
                    if vars[name_var][3] == TypeVariable.phrase \
                            or vars[name_var][3] == TypeVariable.char:
                        res += vars[name_var][0][index]
                    else:
                        raise ArithmeticError("Operand is not a number: " +
                                              operand)
                elif '\"' not in operand and "\'" not in operand \
                        and Arithmetic.isnumber(operand):
                    res += str(operand)
                elif '\"' == operand[0] and '\"' == operand[-1] \
                        or "\'" == operand[0] and "\'" == operand[-1]:
                    res += operand[1:-1]
                else:
                    name_method = worker.find_method(operand)
                    if name_method is not None:
                        if worker\
                                .classes[worker.current_class][name_method][1]\
                                is not None \
                                and worker\
                                .classes[worker.current_class][name_method][1]\
                                != TypeVariable.logic:
                            res += str(worker.call_method("", operand, vars))
                        else:
                            raise ValueError("Invalid type of value: " +
                                             operand)
                    else:
                        raise ArithmeticError("Can not understand a term: " +
                                              operand)
        return res

    @staticmethod
    def sub_operands(operands, vars, worker):
        res = None
        for i in range(0, len(operands)):
            if Arithmetic.isnumber(operands[i]):
                if i == 0:
                    res = float(operands[i])
                else:
                    res -= float(operands[i])
                continue
            if operands[i] in vars \
                    and vars[operands[i]][1] == TypeVariable.number:
                if i == 0:
                    res = vars[operands[i]][0]
                else:
                    res -= vars[operands[i]][0]
                continue
            name_var, index = Arithmetic.get_name_var_and_index(
                operands[i], vars, worker)
            if name_var is not None:
                if vars[name_var][3] == TypeVariable.number:
                    if i == 0:
                        res = vars[name_var][0][index]
                    else:
                        res -= vars[name_var][0][index]
                else:
                    raise ArithmeticError("Operand is not a number: " +
                                          operands[i])
            else:
                val = Arithmetic.get_val_by_method(operands[i], vars, worker)
                if i == 0:
                    res = val
                else:
                    res -= val
        return res

    @staticmethod
    def mult_operands(operands, vars, worker):
        res = 1
        for operand in operands:
            if Arithmetic.isnumber(operand):
                res *= float(operand)
                continue
            if operand in vars and \
                    vars[operand][1] == TypeVariable.number:
                res *= vars[operand][0]
                continue
            name_var, index = Arithmetic.get_name_var_and_index(
                operand, vars, worker)
            if name_var is not None:
                if vars[name_var][3] == TypeVariable.number:
                    res *= vars[name_var][0][index]
                else:
                    raise ArithmeticError("Operand is not a number: " +
                                          operand)
            else:
                res *= Arithmetic.get_val_by_method(operand, vars, worker)
        return res

    @staticmethod
    def div_operands(operands, vars, worker):
        res = None
        for i in range(0, len(operands)):
            if Arithmetic.isnumber(operands[i]):
                if i == 0:
                    res = float(operands[i])
                else:
                    res /= float(operands[i])
                continue
            if operands[i] in vars and \
                    vars[operands[i]][1] == TypeVariable.number:
                if i == 0:
                    res = vars[operands[i]][0]
                else:
                    res /= vars[operands[i]][0]
                continue
            name_var, index = Arithmetic.get_name_var_and_index(
                operands[i], vars, worker)
            if name_var is not None:
                if vars[name_var][3] == TypeVariable.number:
                    if i == 0:
                        res = vars[name_var][0][index]
                    else:
                        res /= vars[name_var][0][index]
                else:
                    raise ArithmeticError("Operand is not a number: " +
                                          operands[i])
            else:
                val = Arithmetic.get_val_by_method(operands[i], vars, worker)
                if i == 0:
                    res = val
                else:
                    res /= val
        return res

    @staticmethod
    def inc_or_dec(str, vars, worker, is_inc):
        name_var, index = Arithmetic.get_name_var_and_index(
            str, vars, worker)
        if name_var is None:
            raise ArithmeticError("Can not find the variable "
                                  "or the variable is not a number: " +
                                  str)
        if vars[name_var][2]:
            raise ArithmeticError(
                "Can not change value of a constant: " + name_var)
        if vars[name_var][1] != TypeVariable.number \
                and len(vars[name_var]) == 4 \
                and vars[name_var][3] != TypeVariable.number:
            raise ArithmeticError("This type of variable "
                                  "can not increment or decrement: " +
                                  name_var)
        if is_inc:
            if index is not None:
                vars[name_var][index] += 1
            else:
                vars[name_var] = (vars[name_var][0] + 1,
                                  TypeVariable.number, False)
        else:
            if index is not None:
                vars[name_var][index] -= 1
            else:
                vars[name_var][0] = (vars[name_var][0] - 1,
                                     TypeVariable.number, False)

    @staticmethod
    def solve_expression(expression, vars, worker):
        operation = Arithmetic.find_arithmetic_operation(expression)
        if operation == "Addition":
            if "got one more" in expression:
                name_var = expression[:len(expression) -
                                      len(" got one more")]
                Arithmetic.inc_or_dec(name_var, vars, worker, True)
                return vars[name_var][0]
            if expression.find("add") == 0 or expression.find("Add") == 0:
                expression = expression[4:]
            operands = re.split(r" and | plus | added to ", expression)
            return Arithmetic.sum_operands(operands, vars, worker)
        elif operation == "Subtraction":
            if "got one less" in expression:
                name_var = expression[:len(expression) -
                                      len(" got one more")]
                Arithmetic.inc_or_dec(name_var, vars, worker, False)
                return vars[name_var][0]
            if "subtract" in expression:
                expression = expression[len("subtract "):]
            elif "the difference between" in expression:
                expression = expression[len("the difference between "):]
            operands = re.split(r" and | minus | without | from ",
                                expression)
            return Arithmetic.sub_operands(operands, vars, worker)
        elif operation == "Multiplication":
            if "multiply" in expression:
                expression = expression[len("multiply "):]
            operands = re.split(r" and | times | multiplied with ",
                                expression)
            return Arithmetic.mult_operands(operands, vars, worker)
        elif operation == "Division":
            if expression.find("divided") == 0:
                expression = expression[len("divided "):]
            elif expression.find("divide") == 0:
                expression = expression[len("divide "):]
            operands = re.split(r" divided by | by | and ",
                                expression)
            return Arithmetic.div_operands(operands, vars, worker)
        return None
