import re
from parser import Parser
from variables_types import TypeVariable
from arithmetic import Arithmetic
from comparison import Comparison


class Worker:
    def __init__(self):
        self.tokens = {
            "That's all": self.end_method,
            "I said": self.output,
            "I wrote": self.output,
            "I sang": self.output,
            "I thought": self.output,
            "I read": self.input,
            "I heard": self.input,
            "I asked": self.prompt,
            "Did you know that": self.add_var,
            "I learned": self.init_method,
            "I would": self.call_method,
            "I remember": self.call_method,
            "Then you get": self.return_val,
            "If all else fails": self.default_case,
            "If": self.if_condition,
            "When": self.if_condition,
            "That\'s what I would do": self.end_if,
            "Or else": self.else_condition,
            "Otherwise": self.else_condition,
            "In regards to": self.switch,
            "On the": self.case_switch,
            "As long as": self.loop_while,
            "Here\'s what I did while": self.loop_while,
            "Here\'s what I did": self.loop_do_while,
            "I did this while": self.end_loop_do_while,
            "I did this as long as": self.end_loop_do_while,
            "For every": self.loop_for,
            "That\'s what I did": self.end_loop
        }
        self.program = None
        self.current_class = ""
        self.current_method = ""
        self.vars = {}
        self.classes = {}
        self.buffer = {}
        self.is_switch = False

    def set_up(self, start_class, main_method, classes, program=None):
        self.program = program
        self.current_class = start_class
        self.current_method = main_method
        self.vars = {self.current_method: {}}
        self.classes = classes
        self.buffer = {"ifs": {}, "loops": {}}

    def find_token(self, sentence):
        for token in self.tokens:
            if sentence.find(token) == 0:
                return token
        return None

    def is_change_var(self, sentence):
        for name_var in self.vars[self.current_method]:
            if sentence.find(name_var) == 0:
                return name_var
        return None

    def find_method(self, sentence):
        for name_method in self.classes[self.current_class]:
            if name_method in sentence:
                return name_method
        return None

    def execute_sentence(self, sentence):
        if self.current_method not in self.vars:
            self.vars[self.current_method] = {}
        token = self.find_token(sentence)
        if token is None and not self.is_switch:
            if "got one more" in sentence:
                self.increment_or_decrement(sentence,
                                            self.vars[self.current_method],
                                            True)
            elif "got one less" in sentence:
                self.increment_or_decrement(sentence,
                                            self.vars[self.current_method],
                                            False)
            else:
                name_var = self.is_change_var(sentence)
                if name_var is not None:
                    self.change_var(sentence, name_var,
                                    self.vars[self.current_method])
                else:
                    raise SyntaxError("Invalid sentence: " + sentence)
        elif token is None and self.is_switch:
            raise SyntaxError("Declared switch, but the variant "
                              "of the variable value not found: " +
                              sentence)
        else:
            if self.tokens[token] is None:
                return
            if self.is_switch and token != "On the" \
                    and token != "If all else fails":
                raise SyntaxError("Declared switch, but the variant "
                                  "of the variable value not found: " +
                                  sentence)
            returned_val = self.tokens[token](token, sentence,
                                              self.vars[self.current_method])
            if returned_val is None:
                return
            else:
                return returned_val

    def output(self, token, sentence, vars):
        print_text = sentence[len(token) + 1:]
        val = Parser.get_val_by_str(print_text, vars, self)
        if val is None:
            val = "nothing"
        print(val)

    def input(self, token, sentence, vars, prompt=""):
        name_var = sentence[len(token) + 1:]
        if not Parser.check_var_name(name_var):
            raise SyntaxError("Invalid name of variable: " + sentence)
        val, type = Parser.parse_input(input(prompt))
        vars[name_var] = (val, type, False)

    def prompt(self, token, sentence, vars):
        if "\"" not in sentence:
            self.input(token, sentence, vars)
        else:
            prompt = sentence[sentence.find("\"") + 1: -1] + " "
            sentence = sentence[:sentence.find("\"") - 1]
            self.input(token, sentence, vars, prompt)

    def end_method(self, token, sentence, vars):
        name_method = sentence[len(token) + 1:]
        if "about" in name_method:
            name_method = name_method[len("about "):]
        if name_method != self.current_method:
            raise SyntaxError("Unexpected name of method: " + sentence)
        vars.clear()
        self.current_method = None

    def add_var(self, token, sentence, vars):
        reg_exp = r"Did you know that (.*?)( always |\s)" \
                  r"(is|are|was|were|have|has|had|likes|liked|like)" \
                  r"( always the | always an | always a " \
                  r"| always | many | the | an | a |\s)" \
                  r"(.*?)(\Z|\s)(.*?)$"
        var_data = re.findall(reg_exp, sentence)
        if len(var_data) == 0 or len(var_data[0]) > 8:
            raise SyntaxError("Invalid declaration of variable: " + sentence)
        if not Parser.check_var_name(var_data[0][0]):
            raise NameError("Invalid name of variable: " + sentence)
        is_const = False
        if "always" in var_data[0][1] or "always" in var_data[0][3]:
            is_const = True
        type = TypeVariable.parse_type(var_data[0][4])
        if type is None:
            raise TypeError("Invalid type of variable: " + sentence)
        type_vals = None
        if type == TypeVariable.arrayLogic:
            type_vals = TypeVariable.logic
        elif type == TypeVariable.arrayChars:
            type_vals = TypeVariable.char
        elif type == TypeVariable.arrayPhrases:
            type_vals = TypeVariable.phrase
        elif type == TypeVariable.arrayNumbers:
            type_vals = TypeVariable.number
        if var_data[0][3] == " many " or type_vals is not None:
            if type_vals is None:
                raise TypeError("The type of variable is not a array: " +
                                sentence)
            val = Parser.parse_array_val(var_data[0][6], type_vals,
                                         vars, self)
            if val == "ValueError":
                raise ValueError("Invalid values of array: " + sentence)
            if is_const and val == []:
                raise ValueError("Const should have a value: " + sentence)
            vars[var_data[0][0]] = (val, type, is_const, type_vals)
            return
        if var_data[0][6] != '':
            val, type = Parser.get_val_by_str_and_type(
                var_data[0][6], var_data[0][4], vars, self)
            if val == "ErrorValue":
                raise ValueError("Invalid value for this type: " + sentence)
            if val == "ErrorType":
                raise TypeError("Invalid type of variable: " + sentence)
            vars[var_data[0][0]] = (val, type, is_const)
        else:
            if is_const:
                raise ValueError("Const should have a value: " + sentence)
            type = TypeVariable.parse_type(var_data[0][4])
            if type is None:
                raise TypeError("Invalid type of variable: " + sentence)
            vars[var_data[0][0]] = (None, type, is_const)

    def change_var(self, sentence, name_var, vars):
        parsed_sentence = re.split(r" is now | are now | now like "
                                   r"| now likes | now become "
                                   r"| now becomes | become | becomes ",
                                   sentence)
        if len(parsed_sentence) < 2:
            raise SyntaxError("Invalid declaration of change variable: " +
                              sentence)
        if parsed_sentence[0] not in vars and name_var in parsed_sentence[0] \
                and name_var != parsed_sentence[0]:
            if vars[name_var][1].value < TypeVariable.arrayNumbers.value:
                raise TypeError("The variable is not a array: " + sentence)
            index_str = parsed_sentence[0][len(name_var) + 1:]
            index = Parser.get_val_by_str(index_str, vars, self)
            if not Parser.isint(index):
                raise IndexError("Index must be integer: " + sentence)
            index = int(index) - 1
            if index < 0 or index > len(vars[name_var][0]):
                raise IndexError("Index out of range: " + sentence)
            val = Parser.get_val_by_str(parsed_sentence[1], vars, self)
            type = vars[name_var][3]
            if val is None:
                raise ValueError("Unexpected value: " + sentence)
            if not Parser.check_val_and_type(val, type):
                raise ValueError("Invalid type of value: " + sentence)
            if index == len(vars[name_var][0]):
                vars[name_var][0].append(val)
            else:
                vars[name_var][0][index] = val
            return
        elif parsed_sentence[0] not in vars:
            raise NameError("The variable not found: " + sentence)
        if vars[parsed_sentence[0]][2]:
            raise ValueError("Can not change value by const: " + sentence)
        val = Parser.get_val_by_str(parsed_sentence[1], vars, self)
        type = vars[parsed_sentence[0]][1]
        if val is None:
            raise ValueError("Unexpected value: " + sentence)
        if not Parser.check_val_and_type(val, type):
            raise ValueError("Invalid type of value: " + sentence)
        vars[parsed_sentence[0]] = (val, type, False)

    def increment_or_decrement(self, sentence, vars, is_increment):
        if is_increment:
            name_var = sentence[:len(sentence) - len("got one more") - 1]
        else:
            name_var = sentence[:len(sentence) - len("got one less") - 1]
        if name_var not in vars:
            raise NameError("Can not find the variable: " + sentence)
        if vars[name_var][2]:
            raise ValueError("Can not change value by const: " + sentence)
        if vars[name_var][1] != TypeVariable.number:
            raise ArithmeticError("Can not increment or decrement "
                                  "not a number: " + sentence)
        val = vars[name_var][0]
        type = vars[name_var][1]
        if is_increment:
            vars[name_var] = (val + 1, type, False)
        else:
            vars[name_var] = (val - 1, type, False)

    def init_method(self, token, sentence, vars):
        needed_vars = self.classes[self.current_class][self.current_method][2]
        if needed_vars is None:
            return
        index_var = 0
        for name_var in needed_vars:
            if self.buffer["args"][index_var][1] != needed_vars[name_var]:
                raise TypeError("Invalid type of argument: " + sentence)
            val, type, is_const = self.buffer["args"][index_var]
            vars[name_var] = (val, type, False)
            index_var += 1
        self.buffer["args"].clear()

    def call_method(self, token, sentence, vars):
        decl = sentence
        if token != "":
            decl = sentence[len(token) + 1:]
            if Arithmetic.change_var(decl, vars, self):
                return
        name_method = decl
        if "using" in decl:
            parsed_decl = re.split(r" using ", decl)
            name_method = parsed_decl[0]
            if name_method not in self.classes[self.current_class]:
                raise NameError("Can find method: " + sentence)
            using_vars = re.split(r" and ", parsed_decl[1])
            self.buffer["args"] = []
            for name_var in using_vars:
                if name_var in vars:
                    self.buffer["args"].append(vars[name_var])
                else:
                    val = Parser.get_val_by_str(name_var, vars, self)
                    if val is None:
                        raise ValueError("Invalid value of argument: " +
                                         sentence)
                    type = TypeVariable.get_type_by_val(val)
                    self.buffer["args"].append((val, type, False))
        if name_method not in self.classes[self.current_class]:
            raise NameError("Can find method: " + sentence)
        called_method = self.current_method
        self.current_method = name_method
        val = self.program.execute_method(self.current_class, name_method)
        self.current_method = called_method
        return val

    def return_val(self, token, sentence, vars):
        if self.classes[self.current_class][self.current_method][1] is None:
            raise SyntaxError("This method does not return anything: " +
                              sentence)
        val_str = sentence[len(token) + 1:]
        val = Parser.get_val_by_str(val_str, vars, self)
        type_val = TypeVariable.get_type_by_val(val)
        if type_val != self\
                .classes[self.current_class][self.current_method][1]:
            raise TypeError("Invalid type of return value: " + sentence)
        vars.clear()
        return "return", val

    def if_condition(self, token, sentence, vars):
        expr = sentence[len(token) + 1:]
        if "then" not in expr:
            raise SyntaxError("Invalid declaration of condition: " +
                              sentence)
        expr = expr[:expr.find(" then")]
        val_expr = Comparison.solve_expression(expr, vars, self)
        if val_expr is None:
            raise SyntaxError("Invalid expression: " + sentence)
        if self.current_method not in self.buffer["ifs"]:
            self.buffer["ifs"][self.current_method] = []
        if val_expr:
            self.buffer["ifs"][self.current_method].append("if")
            return "if", True
        self.buffer["ifs"][self.current_method].append("else")
        return "if", False

    def else_condition(self, token, sentence, vars):
        if self.current_method not in self.buffer["ifs"]:
            raise SyntaxError("\"If\" not found: " + sentence)
        condition_was = self.buffer["ifs"][self.current_method].pop()
        if condition_was == "if":
            return "else", False
        return "else", True

    def end_if(self, token, sentence, vars):
        if self.current_method not in self.buffer["ifs"]:
            raise SyntaxError("\"If\" not found: " + sentence)
        if len(self.buffer["ifs"][self.current_method]) % 2 == 1:
            self.buffer["ifs"][self.current_method].pop()

    def switch(self, token, sentence, vars):
        var_name = sentence[len(token) + 1:]
        if var_name not in vars:
            raise NameError("The variable not found: " + sentence)
        if vars[var_name][1] != TypeVariable.number:
            raise TypeError("The variable must be a number: " + sentence)
        self.is_switch = True
        if self.current_method not in self.buffer["loops"]:
            self.buffer["loops"][self.current_method] = []
        self.buffer["loops"][self.current_method].append(("switch",
                                                          var_name,
                                                          False))

    def case_switch(self, token, sentence, vars):
        if self.current_method not in self.buffer["loops"] \
                or len(self.buffer["loops"][self.current_method]) == 0 \
                or not isinstance(self
                                  .buffer["loops"][self.current_method][-1],
                                  tuple) \
                or self.buffer["loops"][self.current_method][-1][0] \
                != "switch":
            raise SyntaxError("Found case, but switch not found: " + sentence)
        if self.buffer["loops"][self.current_method][-1][2]:
            return "end switch", True
        decl = sentence[len(token) + 1:]
        if "hoof" not in decl:
            raise SyntaxError("Invalid declaration of case: " + sentence)
        str_val = decl[:decl.find(" hoof")]
        if str_val.find("st") == len(str_val) - 2 \
                or str_val.find("nd") == len(str_val) - 2 \
                or str_val.find("rd") == len(str_val) - 2 \
                or str_val.find("th") == len(str_val) - 2:
            str_val = str_val[:-2]
        val = Parser.get_val_by_str(str_val, vars, self)
        if not isinstance(val, float):
            raise ValueError("Value of case must be a number: " + sentence)
        name_var = self.buffer["loops"][self.current_method][-1][1]
        if val == vars[name_var][0]:
            self.buffer["loops"][self.current_method][-1] = \
                ("switch", name_var, True)
            self.is_switch = False
            return "switch", True
        return "switch", False

    def default_case(self, token, sentence, vars):
        if self.current_method not in self.buffer["loops"] \
                or len(self.buffer["loops"][self.current_method]) == 0 \
                or not isinstance(self
                                  .buffer["loops"][self.current_method][-1],
                                  tuple) \
                or self.buffer["loops"][self.current_method][-1][0] \
                != "switch":
            raise SyntaxError("Found default case, but switch not found: " +
                              sentence)
        if self.buffer["loops"][self.current_method][-1][2]:
            return "end switch", True
        name_var = self.buffer["loops"][self.current_method][-1][1]
        self.buffer["loops"][self.current_method][-1] = \
            ("switch", name_var, True)
        self.is_switch = False

    def loop_while(self, token, sentence, vars):
        expr = sentence[len(token) + 1:]
        val = Comparison.solve_expression(expr, vars, self)
        if val is None:
            raise SyntaxError("Invalid expression: " + sentence)
        if self.current_method not in self.buffer["loops"]:
            self.buffer["loops"][self.current_method] = []
        if val:
            self.buffer["loops"][self.current_method].append("while")
            return "while", True
        return "while", False

    def end_loop(self, token, sentence, vars):
        if self.current_method not in self.buffer["loops"]:
            raise SyntaxError("Start loop not found: " + sentence)
        if len(self.buffer["loops"][self.current_method]) == 0:
            return "end loop", True
        last_loop = self.buffer["loops"][self.current_method].pop()
        if last_loop == "while":
            return "end loop", False
        if isinstance(last_loop, tuple) and last_loop[0] == "for" \
                and isinstance(last_loop[3], bool):
            if last_loop[3]:
                delta = -1
            else:
                delta = 1
            if vars[last_loop[1]][1] == TypeVariable.char:
                vars[last_loop[1]] = (chr(ord(vars[last_loop[1]][0]) + delta),
                                      TypeVariable.char, False)
            else:
                vars[last_loop[1]] = (vars[last_loop[1]][0] + delta,
                                      TypeVariable.number, False)
            self.buffer["loops"][self.current_method].append(last_loop)
            return "end loop", False
        if isinstance(last_loop, tuple) and last_loop[0] == "for":
            index = last_loop[3] + 1
            if index == len(last_loop[2]):
                return "end loop", True
            vars[last_loop[1]] = (last_loop[2][index],
                                  vars[last_loop[1]][1], False)
            self.buffer["loops"][self.current_method]\
                .append(("for", last_loop[1], last_loop[2], index))
            return "end loop", False
        return "end loop", True

    def loop_do_while(self, token, sentence, vars):
        if token == sentence:
            return "do while", None
        raise SyntaxError("Invalid start of the loop: " + sentence)

    def end_loop_do_while(self, token, sentence, vars):
        expr = sentence[len(token) + 1:]
        val = Comparison.solve_expression(expr, vars, self)
        if val is None:
            raise SyntaxError("Invalid expression: " + sentence)
        if val:
            return "end do while", True
        return "end do while", False

    def loop_for(self, token, sentence, vars):
        if self.current_method in self.buffer["loops"] \
                and len(self.buffer["loops"][self.current_method]) > 0 \
                and isinstance(self.buffer["loops"][self.current_method][-1],
                               tuple) \
                and self.buffer["loops"][self.current_method][-1][0] == "for":
            if not isinstance(self.buffer["loops"][self.current_method][-1][3],
                              bool):
                return "for", True
            name_var = self.buffer["loops"][self.current_method][-1][1]
            r_bound = self.buffer["loops"][self.current_method][-1][2]
            is_rev = self.buffer["loops"][self.current_method][-1][3]
            if vars[name_var][1] == TypeVariable.char:
                if ord(vars[name_var][0]) > r_bound and not is_rev \
                        or ord(vars[name_var][0]) < r_bound and is_rev:
                    self.buffer["loops"][self.current_method].pop()
                    return "for", False
                return "for", True
            if vars[name_var][0] > r_bound and not is_rev \
                    or vars[name_var][0] < r_bound and is_rev:
                self.buffer["loops"][self.current_method].pop()
                vars.pop(name_var)
                return "for", False
            return "for", True
        decl = sentence[len(token) + 1:]
        type = TypeVariable.parse_type(decl[:decl.find(" ")])
        if type is None:
            raise TypeError("Invalid type of loop: " + sentence)
        decl = decl[decl.find(" ") + 1:]
        if "from" in decl and "to" in decl:
            split_decl = re.split(r" from | to ", decl)
            if len(split_decl) != 3:
                raise SyntaxError("Invalid declaration of loop: " +
                                  sentence)
            if split_decl[0] not in vars:
                if not Parser.check_var_name(split_decl[0]):
                    raise NameError("Invalid name of variable: " + sentence)
                l_bound = Parser.get_val_by_str(split_decl[1], vars, self)
                r_bound = Parser.get_val_by_str(split_decl[2], vars, self)
                if type == TypeVariable.number:
                    if l_bound is None or r_bound is None \
                            or not isinstance(l_bound, float) \
                            or not isinstance(r_bound, float):
                        raise ValueError("Invalid boundaries of loop: " +
                                         sentence)
                    vars[split_decl[0]] = (l_bound, type, False)
                elif type == TypeVariable.char:
                    if not Parser.isint(l_bound) and len(l_bound) > 1 \
                            or not Parser.isint(r_bound) and len(r_bound) > 1:
                        raise ValueError("Invalid boundaries of loop: " +
                                         sentence)
                    if Parser.isint(l_bound):
                        vars[split_decl[0]] = (chr(int(l_bound)), type, False)
                    else:
                        vars[split_decl[0]] = (l_bound, type, False)
                        l_bound = ord(l_bound)
                    if not Parser.isint(r_bound):
                        r_bound = ord(r_bound)
                else:
                    raise TypeError("Unsupported type of loop: " + sentence)
                is_reversed = False
                if l_bound > r_bound:
                    is_reversed = True
                if self.current_method not in self.buffer["loops"]:
                    self.buffer["loops"][self.current_method] = []
                self.buffer["loops"][self.current_method]\
                    .append(("for", split_decl[0], r_bound, is_reversed))
                return "for", True
            else:
                raise NameError("A variable with the same name "
                                "already exists: " + sentence)
        elif "in" in decl:
            split_decl = re.split(r" in ", decl)
            if split_decl[0] not in vars:
                if not Parser.check_var_name(split_decl[0]):
                    raise NameError("Invalid name of variable: " + sentence)
                iter_obj = Parser.get_val_by_str(split_decl[1], vars, self)
                if iter_obj is None \
                        or not isinstance(iter_obj, list) \
                        and not isinstance(iter_obj, str):
                    raise ValueError("Invalid the iterating object: " +
                                     sentence)
                if len(iter_obj) == 0:
                    return "for", False
                if isinstance(iter_obj, list):
                    type_iter_elem = TypeVariable.get_type_by_val(iter_obj[0])
                else:
                    type_iter_elem = TypeVariable.char
                if type != type_iter_elem:
                    raise TypeError("Type of iterating variable and "
                                    "iterating value does not match: " +
                                    sentence)
                vars[split_decl[0]] = (iter_obj[0], type_iter_elem, False)
                if self.current_method not in self.buffer["loops"]:
                    self.buffer["loops"][self.current_method] = []
                self.buffer["loops"][self.current_method] \
                    .append(("for", split_decl[0], iter_obj, 0))
                return "for", True
            else:
                raise NameError("A variable with the same name "
                                "already exists: " + sentence)
        else:
            raise SyntaxError("Invalid declaration of loop \"For\": " +
                              sentence)
