import parser_funcs
from worker import Worker


class Program:
    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            text = f.read().split('\n')
        self.sentences = parser_funcs.ParserFuncs\
            .split_lines_by_sentences(text)
        self.classes = parser_funcs.ParserFuncs\
            .find_all_class_methods(self.sentences)
        self.worker = Worker()

    def find_main_method(self):
        class_name, method_name, index = "", "", 0
        for name_class in self.classes:
            for name_method in self.classes[name_class]:
                if self.classes[name_class][name_method][1] == "main":
                    if class_name == "":
                        class_name = name_class
                        method_name = name_method
                        index = self.classes[name_class][name_method][0]
                    else:
                        raise SyntaxError("Found several main methods")
        if class_name == "":
            raise SyntaxError("Can not find main method")
        return class_name, method_name, index

    def find_end_if(self, current_pos):
        i = current_pos
        stack = []
        while self.sentences[i].find("That's all") == -1:
            if self.sentences[i].find("If") == 0 \
                    or self.sentences[i].find("When") == 0:
                stack.append("If")
            elif self.sentences[i].find("Otherwise") == 0 \
                    or self.sentences[i].find("Or else") == 0 \
                    or self.sentences[i] == "That\'s what I would do":
                if self.sentences[i].find("Otherwise") == 0 \
                        or self.sentences[i].find("Or else") == 0:
                    if len(stack) == 1:
                        return i
                else:
                    if len(stack) == 1:
                        return i
                    stack.pop()
            i += 1
        raise SyntaxError("Can not find end of if: " +
                          self.sentences[current_pos])

    def find_end_else(self, current_pos):
        i = current_pos + 1
        stack = ["if"]
        while self.sentences[i].find("That's all") == -1:
            if self.sentences[i].find("If") == 0 \
                    or self.sentences[i].find("When") == 0:
                stack.append("If")
            elif self.sentences[i].find("Otherwise") == 0 \
                    or self.sentences[i].find("Or else") == 0 \
                    or self.sentences[i] == "That\'s what I would do":
                if self.sentences[i].find("Otherwise") == 0 \
                        or self.sentences[i].find("Or else") == 0:
                    if len(stack) == 1:
                        raise SyntaxError("\"Else\" can not end with "
                                          "declaration of other \"Else\": " +
                                          self.sentences[current_pos])
                else:
                    if len(stack) == 1:
                        return i
                    stack.pop()
            i += 1
        raise SyntaxError("Can not find end of else: " +
                          self.sentences[current_pos])

    def find_end_loop(self, current_pos):
        i = current_pos
        count_loops = 0
        while self.sentences[i].find("That's all") == -1:
            if self.sentences[i].find("As long as") == 0 \
                    or self.sentences[i].find("For every") == 0:
                count_loops += 1
            elif self.sentences[i] == "That\'s what I did":
                count_loops -= 1
                if count_loops == 0:
                    return i
            i += 1
        raise SyntaxError("Can not find end of loop: " +
                          self.sentences[current_pos])

    def find_next_case_switch(self, current_pos):
        i = current_pos + 1
        while self.sentences[i].find("That's all") == -1:
            if self.sentences[i].find("On the") == 0 \
                    or self.sentences[i] == "That\'s what I did" \
                    or self.sentences[i] == "If all else fails":
                return i
            i += 1
        raise SyntaxError("Next case or end of switch not found: " +
                          self.sentences[current_pos])

    def find_end_switch(self, current_pos):
        i = current_pos
        while self.sentences[i].find("That's all") == -1:
            if self.sentences[i] == "That\'s what I did":
                return i
            i += 1
        raise SyntaxError("End of switch not found: " +
                          self.sentences[current_pos])

    def run(self):
        current_class, current_method, i = self.find_main_method()
        self.worker.set_up(current_class, current_method, self.classes, self)
        loops = []
        i += 1
        while i < len(self.sentences):
            if self.worker.current_method is None:
                return
            returned_val = self.worker.execute_sentence(self.sentences[i])
            if returned_val is not None:
                if returned_val[0] == "if":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_end_if(i)
                    continue
                if returned_val[0] == "else":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_end_else(i) + 1
                    continue
                if returned_val[0] == "while" or returned_val[0] == "for":
                    if returned_val[1]:
                        loops.append(i)
                        i += 1
                    else:
                        i = self.find_end_loop(i) + 1
                    continue
                if returned_val[0] == "end loop":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = loops.pop()
                    continue
                if returned_val[0] == "do while":
                    loops.append(i)
                    i += 1
                    continue
                if returned_val[0] == "end do while":
                    index = loops.pop()
                    if self.sentences[index] != "Here\'s what I did":
                        raise SyntaxError("Invalid start of loop "
                                          "\"Do While\": " +
                                          self.sentences[index])
                    if returned_val[1]:
                        i = index
                    else:
                        i += 1
                    continue
                if returned_val[0] == "switch":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_next_case_switch(i)
                    continue
                if returned_val[0] == "end switch":
                    i = self.find_end_switch(i)
                    continue
            i += 1

    def execute_method(self, current_class, name_method):
        i = self.classes[current_class][name_method][0]
        loops = []
        while i < len(self.sentences):
            if self.worker.current_method != name_method:
                return
            returned_val = self.worker.execute_sentence(self.sentences[i])
            if returned_val is not None:
                if returned_val[0] == "return":
                    return returned_val[1]
                if returned_val[0] == "if":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_end_if(i)
                    continue
                if returned_val[0] == "else":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_end_else(i) + 1
                    continue
                if returned_val[0] == "while" or returned_val[0] == "for":
                    if returned_val[1]:
                        loops.append(i)
                        i += 1
                    else:
                        i = self.find_end_loop(i) + 1
                    continue
                if returned_val[0] == "end loop":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = loops.pop()
                    continue
                if returned_val[0] == "do while":
                    loops.append(i)
                    i += 1
                    continue
                if returned_val[0] == "end do while":
                    index = loops.pop()
                    if self.sentences[index] != "Here\'s what I did":
                        raise SyntaxError("Invalid start of loop "
                                          "\"Do While\": " +
                                          self.sentences[index])
                    if returned_val[1]:
                        i = index
                    else:
                        i += 1
                    continue
                if returned_val[0] == "switch":
                    if returned_val[1]:
                        i += 1
                    else:
                        i = self.find_next_case_switch(i)
                    continue
                if returned_val[0] == "end switch":
                    i = self.find_end_switch(i)
                    continue
            i += 1
