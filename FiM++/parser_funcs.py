import re
from variables_types import TypeVariable
from arithmetic import Arithmetic
from comparison import Comparison


class ParserFuncs:
    @staticmethod
    def erase_article_from_start_str(str):
        if str.find(' ') == 1:
            return str[2:]
        if str.find(' ') == 3:
            return str[4:]
        return str

    @staticmethod
    def find_all_class_methods(sentences):
        classes = {}
        current_class = None
        for i in range(0, len(sentences)):
            if "Dear Princess Celestia" in sentences[i]:
                current_class = sentences[i + 1]
                classes[current_class] = {}
                i += 1
            elif "Today I learned" in sentences[i]:
                if current_class is None:
                    raise SyntaxError("Can not find class: " + sentences[i])
                name_main_method = sentences[i][len("Today I learned "):]
                if "about" in name_main_method:
                    name_main_method = name_main_method[len("about "):]
                classes[current_class][name_main_method] = (i, "main")
            elif "I learned" in sentences[i]:
                decl = sentences[i][len("I learned "):]
                name_method, type_return, args = \
                    ParserFuncs.parse_decl_of_method(decl)
                if name_method == "ErrorName":
                    raise SyntaxError("Invalid name method: " + sentences[i])
                if type_return == "ErrorTypeReturn":
                    raise TypeError("Invalid type of return: " +
                                    sentences[i])
                if args == "ErrorDeclArg":
                    raise SyntaxError("Invalid declaration of arguments: " +
                                      sentences[i])
                if args == "ErrorTypeArg":
                    raise TypeError("Invalid type of arguments: " +
                                    sentences[i])
                if args == "ErrorArgName":
                    raise SyntaxError("Invalid name(s) of arguments: " +
                                      sentences[i])
                classes[current_class][name_method] = (i, type_return, args)
        return classes

    @staticmethod
    def parse_decl_of_method(decl):
        if "about" in decl:
            decl = decl[len("about "):]
        has_with = False
        if "with" in decl or "to get" in decl:
            has_with = True
        has_using = False
        if "using" in decl:
            has_using = True
        parsed_decl = re.split(r" with | to get | using ", decl)
        if len(parsed_decl) == 0 or parsed_decl[0].find("with") == 0:
            return "ErrorName", None, None
        name_method = parsed_decl[0]
        parsed_decl.pop(0)
        type_return = None
        if has_with:
            type_return = TypeVariable.parse_type(
                ParserFuncs.erase_article_from_start_str(parsed_decl[0]))
            if type_return is None:
                return None, "ErrorTypeReturn", None
            parsed_decl.pop(0)
        args = None
        if has_using:
            args = {}
            parsed_args = re.split(r' and ', parsed_decl[0])
            for arg in parsed_args:
                arg = ParserFuncs.erase_article_from_start_str(arg)
                if arg.find(" ") == -1:
                    return None, None, "ErrorDeclArg"
                type_arg = TypeVariable.parse_type(arg[:arg.find(" ")])
                if type_arg is None:
                    return None, None, "ErrorTypeArg"
                name_arg = arg[arg.find(" ") + 1:]
                if not ParserFuncs.check_var_name(name_arg):
                    return None, None, "ErrorArgName"
                args[name_arg] = type_arg
        return name_method, type_return, args

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
    def parse_input(input):
        if ParserFuncs.isnumber(input):
            return float(input), TypeVariable.number
        if input == "yes" or input == "true" \
                or input == "right" or input == "correct":
            return True, TypeVariable.logic
        if input == "no" or input == "false" \
                or input == "wrong" or input == "incorrect":
            return False, TypeVariable.logic
        if len(input) == 1:
            return input, TypeVariable.char
        return input, TypeVariable.phrase

    @staticmethod
    def check_val_and_type(val, type):
        if type == TypeVariable.number:
            if not isinstance(val, str) and ParserFuncs.isnumber(val):
                return True
            return False
        if type == TypeVariable.logic:
            if isinstance(val, bool):
                return True
            return False
        if type == TypeVariable.char:
            if len(val) == 1:
                return True
            return False
        if type == TypeVariable.phrase:
            if ParserFuncs.isnumber(val) or isinstance(val, bool):
                return False
            return True
        return False

    @staticmethod
    def check_var_name(name):
        if "true" == name[0:4] or "false" == name[0:5] \
                or "True" == name[0:4] or "False" == name[0:5]:
            return False
        reg_exp = r"(\d+|\"|\'|Dear|" \
                  r"I|is|are|has|have" \
                  r"|likes|liked|like|was|were)"
        if re.search(reg_exp, name) is not None:
            return False
        return True

    @staticmethod
    def get_val_by_str_and_type(string, type, vars, worker):
        val = ParserFuncs.get_val_by_str(string, vars, worker)
        if val is None:
            return "ErrorValue", None
        if type == "number":
            if ParserFuncs.isnumber(val):
                return val, TypeVariable.number
            return "ErrorValue", None
        if type == "letter" or type == "character":
            if isinstance(val, str) and len(val) == 1:
                return val, TypeVariable.char
            return "ErrorValue", None
        if type == "word" or type == "phrase" or type == "name" \
                or type == "sentence" or type == "quote":
            if isinstance(val, str):
                return val, TypeVariable.phrase
            return "ErrorValue", None
        if type == "logic" or type == "argument":
            if isinstance(val, bool):
                return val, TypeVariable.logic
            return "ErrorValue", None
        return "ErrorType", None

    @staticmethod
    def get_val_by_str(val, vars, worker):
        if val in vars:
            return vars[val][0]
        name_var = worker.is_change_var(val)
        if name_var is not None:
            return_val = ParserFuncs.get_val_in_array(val, name_var, vars, worker)
            if return_val == "ErrorIndex":
                return None
            if return_val is not None:
                return return_val
        if ParserFuncs.isnumber(val):
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
        if solution is None:
            name_method = worker.find_method(val)
            if name_method is None:
                solution_logic = Comparison\
                    .solve_expression(val, vars, worker)
                if solution_logic is not None:
                    return solution_logic
            elif name_method is not None:
                returned_val = worker.call_method("", val, vars)
                if returned_val is not None:
                    return returned_val
        else:
            return solution
        return None

    @staticmethod
    def parse_array_val(str, type_vals, vars, worker):
        array = []
        if str == '':
            return array
        vals = re.split(r" and ", str)
        for str_val in vals:
            val = ParserFuncs.get_val_by_str(str_val, vars, worker)
            if TypeVariable.get_type_by_val(val) != type_vals:
                return "ValueError"
            array.append(val)
        return array

    @staticmethod
    def get_sentences_by_split_text(split_text):
        sentences = []
        for fragment in split_text:
            if fragment == '':
                continue
            sentences.append(fragment.strip())
        return sentences

    @staticmethod
    def get_val_in_array(str, name_var, vars, worker):
        if name_var not in vars:
            return None
        if vars[name_var][1].value < TypeVariable.arrayNumbers.value:
            return None
        index_str = str[len(name_var) + 1:]
        index = ParserFuncs.get_val_by_str(index_str, vars, worker)
        if not ParserFuncs.isint(index):
            return "ErrorIndex"
        index = int(index) - 1
        if index < 0 or index >= len(vars[name_var][0]):
            return "ErrorIndex"
        return vars[name_var][0][index]

    @staticmethod
    def split_lines_by_sentences(lines):
        text = ''
        is_comment = False
        for line in lines:
            if line == '':
                continue
            if "P." in line:
                new_line = line[:line.find("P.") - 1]
            else:
                new_line = line
            if '(' in new_line and ')' in new_line:
                text += new_line[:new_line.find("(")] + \
                        new_line[new_line.find(")") + 1:].lstrip()
            elif '(' in new_line and ')' not in new_line:
                text += new_line[:new_line.find("(")]
                is_comment = True
            elif is_comment and ')' in new_line:
                text += new_line[new_line.find(")") + 1:].lstrip()
                is_comment = False
            elif is_comment and ')' not in new_line:
                continue
            else:
                text += new_line
        split_text = re.findall(r'''((?:[^\.!\?:"]|"[^"]*"|'[^']*')+)''',
                                text)
        return ParserFuncs.get_sentences_by_split_text(split_text)
