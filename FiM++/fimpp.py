import sys
from program import Program
from interpreter import Interpreter


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 2:
        raise SyntaxError("Found more arguments than needed")
    if len(args) == 2:
        if args[1] == "-h" or args[1] == "--help":
            print("Usage: fimpp.py [NONE/path]\n")
            print("Interpreter FiM++. Version 1.0\n")
            print("Optional argument:")
            print("  NONE\t\trun the interpreter "
                  "in the mode \"step-by-step\"")
            print("  path\t\tinterpreter execute file with code\n")
            print("Author: Vasilev Ilya <bkmz1840@gmail.com>")
        else:
            program = Program(args[1])
            program.run()
    else:
        interpreter = Interpreter()
        interpreter.run()
