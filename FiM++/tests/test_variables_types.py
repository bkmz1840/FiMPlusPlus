import unittest
from variables_types import TypeVariable


class TestTypeVariable(unittest.TestCase):
    def test_parse_type(self):
        t1 = "number"
        t2 = "numbers"
        t3 = "logic"
        t4 = "logics"
        t5 = "argument"
        t6 = "arguments"
        t7 = "phrases"
        t8 = "phrase"
        t9 = "character"
        t10 = "characters"
        t11 = "letter"
        t12 = "letters"
        self.assertEqual(TypeVariable.number, TypeVariable.parse_type(t1))
        self.assertEqual(TypeVariable.arrayNumbers,
                         TypeVariable.parse_type(t2))
        self.assertEqual(TypeVariable.logic, TypeVariable.parse_type(t3))
        self.assertIsNone(TypeVariable.parse_type(t4))
        self.assertEqual(TypeVariable.logic, TypeVariable.parse_type(t5))
        self.assertEqual(TypeVariable.arrayLogic,
                         TypeVariable.parse_type(t6))
        self.assertEqual(TypeVariable.arrayPhrases,
                         TypeVariable.parse_type(t7))
        self.assertEqual(TypeVariable.phrase, TypeVariable.parse_type(t8))
        self.assertEqual(TypeVariable.char, TypeVariable.parse_type(t9))
        self.assertEqual(TypeVariable.arrayChars,
                         TypeVariable.parse_type(t10))
        self.assertEqual(TypeVariable.char, TypeVariable.parse_type(t11))
        self.assertEqual(TypeVariable.arrayChars,
                         TypeVariable.parse_type(t12))

    def test_get_type_by_val(self):
        v1 = None
        v2 = 10.0
        v3 = "Hello"
        v4 = "A"
        v5 = False
        self.assertIsNone(TypeVariable.get_type_by_val(v1))
        self.assertEqual(TypeVariable.number,
                         TypeVariable.get_type_by_val(v2))
        self.assertEqual(TypeVariable.phrase,
                         TypeVariable.get_type_by_val(v3))
        self.assertEqual(TypeVariable.char,
                         TypeVariable.get_type_by_val(v4))
        self.assertEqual(TypeVariable.logic,
                         TypeVariable.get_type_by_val(v5))


if __name__ == "__main__":
    unittest.main()
