import unittest
from program import Program
from variables_types import TypeVariable


class TestWorker(unittest.TestCase):
    def setUp(self):
        program = Program("../test.fpp")
        self.worker = program.worker
        current_class, current_method, i = program.find_main_method()
        self.worker.set_up(current_class, current_method,
                           program.classes, program)
        self.worker.program.worker = self.worker

    def test_find_token(self):
        s1 = "I wrote \"Hello!\""
        s2 = "A is now \"I would be a lion\""
        s3 = "A = 5"
        self.assertEqual("I wrote", self.worker.find_token(s1))
        self.assertIsNone(self.worker.find_token(s2))
        self.assertIsNone(self.worker.find_token(s3))

    def test_find_method(self):
        s1 = "random"
        s2 = "summator using A and B"
        s3 = "\"get flag\""
        self.assertEqual("random", self.worker.find_method(s1))
        self.assertEqual("summator", self.worker.find_method(s2))
        self.assertIsNone(self.worker.find_token(s3))

    def test_is_change_var(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (20.0, TypeVariable.number, False),
                "C": ([1.0, 2.0, 3.0], TypeVariable.arrayNumbers,
                      False, TypeVariable.number),
                "S": ("qwerty", TypeVariable.phrase, False)}
        self.worker.vars[self.worker.current_method] = vars
        s1 = "C 1"
        s2 = "B"
        s3 = "\"A\""
        self.assertEqual("C", self.worker.is_change_var(s1))
        self.assertEqual("B", self.worker.is_change_var(s2))
        self.assertIsNone(self.worker.is_change_var(s3))

    def test_execute_sentence(self):
        s1 = "int a"
        self.assertRaises(SyntaxError, self.worker.execute_sentence, s1)
        s2 = "Did you know that A is the number 10"
        self.assertIsNone(self.worker.execute_sentence(s2))
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False)},
                             self.worker.vars[self.worker.current_method])
        s3 = "A got one more"
        self.assertIsNone(self.worker.execute_sentence(s3))
        self.assertDictEqual({"A": (11.0, TypeVariable.number, False)},
                             self.worker.vars[self.worker.current_method])
        s4 = "A got one less"
        self.assertIsNone(self.worker.execute_sentence(s4))
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False)},
                             self.worker.vars[self.worker.current_method])
        s5 = "A is now 0"
        self.assertIsNone(self.worker.execute_sentence(s5))
        self.assertDictEqual({"A": (0.0, TypeVariable.number, False)},
                             self.worker.vars[self.worker.current_method])
        s6 = "In regards to A"
        self.assertIsNone(self.worker.execute_sentence(s6))
        s7 = "A is now 10"
        s8 = "I wrote \'Q\'"
        self.assertRaises(SyntaxError, self.worker.execute_sentence, s7)
        self.assertRaises(SyntaxError, self.worker.execute_sentence, s8)
        self.worker.is_switch = False
        s9 = "As long as correct"
        self.assertTupleEqual(("while", True), self.worker
                              .execute_sentence(s9))
        self.worker.buffer["loops"][self.worker.current_method].clear()

    """
    def test_input(self):
        token1 = "I read"
        token2 = "I heard"
        vars = {}
        s1 = "I read A"  # input: "no"
        s2 = "I heard B"  # input: "10.5"
        s3 = "I read C"  # input: 1Ter5
        self.worker.input(token1, s1, vars)
        self.worker.input(token2, s2, vars)
        self.worker.input(token1, s3, vars)
        self.assertDictEqual({"A": (False,
                                    TypeVariable.logic,
                                    False),
                              "B": (10.5,
                                    TypeVariable.number,
                                    False),
                              "C": ("1Ter5",
                                    TypeVariable.phrase,
                                    False)},
                             vars)
        s4 = "I heard false argument"
        s5 = "I read Dear student"
        self.assertRaises(SyntaxError, self.worker.input, token2, s4, vars)
        self.assertRaises(SyntaxError, self.worker.input, token1, s5, vars)
    """

    def test_add_var(self):
        t = "Did you know that"
        vars = self.worker.vars[self.worker.current_method]
        s1 = "A = 5"
        s2 = "Did you know that A is 6?"
        s3 = "Did you know that what I sang has the name \"Song\""
        self.assertRaises(SyntaxError, self.worker.add_var, t, s1, vars)
        self.assertRaises(TypeError, self.worker.add_var, t, s2, vars)
        self.assertRaises(NameError, self.worker.add_var, t, s3, vars)
        s4 = "Did you know that A has many name"
        self.assertRaises(TypeError, self.worker.add_var, t, s4, vars)
        s5 = "Did you know that A has many names"
        s6 = "Did you know that B is the numbers 1 and 2 and 3"
        s16 = "Did you know that C is the arguments no and yes"
        s17 = "Did you know that D is the letters \'a\' and \'b\'"
        self.worker.add_var(t, s5, vars)
        self.worker.add_var(t, s6, vars)
        self.worker.add_var(t, s16, vars)
        self.worker.add_var(t, s17, vars)
        self.assertDictEqual({"A": ([], TypeVariable.arrayPhrases,
                                    False, TypeVariable.phrase),
                              "B": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers, False,
                                    TypeVariable.number),
                              "C": ([False, True], TypeVariable.arrayLogic,
                                    False, TypeVariable.logic),
                              "D": (["a", "b"], TypeVariable.arrayChars,
                                    False, TypeVariable.char)}, vars)
        s7 = "Did you know that A is the numbers \"hello\""
        s8 = "Did you know that A always has many names"
        self.assertRaises(ValueError, self.worker.add_var, t, s7, vars)
        self.assertRaises(ValueError, self.worker.add_var, t, s8, vars)
        s9 = "Did you know that A is the number \"Hello\""
        s10 = "Did you know that A is the type \"Hello\""
        self.assertRaises(ValueError, self.worker.add_var, t, s9, vars)
        self.assertRaises(TypeError, self.worker.add_var, t, s10, vars)
        vars.clear()
        s11 = "Did you know that A is the phrase \"Hello\""
        s12 = "Did you know that Flag is always the argument correct"
        self.worker.add_var(t, s11, vars)
        self.worker.add_var(t, s12, vars)
        self.assertDictEqual({"A": ("Hello", TypeVariable.phrase, False),
                              "Flag": (True, TypeVariable.logic, True)},
                             vars)
        s13 = "Did you know that A is always the number"
        s14 = "Did you know that Music is the song"
        self.assertRaises(ValueError, self.worker.add_var, t, s13, vars)
        self.assertRaises(TypeError, self.worker.add_var, t, s14, vars)
        vars.clear()
        s15 = "Did you know that A is the number"
        self.worker.add_var(t, s15, vars)
        self.assertDictEqual({"A": (None, TypeVariable.number, False)}, vars)

    def test_change_var(self):
        vars = {"A": (False, TypeVariable.logic, False),
                "E": ([1.0], TypeVariable.arrayNumbers,
                      False, TypeVariable.number),
                "D": (10.0, TypeVariable.number, True)}
        s1 = "A = 5"
        s2 = "B is now 5"
        s3 = "D 1 is now 5"
        s4 = "E index is now 6"
        s5 = "E 0 is now 6"
        s6 = "E 1 is now value"
        s7 = "E 1 is now \"Hello\""
        s8 = "D is now 5"
        s9 = "A is now flag"
        s10 = "A is now 5"
        s11 = "A is now correct"
        s12 = "E 1 is now D"
        self.assertRaises(SyntaxError, self.worker.change_var, s1, "A", vars)
        self.assertRaises(NameError, self.worker.change_var, s2, "B", vars)
        self.assertRaises(TypeError, self.worker.change_var, s3, "D", vars)
        self.assertRaises(IndexError, self.worker.change_var, s4, "E", vars)
        self.assertRaises(IndexError, self.worker.change_var, s5, "E", vars)
        self.assertRaises(ValueError, self.worker.change_var, s6, "E", vars)
        self.assertRaises(ValueError, self.worker.change_var, s7, "E", vars)
        self.assertRaises(ValueError, self.worker.change_var, s8, "D", vars)
        self.assertRaises(ValueError, self.worker.change_var, s9, "A", vars)
        self.assertRaises(ValueError, self.worker.change_var, s10, "A", vars)
        self.worker.change_var(s11, "A", vars)
        self.worker.change_var(s12, "E", vars)
        self.assertDictEqual({"A": (True, TypeVariable.logic, False),
                              "E": ([10.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "D": (10.0, TypeVariable.number, True)}, vars)

    def test_increment_or_decrement(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (10.0, TypeVariable.number, True),
                "C": (False, TypeVariable.logic, False)}
        s1 = "B got one more"
        s2 = "C got one less"
        s3 = "Var got one more"
        self.assertRaises(ValueError, self.worker.increment_or_decrement,
                          s1, vars, True)
        self.assertRaises(ArithmeticError, self.worker.increment_or_decrement,
                          s2, vars, False)
        self.assertRaises(NameError, self.worker.increment_or_decrement,
                          s3, vars, True)
        s4 = "A got one more"
        self.worker.increment_or_decrement(s4, vars, True)
        self.assertDictEqual({"A": (11.0, TypeVariable.number, False),
                              "B": (10.0, TypeVariable.number, True),
                              "C": (False, TypeVariable.logic, False)}, vars)
        s5 = "A got one less"
        self.worker.increment_or_decrement(s5, vars, False)
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (10.0, TypeVariable.number, True),
                              "C": (False, TypeVariable.logic, False)}, vars)

    def test_return_val(self):
        self.worker.vars = {"get default name": {},
                            "random": {}}
        vars = {}
        t = "Then you get"
        # greetings
        s1 = "Then you get 42"
        self.worker.current_method = "greetings"
        self.assertRaises(SyntaxError, self.worker.return_val, t, s1, vars)
        # get default name
        s2 = "Then you get 111"
        self.worker.current_method = "get default name"
        self.assertRaises(TypeError, self.worker.return_val, t, s2, vars)
        # random
        s3 = "Then you get 125"
        self.worker.current_method = "random"
        self.assertTupleEqual(("return", 125), self
                              .worker.return_val(t, s3, vars))

    def test_if_condition(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (True, TypeVariable.logic, True),
                "C": (False, TypeVariable.logic, True)}
        t = "If"
        t2 = "When"
        s1 = "If B"
        s2 = "If A then"
        self.assertRaises(SyntaxError, self.worker.if_condition, t, s1, vars)
        self.assertRaises(SyntaxError, self.worker.if_condition, t, s2, vars)
        s3 = "If B then"
        s4 = "When A is 10 then"
        self.assertTupleEqual(("if", True), self.worker
                              .if_condition(t, s3, vars))
        self.assertTupleEqual(("if", True), self.worker
                              .if_condition(t2, s4, vars))
        s5 = "If C then"
        s6 = "When A is more than 10 then"
        self.assertTupleEqual(("if", False), self.worker
                              .if_condition(t, s5, vars))
        self.assertTupleEqual(("if", False), self.worker
                              .if_condition(t2, s6, vars))

    def test_else_condition(self):
        t = "Or else"
        vars = {}
        s1 = "Or else"
        self.assertRaises(SyntaxError, self.worker.else_condition,
                          t, s1, vars)
        s = "If true then"
        self.worker.if_condition("If", s, vars)
        self.assertTupleEqual(("else", False), self.worker
                              .else_condition(t, s1, vars))

    def test_switch(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": ("Aaaa", TypeVariable.phrase, False)}
        t = "In regards to"
        s1 = "In regards to C"
        s2 = "In regards to B"
        s3 = "In regards to A"
        self.assertRaises(NameError, self.worker.switch, t, s1, vars)
        self.assertRaises(TypeError, self.worker.switch, t, s2, vars)
        self.worker.switch(t, s3, vars)
        self.assertTupleEqual(("switch", "A", False), self.worker
                              .buffer["loops"][self.worker.current_method][-1])

    def test_case_switch(self):
        vars = {"A": (10.0, TypeVariable.number, False)}
        t = "On the"
        s1 = "On the 1st hoof"
        self.assertRaises(SyntaxError, self.worker.case_switch, t, s1, vars)
        s = "In regards to A"
        self.worker.switch("In regards to", s, vars)
        s2 = "On the 2nd"
        s3 = "On the third hoof"
        self.assertRaises(SyntaxError, self.worker.case_switch, t, s2, vars)
        self.assertRaises(ValueError, self.worker.case_switch, t, s3, vars)
        s4 = "On the 4th hoof"
        s5 = "On the 10th hoof"
        self.assertTupleEqual(("switch", False),
                              self.worker.case_switch(t, s4, vars))
        self.assertTupleEqual(("switch", True),
                              self.worker.case_switch(t, s5, vars))

    def test_default_case(self):
        vars = {"A": (10.0, TypeVariable.number, False)}
        t = "If all else fails"
        s1 = "If all else fails"
        self.assertRaises(SyntaxError, self.worker.default_case, t, s1, vars)
        s = "In regards to A"
        self.worker.switch("In regards to", s, vars)
        self.worker.default_case(t, s1, vars)
        cm = self.worker.current_method
        self.assertFalse(self.worker.is_switch)
        self.assertTupleEqual(("switch", "A", True), self.worker
                              .buffer["loops"][cm][-1])

    def test_loop_while(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (True, TypeVariable.logic, False)}
        t = "As long as"
        s1 = "As long as A = 10"
        self.assertRaises(SyntaxError, self.worker.loop_while, t, s1, vars)
        s2 = "As long as not B"
        self.assertTupleEqual(("while", False), self.worker
                              .loop_while(t, s2, vars))
        s3 = "As long as A is 10"
        cm = self.worker.current_method
        self.assertTupleEqual(("while", True), self.worker
                              .loop_while(t, s3, vars))
        self.assertEqual("while", self.worker.buffer["loops"][cm][-1])

    def test_loop_do_while(self):
        vars = {}
        t = "Here's what I did"
        s1 = t + " with it"
        self.assertRaises(SyntaxError, self.worker
                          .loop_do_while, t, s1, vars)
        self.assertTupleEqual(("do while", None), self.worker
                              .loop_do_while(t, t, vars))

    def test_end_loop_do_while(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (True, TypeVariable.logic, False)}
        t = "I did this while"
        s1 = "I did this while A = 10"
        self.assertRaises(SyntaxError, self.worker.end_loop_do_while,
                          t, s1, vars)
        s2 = "I did this while not B"
        s3 = "I did this while A is 10"
        self.assertTupleEqual(("end do while", False), self.worker
                              .end_loop_do_while(t, s2, vars))
        self.assertTupleEqual(("end do while", True), self.worker
                              .end_loop_do_while(t, s3, vars))

    def test_loop_for(self):
        vars = {"A": (10.0, TypeVariable.number, False),
                "B": (20.0, TypeVariable.number, False),
                "C": ([1.0, 2.0, 3.0], TypeVariable.arrayNumbers,
                      False, TypeVariable.number),
                "S": ("qwerty", TypeVariable.phrase, False)}
        t = "For every"
        s = "For every number i = 0; i < 10; i++"
        self.assertRaises(SyntaxError, self.worker.loop_for, t, s, vars)
        s1 = "For every type x from 1 to 10"
        self.assertRaises(TypeError, self.worker.loop_for, t, s1, vars)
        # from ... to ...
        # number
        s2 = "For every number A from 1 to 10"
        s3 = "For every number What I Wrote from 1 to 10"
        self.assertRaises(NameError, self.worker.loop_for, t, s2, vars)
        self.assertRaises(NameError, self.worker.loop_for, t, s3, vars)
        s4 = "For every number x from A to \"Hello\""
        s5 = "For every number x from \'a\' to A"
        s6 = "For every number x from 10 to"
        self.assertRaises(ValueError, self.worker.loop_for, t, s4, vars)
        self.assertRaises(ValueError, self.worker.loop_for, t, s5, vars)
        self.assertRaises(SyntaxError, self.worker.loop_for, t, s6, vars)
        cm = self.worker.current_method
        s11 = "For every number x from 1 to 10"
        self.worker.loop_for(t, s11, vars)
        self.assertTupleEqual(("for", "x", 10.0, False), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": (1.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        s12 = "For every number x from A to B"
        self.worker.loop_for(t, s12, vars)
        self.assertTupleEqual(("for", "x", 20.0, False), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": (10.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        s13 = "For every number x from B to 0"
        self.worker.loop_for(t, s13, vars)
        self.assertTupleEqual(("for", "x", 0.0, True), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": (20.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        # character
        s7 = "For every character x from \"Asd\" to 10"
        s8 = "For every character x from 10 to \"asd\""
        s9 = "For every character x from 50 to"
        self.assertRaises(ValueError, self.worker.loop_for, t, s7, vars)
        self.assertRaises(ValueError, self.worker.loop_for, t, s8, vars)
        self.assertRaises(SyntaxError, self.worker.loop_for, t, s9, vars)
        s10 = "For every argument Arg from incorrect to correct"
        self.assertRaises(TypeError, self.worker.loop_for, t, s10, vars)
        s14 = "For every character x from \'a\' to \'z\'"
        self.worker.loop_for(t, s14, vars)
        self.assertTupleEqual(("for", "x", 122, False), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": ("a", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        s15 = "For every character x from 97 to 122"
        self.worker.loop_for(t, s15, vars)
        self.assertTupleEqual(("for", "x", 122, False), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": ("a", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        s16 = "For every character x from \'Z\' to \'A\'"
        self.worker.loop_for(t, s16, vars)
        self.assertTupleEqual(("for", "x", 65, True), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "x": ("Z", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("x")
        # in ...
        s1 = "For every number A in C"
        s2 = "For every number what I given in C"
        s3 = "For every number e in A"
        s4 = "For every number e in var"
        s5 = "For every character e in \"\""
        s6 = "For every character e in C"
        s7 = "For every number e in S"
        self.assertRaises(NameError, self.worker.loop_for, t, s1, vars)
        self.assertRaises(NameError, self.worker.loop_for, t, s2, vars)
        self.assertRaises(ValueError, self.worker.loop_for, t, s3, vars)
        self.assertRaises(ValueError, self.worker.loop_for, t, s4, vars)
        self.assertTupleEqual(("for", False), self.worker
                              .loop_for(t, s5, vars))
        self.assertRaises(TypeError, self.worker.loop_for, t, s6, vars)
        self.assertRaises(TypeError, self.worker.loop_for, t, s7, vars)
        s8 = "For every number e in C"
        self.worker.loop_for(t, s8, vars)
        self.assertTupleEqual(("for", "e", [1.0, 2.0, 3.0], 0), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "e": (1.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("e")
        s9 = "For every character e in S"
        self.worker.loop_for(t, s9, vars)
        self.assertTupleEqual(("for", "e", "qwerty", 0), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "e": ("q", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("e")
        s10 = "For every character e in \"Hello\""
        self.worker.loop_for(t, s10, vars)
        self.assertTupleEqual(("for", "e", "Hello", 0), self.worker
                              .buffer["loops"][cm][-1])
        self.assertDictEqual({"A": (10.0, TypeVariable.number, False),
                              "B": (20.0, TypeVariable.number, False),
                              "C": ([1.0, 2.0, 3.0],
                                    TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "S": ("qwerty", TypeVariable.phrase, False),
                              "e": ("H", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].pop()
        vars.pop("e")

    def test_end_loop(self):
        vars = {"L": ([1.0, 2.0], TypeVariable.arrayNumbers, False,
                      TypeVariable.number)}
        cm = self.worker.current_method
        s = "That's what I did"
        self.assertRaises(SyntaxError, self.worker.end_loop, s, s, vars)
        s_w = "As long as correct"
        self.worker.loop_while("As long as", s_w, vars)
        self.worker.buffer["loops"][cm].clear()
        self.assertTupleEqual(("end loop", True), self.worker
                              .end_loop(s, s, vars))
        self.worker.loop_while("As long as", s_w, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        s_f_n = "For every number x from 1 to 2"
        s_f_n_r = "For every number x from 2 to 1"
        s_f_c = "For every character x from \'a\' to \'b\'"
        s_f_c_r = "For every character x from \'b\' to \'a\'"
        self.worker.loop_for("For every", s_f_n, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        self.assertDictEqual({"L": ([1.0, 2.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "x": (2.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].clear()
        vars.pop("x")
        self.worker.loop_for("For every", s_f_n_r, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        self.assertDictEqual({"L": ([1.0, 2.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "x": (1.0, TypeVariable.number, False)}, vars)
        self.worker.buffer["loops"][cm].clear()
        vars.pop("x")
        self.worker.loop_for("For every", s_f_c, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        self.assertDictEqual({"L": ([1.0, 2.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "x": ("b", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].clear()
        vars.pop("x")
        self.worker.loop_for("For every", s_f_c_r, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        self.assertDictEqual({"L": ([1.0, 2.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "x": ("a", TypeVariable.char, False)}, vars)
        self.worker.buffer["loops"][cm].clear()
        vars.pop("x")
        s_f_l = "For every number x in L"
        self.worker.loop_for("For every", s_f_l, vars)
        self.assertTupleEqual(("end loop", False), self.worker
                              .end_loop(s, s, vars))
        self.assertDictEqual({"L": ([1.0, 2.0], TypeVariable.arrayNumbers,
                                    False, TypeVariable.number),
                              "x": (2.0, TypeVariable.number, False)}, vars)
        self.assertTupleEqual(("for", "x", vars["L"][0], 1), self.worker
                              .buffer["loops"][cm][-1])


if __name__ == "__main__":
    unittest.main()
