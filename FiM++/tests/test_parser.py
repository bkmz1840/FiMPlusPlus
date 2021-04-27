import unittest
from program import Program
from parser import Parser
from variables_types import TypeVariable


class TestParser(unittest.TestCase):
    def setUp(self):
        program = Program("../test.fpp")
        self.worker = program.worker
        current_class, current_method, i = program.find_main_method()
        self.worker.set_up(current_class, current_method,
                           program.classes, program)
        self.vars = {
            "A": (10.0, TypeVariable.number, False),
            "B": ("Hell", TypeVariable.phrase, True),
            "C": (False, TypeVariable.logic, False),
            "D": (5.0, TypeVariable.number, True),
            "E": ([1.0, 2.0, 3.0, 4.0], TypeVariable.arrayNumbers,
                  False, TypeVariable.number),
            "i": (1.0, TypeVariable.number, False)
        }
        self.worker.vars = {current_method: self.vars}
        self.worker.program.worker = self.worker

    def test_erase_article_from_start_str(self):
        s1 = "the number"
        s2 = "number"
        s3 = "a number"
        self.assertEqual("number", Parser.erase_article_from_start_str(s1))
        self.assertEqual("number", Parser.erase_article_from_start_str(s2))
        self.assertEqual("number", Parser.erase_article_from_start_str(s3))

    def test_find_all_class_methods(self):
        s1 = ["Dear Princess Celestia", "Letter one",
              "Today I learned how to say"]
        rd1 = {"Letter one": {"how to say": (2, "main")}}
        s2 = ["Dear Princess Celestia", "Letter one",
              "Today I learned how to say", "I learned how multiply"]
        rd2 = {"Letter one": {"how to say": (2, "main"),
                              "how multiply": (3, None, None)}}
        s3 = ["Dear Princess Celestia", "Letter one",
              "I learned about greetings with a name"]
        rd3 = {"Letter one": {"greetings": (2, TypeVariable.phrase, None)}}
        s4 = ["Dear Princess Celestia", "Letter one",
              "Today I learned how to say",
              "I learned about editor with phrase using a phrase Text"]
        rd4 = {"Letter one": {"how to say": (2, "main"),
                              "editor": (3, TypeVariable.phrase,
                                         {"Text":
                                          TypeVariable.phrase})}}
        s5 = ["Dear Princess Celestia", "Letter one",
              "I learned about editor using a name Line and a phrase Text"]
        rd5 = {"Letter one": {"editor": (2, None,
                                         {"Line":
                                          TypeVariable.phrase,
                                          "Text":
                                          TypeVariable.phrase})}}
        s6 = ["Dear Princess Celestia", "Letter one",
              "I learned about editor with a phrase " +
              "using the character Line and a phrase Text " +
              "and a phrase Another Text"]
        rd6 = {"Letter one": {"editor": (2, TypeVariable.phrase,
                                         {"Line":
                                          TypeVariable.char,
                                          "Text":
                                          TypeVariable.phrase,
                                          "Another Text":
                                          TypeVariable.phrase})}}
        s7 = ["Today I learned how to say",
              "Dear Princess Celestia", "Letter one"]
        s8 = ["Dear Princess Celestia", "Letter one",
              "I learned about editor using Line"]
        s9 = ["Dear Princess Celestia", "Letter one",
              "I learned about editor using a name what I said"]
        s10 = ["Dear Princess Celestia", "Letter one",
               "I learned about editor with digit"]
        s11 = ["Dear Princess Celestia", "Letter one",
               "I learned with digit"]
        s12 = ["Dear Princess Celestia", "Letter one",
               "I learned about editor using digit Text"]
        self.assertDictEqual(rd1, Parser.find_all_class_methods(s1))
        self.assertDictEqual(rd2, Parser.find_all_class_methods(s2))
        self.assertDictEqual(rd3, Parser.find_all_class_methods(s3))
        self.assertDictEqual(rd4, Parser.find_all_class_methods(s4))
        self.assertDictEqual(rd5, Parser.find_all_class_methods(s5))
        self.assertDictEqual(rd6, Parser.find_all_class_methods(s6))
        self.assertRaises(SyntaxError, Parser.find_all_class_methods, s7)
        self.assertRaises(SyntaxError, Parser.find_all_class_methods, s8)
        self.assertRaises(SyntaxError, Parser.find_all_class_methods, s9)
        self.assertRaises(TypeError, Parser.find_all_class_methods, s10)
        self.assertRaises(SyntaxError, Parser.find_all_class_methods, s11)
        self.assertRaises(TypeError, Parser.find_all_class_methods, s12)

    def test_parse_decl_of_method(self):
        d1 = "how greetings"
        d2 = "about editor"
        d3 = "about editor with a phrase"
        d4 = "about editor using a phrase Text"
        d5 = "about editor with a phrase using a letter Mode " \
             "and a name Editor and a phrase Text"
        d6 = "with a name"
        d7 = "about editor with digit"
        d8 = "about editor using digit Text"
        d9 = "about editor using a phrase what I wrote"
        d10 = "about editor using Line"
        self.assertTupleEqual(("how greetings", None, None),
                              Parser.parse_decl_of_method(d1))
        self.assertTupleEqual(("editor", None, None),
                              Parser.parse_decl_of_method(d2))
        self.assertTupleEqual(("editor", TypeVariable.phrase, None),
                              Parser.parse_decl_of_method(d3))
        self.assertTupleEqual(("editor", None, {"Text": TypeVariable.phrase}),
                              Parser.parse_decl_of_method(d4))
        self.assertTupleEqual(("editor", TypeVariable.phrase,
                               {"Mode": TypeVariable.char,
                                "Editor": TypeVariable.phrase,
                                "Text": TypeVariable.phrase}),
                              Parser.parse_decl_of_method(d5))
        self.assertTupleEqual(("ErrorName", None, None),
                              Parser.parse_decl_of_method(d6))
        self.assertTupleEqual((None, "ErrorTypeReturn", None),
                              Parser.parse_decl_of_method(d7))
        self.assertTupleEqual((None, None, "ErrorTypeArg"),
                              Parser.parse_decl_of_method(d8))
        self.assertTupleEqual((None, None, "ErrorArgName"),
                              Parser.parse_decl_of_method(d9))
        self.assertTupleEqual((None, None, "ErrorDeclArg"),
                              Parser.parse_decl_of_method(d10))

    def test_isnumber(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = None
        self.assertEqual(False, Parser.isnumber(v1))
        self.assertEqual(False, Parser.isnumber(v2))
        self.assertEqual(True, Parser.isnumber(v3))
        self.assertEqual(True, Parser.isnumber(v4))
        self.assertEqual(False, Parser.isnumber(v5))
        self.assertEqual(False, Parser.isnumber(v6))

    def test_isint(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = "5"
        v7 = None
        self.assertFalse(Parser.isint(v1))
        self.assertFalse(Parser.isint(v2))
        self.assertTrue(Parser.isint(v3))
        self.assertFalse(Parser.isint(v4))
        self.assertFalse(Parser.isint(v5))
        self.assertTrue(Parser.isint(v6))
        self.assertFalse(Parser.isint(v7))

    def test_parse_input(self):
        in1 = "10.5"
        in2 = ""
        in3 = "no"
        in4 = "a"
        in5 = "qwert"
        self.assertTupleEqual((10.5, TypeVariable.number),
                              Parser.parse_input(in1))
        self.assertTupleEqual(("", TypeVariable.phrase),
                              Parser.parse_input(in2))
        self.assertTupleEqual((False, TypeVariable.logic),
                              Parser.parse_input(in3))
        self.assertTupleEqual(('a', TypeVariable.char),
                              Parser.parse_input(in4))
        self.assertTupleEqual(("qwert", TypeVariable.phrase),
                              Parser.parse_input(in5))

    def test_check_val_and_type(self):
        v1, t1 = 10, TypeVariable.number
        v2, t2 = "14", TypeVariable.number
        self.assertTrue(Parser.check_val_and_type(v1, t1))
        self.assertFalse(Parser.check_val_and_type(v2, t2))
        v3, t3 = False, TypeVariable.logic
        v4, t4 = "True", TypeVariable.logic
        self.assertTrue(Parser.check_val_and_type(v3, t3))
        self.assertFalse(Parser.check_val_and_type(v4, t4))
        v5, t5 = 'A', TypeVariable.char
        v6, t6 = "Abra", TypeVariable.char
        self.assertTrue(Parser.check_val_and_type(v5, t5))
        self.assertFalse(Parser.check_val_and_type(v6, t6))
        v7, t7 = "Abra", TypeVariable.phrase
        v8, t8 = 10, TypeVariable.phrase
        v9, t9 = False, TypeVariable.phrase
        v10, t10 = 'A', TypeVariable.phrase
        self.assertTrue(Parser.check_val_and_type(v7, t7))
        self.assertFalse(Parser.check_val_and_type(v8, t8))
        self.assertFalse(Parser.check_val_and_type(v9, t9))
        self.assertTrue(Parser.check_val_and_type(v10, t10))

    def test_check_var_name(self):
        n1 = "false love"
        n2 = "True argument"
        n3 = "A"
        n4 = "second name of Dear girl"
        n5 = "number what I heard"
        n6 = "what I wrote"
        self.assertFalse(Parser.check_var_name(n1))
        self.assertFalse(Parser.check_var_name(n2))
        self.assertTrue(Parser.check_var_name(n3))
        self.assertFalse(Parser.check_var_name(n4))
        self.assertFalse(Parser.check_var_name(n5))
        self.assertFalse(Parser.check_var_name(n6))

    def test_get_val_by_str_and_type(self):
        vars = {"A": (10, TypeVariable.number, False),
                "B": (False, TypeVariable.logic, True),
                "C": ("Area", TypeVariable.phrase, False),
                "D": ("D", TypeVariable.char, False)}
        t1 = "number"
        s1 = "10"
        s2 = "10.90"
        s3 = "1are5"
        s4 = "A"
        self.assertTupleEqual((10, TypeVariable.number), Parser
                              .get_val_by_str_and_type(s1, t1, vars,
                                                       self.worker))
        self.assertTupleEqual((10.9, TypeVariable.number), Parser
                              .get_val_by_str_and_type(s2, t1, vars,
                                                       self.worker))
        self.assertTupleEqual(("ErrorValue", None), Parser
                              .get_val_by_str_and_type(s3, t1, vars,
                                                       self.worker))
        self.assertTupleEqual((10, TypeVariable.number), Parser
                              .get_val_by_str_and_type(s4, t1, vars,
                                                       self.worker))
        t2 = "letter"
        s5 = "q"
        s6 = "\'A\'"
        s7 = "D"
        self.assertTupleEqual(("ErrorValue", None), Parser
                              .get_val_by_str_and_type(s5, t2, vars,
                                                       self.worker))
        self.assertTupleEqual(("A", TypeVariable.char), Parser
                              .get_val_by_str_and_type(s6, t2, vars,
                                                       self.worker))
        self.assertTupleEqual(("D", TypeVariable.char), Parser
                              .get_val_by_str_and_type(s7, t2, vars,
                                                       self.worker))
        t3 = "phrase"
        s9 = '\"Hello\"'
        s10 = "incorrect"
        s11 = "C"
        self.assertTupleEqual(("Hello", TypeVariable.phrase), Parser
                              .get_val_by_str_and_type(s9, t3, vars,
                                                       self.worker))
        self.assertTupleEqual(("ErrorValue", None), Parser
                              .get_val_by_str_and_type(s10, t3, vars,
                                                       self.worker))
        self.assertTupleEqual(("Area", TypeVariable.phrase), Parser
                              .get_val_by_str_and_type(s11, t3, vars,
                                                       self.worker))
        t4 = "logic"
        s13 = "no"
        s14 = "B"
        s15 = '\"True\"'
        self.assertTupleEqual((False, TypeVariable.logic), Parser
                              .get_val_by_str_and_type(s13, t4, vars,
                                                       self.worker))
        self.assertTupleEqual((False, TypeVariable.logic), Parser
                              .get_val_by_str_and_type(s14, t4, vars,
                                                       self.worker))
        self.assertTupleEqual(("ErrorValue", None), Parser
                              .get_val_by_str_and_type(s15, t4, vars,
                                                       self.worker))
        t5 = "anyType"
        s16 = "\"Error\""
        self.assertTupleEqual(("ErrorType", None), Parser
                              .get_val_by_str_and_type(s16, t5, vars,
                                                       self.worker))

    def test_get_val_by_str(self):
        v1 = "A"  # 10.0
        v2 = "E"  # [1.0, 2.0, 3.0, 4.0]
        v3 = "E 1"  # 1.0
        v4 = "E 5"  # None
        v5 = "E i"  # 1.0
        v6 = "10"  # 10.0
        v7 = "17.8"  # 17.8
        v8 = ""  # None
        v9 = "\"Hello!\""  # Hello!
        v10 = "\'a\'"  # a
        v11 = "\"Hello\" plus \", \" added to \"world!\""  # Hello, world!
        v12 = "true"  # True
        v13 = "correct"  # True
        v14 = "false"  # False
        v15 = "no"  # False
        v16 = "10 times 10"  # 100.0
        v17 = "add A and D"  # 15.0
        v18 = "E 1 plus E 2"  # 3.0
        v19 = "D is 10.0"  # False
        v20 = "A is more than D"  # True
        v21 = "random"  # 42.0
        v22 = "summator using A and D"  # 15.0
        v23 = "\'abs\'"  # None
        self.assertEqual(10.0, Parser
                         .get_val_by_str(v1, self.vars, self.worker))
        self.assertEqual([1.0, 2.0, 3.0, 4.0], Parser
                         .get_val_by_str(v2, self.vars, self.worker))
        self.assertEqual(1.0, Parser
                         .get_val_by_str(v3, self.vars, self.worker))
        self.assertIsNone(Parser.get_val_by_str(v4, self.vars, self.worker))
        self.assertEqual(1.0, Parser
                         .get_val_by_str(v5, self.vars, self.worker))
        self.assertEqual(10.0, Parser
                         .get_val_by_str(v6, self.vars, self.worker))
        self.assertEqual(17.8, Parser
                         .get_val_by_str(v7, self.vars, self.worker))
        self.assertIsNone(Parser.get_val_by_str(v8, self.vars, self.worker))
        self.assertEqual("Hello!", Parser
                         .get_val_by_str(v9, self.vars, self.worker))
        self.assertEqual("a", Parser
                         .get_val_by_str(v10, self.vars, self.worker))
        self.assertEqual("Hello, world!", Parser
                         .get_val_by_str(v11, self.vars, self.worker))
        self.assertTrue(Parser.get_val_by_str(v12, self.vars, self.worker))
        self.assertTrue(Parser.get_val_by_str(v13, self.vars, self.worker))
        self.assertFalse(Parser.get_val_by_str(v14, self.vars, self.worker))
        self.assertFalse(Parser.get_val_by_str(v15, self.vars, self.worker))
        self.assertEqual(100.0, Parser
                         .get_val_by_str(v16, self.vars, self.worker))
        self.assertEqual(15.0, Parser
                         .get_val_by_str(v17, self.vars, self.worker))
        self.assertEqual(3.0, Parser
                         .get_val_by_str(v18, self.vars, self.worker))
        self.assertFalse(Parser.get_val_by_str(v19, self.vars, self.worker))
        self.assertTrue(Parser.get_val_by_str(v20, self.vars, self.worker))
        self.assertEqual(42.0, Parser
                         .get_val_by_str(v21, self.vars, self.worker))
        self.assertEqual(15.0, Parser
                         .get_val_by_str(v22, self.vars, self.worker))
        self.assertIsNone(Parser.get_val_by_str(v23, self.vars, self.worker))

    def test_parse_array_val(self):
        s1 = ""
        s2 = "\"ab\" and \"ra\" and \"kad\" and \"abra\""
        s3 = "1 and 2 and 3"
        s4 = "no and incorrect and correct and yes"
        s5 = "\'q\' and \'w\' and \'e\' and \'r\' and \'t\'"
        s6 = "1 and \"asd\""
        s7 = "A and D and 7"
        self.assertListEqual([], Parser
                             .parse_array_val(s1, TypeVariable.phrase,
                                              self.vars, self.worker))
        self.assertListEqual(["ab", "ra", "kad", "abra"], Parser
                             .parse_array_val(s2, TypeVariable.phrase,
                                              self.vars, self.worker))
        self.assertListEqual([1.0, 2.0, 3.0], Parser
                             .parse_array_val(s3, TypeVariable.number,
                                              self.vars, self.worker))
        self.assertListEqual([False, False, True, True], Parser
                             .parse_array_val(s4, TypeVariable.logic,
                                              self.vars, self.worker))
        self.assertListEqual(["q", "w", "e", "r", "t"], Parser
                             .parse_array_val(s5, TypeVariable.char,
                                              self.vars, self.worker))
        self.assertEqual("ValueError", Parser
                         .parse_array_val(s6, TypeVariable.number,
                                          self.vars, self.worker))
        self.assertListEqual([10.0, 5.0, 7.0], Parser
                             .parse_array_val(s7, TypeVariable.number,
                                              self.vars, self.worker))

    def test_get_sentences_by_split_text(self):
        st1 = [""]
        st2 = ["                 How do it work?"]
        st3 = ["                 How do it work?                 "]
        self.assertListEqual([], Parser.get_sentences_by_split_text(st1))
        self.assertListEqual(["How do it work?"], Parser
                             .get_sentences_by_split_text(st2))
        self.assertListEqual(["How do it work?"], Parser
                             .get_sentences_by_split_text(st3))

    def test_get_val_in_array(self):
        s1 = "E 1"
        s2 = "D 1"
        s3 = "E 5"
        s4 = "E 2"
        s5 = "E 0"
        s6 = "E i"
        s7 = "E get next index using i"
        s8 = "R 1"
        self.assertEqual(1.0, Parser
                         .get_val_in_array(s1, "E", self.vars, self.worker))
        self.assertIsNone(Parser.get_val_in_array(s2, "D",
                                                  self.vars, self.worker))
        self.assertEqual("ErrorIndex", Parser
                         .get_val_in_array(s3, "E", self.vars, self.worker))
        self.assertEqual(2.0, Parser
                         .get_val_in_array(s4, "E", self.vars, self.worker))
        self.assertEqual("ErrorIndex", Parser
                         .get_val_in_array(s5, "E", self.vars, self.worker))
        self.assertEqual(1.0, Parser
                         .get_val_in_array(s6, "E", self.vars, self.worker))
        self.assertEqual(2.0, Parser
                         .get_val_in_array(s7, "E", self.vars, self.worker))
        self.assertIsNone(Parser.get_val_in_array(s8, "R",
                                                  self.vars, self.worker))

    def test_split_lines_by_sentences(self):
        t1 = ["I wrote (or not) some tasks for next week."]
        t2 = ["Apple is now green! P.S.: Everybody know it."]
        t3 = ["I wrote (or not. or have forgotten about it.) "
              "some tasks for next week."]
        t4 = ["I wrote (or not.", "or have forgotten about it.) "
                                  "some tasks for next week."]
        t5 = ["I wrote (or not.", "or have forgotten",
              "about it.) some tasks for next week."]
        self.assertListEqual(["I wrote some tasks for next week"],
                             Parser.split_lines_by_sentences(t1))
        self.assertListEqual(["Apple is now green"],
                             Parser.split_lines_by_sentences(t2))
        self.assertListEqual(["I wrote some tasks for next week"],
                             Parser.split_lines_by_sentences(t3))
        self.assertListEqual(["I wrote some tasks for next week"],
                             Parser.split_lines_by_sentences(t4))
        self.assertListEqual(["I wrote some tasks for next week"],
                             Parser.split_lines_by_sentences(t5))


if __name__ == "__main__":
    unittest.main()
