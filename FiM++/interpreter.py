from worker import Worker


class Interpreter:
    def __init__(self):
        self.worker = Worker()
        self.classes = {"Interpreter": {"very much new": (2, "main")}}

    def run(self):
        self.worker.set_up("Interpreter", "very much new", self.classes)
        print("Dear Princess Celestia: Interpreter.")
        print("Today I learned very much new.")
        while True:
            try:
                current_sentence = input(">>> ")
                if "." != current_sentence[-1] \
                        and "!" != current_sentence[-1] \
                        and "?" != current_sentence[-1] \
                        and ":" != current_sentence[-1]:
                    raise SyntaxError("It is not a sentence: " +
                                      current_sentence)
                if current_sentence == "That\'s all very much new.":
                    print("Your faithful student, programmer!")
                    break
                self.worker.execute_sentence(current_sentence[:-1])
            except Exception as ex:
                print(str(ex) + "\n")
