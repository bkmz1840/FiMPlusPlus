from enum import Enum


class TypeVariable(Enum):
    number = 1
    logic = 2
    char = 3
    phrase = 4
    arrayNumbers = 5
    arrayLogic = 6
    arrayChars = 7
    arrayPhrases = 8

    @staticmethod
    def parse_type(type):
        if type == "number":
            return TypeVariable.number
        if type == "letter" or type == "character":
            return TypeVariable.char
        if type == "word" or type == "phrase" or type == "name" \
                or type == "sentence" or type == "quote":
            return TypeVariable.phrase
        if type == "logic" or type == "argument":
            return TypeVariable.logic
        if type == "numbers":
            return TypeVariable.arrayNumbers
        if type == "letters" or type == "characters":
            return TypeVariable.arrayChars
        if type == "words" or type == "phrases" or type == "names" \
                or type == "sentences" or type == "quotes":
            return TypeVariable.arrayPhrases
        if type == "arguments":
            return TypeVariable.arrayLogic
        return None

    @staticmethod
    def get_type_by_val(val):
        if val is None:
            return None
        if isinstance(val, bool):
            return TypeVariable.logic
        if isinstance(val, float) or isinstance(val, int):
            return TypeVariable.number
        if len(val) == 1:
            return TypeVariable.char
        return TypeVariable.phrase
