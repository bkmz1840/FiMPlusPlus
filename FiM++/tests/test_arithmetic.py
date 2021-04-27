import unittest
from program import Program
from arithmetic import Arithmetic
from variables_types import TypeVariable


class TestArithmetic(unittest.TestCase):
    def setUp(self):
        program = Program("../test.fpp")
        self.worker = program.worker
        current_class, current_method, i = program.find_main_method()
        self.worker.set_up(current_class, current_method,
                           program.classes, program)
        self.vars = {"A": (10.5, TypeVariable.number, False),
                     "B": (8, TypeVariable.number, True),
                     "C": ("Ab", TypeVariable.phrase, False),
                     "D": ("bA", TypeVariable.phrase, False),
                     "E": ([1.0, 2.0, 3.0, 4.0], TypeVariable.arrayNumbers,
                           False, TypeVariable.number),
                     "F": (["ab", "ra", "ka", "dabra"],
                           TypeVariable.arrayPhrases, False,
                           TypeVariable.phrase),
                     "i": (2.0, TypeVariable.number, False),
                     "o": (0.0, TypeVariable.number, False)}
        self.worker.vars = {current_method: self.vars}
        self.worker.program.worker = self.worker
        self.ex1 = "add 2 and 3"  # 5
        self.ex2 = "A added to 3"  # 13.5
        self.ex3 = "A got one more"  # 11.5
        self.ex4 = "subtract B and 9"  # -1
        self.ex5 = "A minus 10"  # 1.5
        self.ex6 = "the difference between A and B"  # 3.5
        self.ex7 = "9 times 8"  # 72
        self.ex8 = "multiply A and B"  # 92
        self.ex9 = "A divided by 11.5"  # 1
        self.ex10 = "divide A and B"
        self.ex11 = "divide A by 10"  # 1.15
        self.ex12 = "add 2 and 3 plus 4 added to 5"  # 14
        self.ex13 = "C plus D added to 17"
        self.ex14 = "Add \"Ba\" and C"
        self.ex15 = "Add E 1 and E 2 plus E 3 added to E 4"
        self.ex16 = "random divided by E i"

    def test_find_arithmetic_operation(self):
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex1))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex2))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex3))
        self.assertEqual("Subtraction", Arithmetic
                         .find_arithmetic_operation(self.ex4))
        self.assertEqual("Subtraction", Arithmetic
                         .find_arithmetic_operation(self.ex5))
        self.assertEqual("Subtraction", Arithmetic
                         .find_arithmetic_operation(self.ex6))
        self.assertEqual("Multiplication", Arithmetic
                         .find_arithmetic_operation(self.ex7))
        self.assertEqual("Multiplication", Arithmetic
                         .find_arithmetic_operation(self.ex8))
        self.assertEqual("Division", Arithmetic
                         .find_arithmetic_operation(self.ex9))
        self.assertEqual("Division", Arithmetic
                         .find_arithmetic_operation(self.ex10))
        self.assertEqual("Division", Arithmetic
                         .find_arithmetic_operation(self.ex11))
        self.assertIsNone(Arithmetic.find_arithmetic_operation(""))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex12))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex13))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex14))
        self.assertEqual("Addition", Arithmetic
                         .find_arithmetic_operation(self.ex15))
        self.assertEqual("Division", Arithmetic
                         .find_arithmetic_operation(self.ex16))

    def test_solve_expression(self):
        self.assertEqual(5, Arithmetic
                         .solve_expression(self.ex1, self.vars, self.worker))
        self.assertEqual(13.5, Arithmetic
                         .solve_expression(self.ex2, self.vars, self.worker))
        self.assertEqual(11.5, Arithmetic
                         .solve_expression(self.ex3, self.vars, self.worker))
        self.assertEqual(-1, Arithmetic
                         .solve_expression(self.ex4, self.vars, self.worker))
        self.assertEqual(1.5, Arithmetic
                         .solve_expression(self.ex5, self.vars, self.worker))
        self.assertEqual(3.5, Arithmetic
                         .solve_expression(self.ex6, self.vars, self.worker))
        self.assertEqual(72, Arithmetic
                         .solve_expression(self.ex7, self.vars, self.worker))
        self.assertEqual(92, Arithmetic
                         .solve_expression(self.ex8, self.vars, self.worker))
        self.assertEqual(1, Arithmetic
                         .solve_expression(self.ex9, self.vars, self.worker))
        self.assertEqual(11.5 / 8, Arithmetic
                         .solve_expression(self.ex10, self.vars, self.worker))
        self.assertEqual(1.15, Arithmetic
                         .solve_expression(self.ex11, self.vars, self.worker))
        self.assertEqual(14, Arithmetic
                         .solve_expression(self.ex12, self.vars, self.worker))
        self.assertEqual("AbbA17", Arithmetic
                         .solve_expression(self.ex13, self.vars, self.worker))
        self.assertEqual("BaAb", Arithmetic
                         .solve_expression(self.ex14, self.vars, self.worker))
        self.assertEqual(10.0, Arithmetic
                         .solve_expression(self.ex15, self.vars, self.worker))
        self.assertEqual(21.0, Arithmetic
                         .solve_expression(self.ex16, self.vars, self.worker))

    def test_sum(self):
        ops1 = ["10", "20"]
        ops2 = ["A", "0.5"]
        ops3 = ["A", "B"]
        ops4 = ["\"Hello\"", "\", world\"", "\'!\'"]
        ops5 = ["Q", "10"]
        ops6 = ["\'h", "\"ello"]
        ops7 = ["\'H\'", "ello"]
        ops8 = ["10", "\"Balls\""]
        ops9 = ["random", "E i"]
        ops10 = ["get default name", "\", hello!\""]
        ops11 = ["some method", "10"]
        ops12 = ["get flag", "10"]
        self.assertEqual(30, Arithmetic
                         .sum_operands(ops1, self.vars, self.worker))
        self.assertEqual(11, Arithmetic
                         .sum_operands(ops2, self.vars, self.worker))
        self.assertEqual(18.5, Arithmetic
                         .sum_operands(ops3, self.vars, self.worker))
        self.assertEqual("Hello, world!", Arithmetic
                         .sum_operands(ops4, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.sum_operands,
                          ops5, self.vars, self.worker)
        self.assertRaises(ArithmeticError, Arithmetic.sum_operands,
                          ops6, self.vars, self.worker)
        self.assertRaises(ArithmeticError, Arithmetic.sum_operands,
                          ops7, self.vars, self.worker)
        self.assertEqual("10Balls", Arithmetic
                         .sum_operands(ops8, self.vars, self.worker))
        self.assertEqual(44.0, Arithmetic
                         .sum_operands(ops9, self.vars, self.worker))
        self.assertEqual("Ivan, hello!", Arithmetic
                         .sum_operands(ops10, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.sum_operands,
                          ops11, self.vars, self.worker)
        self.assertRaises(ValueError, Arithmetic.sum_operands,
                          ops12, self.vars, self.worker)

    def test_sub(self):
        ops1 = ["10", "20"]
        ops2 = ["A", "0.5"]
        ops3 = ["A", "B"]
        ops4 = ["\"really\"", 10]
        ops5 = ["random", "E i"]
        self.assertEqual(-10, Arithmetic.sub_operands(ops1, self.vars,
                                                      self.worker))
        self.assertEqual(10, Arithmetic.sub_operands(ops2, self.vars,
                                                     self.worker))
        self.assertEqual(2.5, Arithmetic.sub_operands(ops3, self.vars,
                                                      self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.sub_operands,
                          ops4, self.vars, self.worker)
        self.assertEqual(40.0, Arithmetic.sub_operands(ops5, self.vars,
                                                       self.worker))

    def test_mult(self):
        ops1 = ["10", "20"]
        ops2 = ["A", "8"]
        ops3 = ["A", "B"]
        ops4 = ["\"really\"", 10]
        ops5 = ["random", "E 1"]
        self.assertEqual(200, Arithmetic.mult_operands(ops1, self.vars,
                                                       self.worker))
        self.assertEqual(84.0, Arithmetic.mult_operands(ops2, self.vars,
                                                        self.worker))
        self.assertEqual(84.0, Arithmetic.mult_operands(ops3, self.vars,
                                                        self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.mult_operands,
                          ops4, self.vars, self.worker)
        self.assertEqual(42.0, Arithmetic.mult_operands(ops5, self.vars,
                                                        self.worker))

    def test_div(self):
        ops1 = ["10", "20"]
        ops2 = ["A", "8"]
        ops3 = ["A", "B"]
        ops4 = ["\"really\"", 10]
        ops5 = ["random", "E i"]
        self.assertEqual(0.5, Arithmetic.div_operands(ops1, self.vars,
                                                      self.worker))
        self.assertEqual(10.5 / 8, Arithmetic.div_operands(ops2, self.vars,
                                                           self.worker))
        self.assertEqual(10.5 / 8, Arithmetic.div_operands(ops3, self.vars,
                                                           self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.div_operands,
                          ops4, self.vars, self.worker)
        self.assertEqual(21.0, Arithmetic.div_operands(ops5, self.vars,
                                                       self.worker))

    def test_isnumber(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = None
        self.assertEqual(False, Arithmetic.isnumber(v1))
        self.assertEqual(False, Arithmetic.isnumber(v2))
        self.assertEqual(True, Arithmetic.isnumber(v3))
        self.assertEqual(True, Arithmetic.isnumber(v4))
        self.assertEqual(False, Arithmetic.isnumber(v5))
        self.assertEqual(False, Arithmetic.isnumber(v6))

    def test_isint(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = "5"
        v7 = None
        self.assertFalse(Arithmetic.isint(v1))
        self.assertFalse(Arithmetic.isint(v2))
        self.assertTrue(Arithmetic.isint(v3))
        self.assertFalse(Arithmetic.isint(v4))
        self.assertFalse(Arithmetic.isint(v5))
        self.assertTrue(Arithmetic.isint(v6))
        self.assertFalse(Arithmetic.isint(v7))

    def test_get_val_by_method(self):
        o1 = "Some method"
        o2 = "get default name"
        o3 = "random"
        o4 = "summator using E 1 and E i"
        self.assertRaises(ArithmeticError, Arithmetic.get_val_by_method,
                          o1, self.vars, self.worker)
        self.assertRaises(ValueError, Arithmetic.get_val_by_method,
                          o2, self.vars, self.worker)
        self.assertEqual(42.0, Arithmetic
                         .get_val_by_method(o3, self.vars, self.worker))
        self.assertEqual(3.0, Arithmetic
                         .get_val_by_method(o4, self.vars, self.worker))

    def test_get_name_var_and_index(self):
        o1 = "D"
        o2 = "var 1"
        o3 = "E 1"
        o4 = "E i"
        o5 = "E index"
        o6 = "E D"
        o7 = "E o"
        self.assertTupleEqual(("D", None), Arithmetic
                              .get_name_var_and_index(o1, self.vars,
                                                      self.worker))
        self.assertTupleEqual((None, None), Arithmetic
                              .get_name_var_and_index(o2, self.vars,
                                                      self.worker))
        self.assertTupleEqual(("E", 0), Arithmetic
                              .get_name_var_and_index(o3, self.vars,
                                                      self.worker))
        self.assertTupleEqual(("E", 1), Arithmetic
                              .get_name_var_and_index(o4, self.vars,
                                                      self.worker))
        self.assertTupleEqual((None, None), Arithmetic
                              .get_name_var_and_index(o5, self.vars,
                                                      self.worker))
        self.assertTupleEqual((None, None), Arithmetic
                              .get_name_var_and_index(o6, self.vars,
                                                      self.worker))
        self.assertTupleEqual((None, None), Arithmetic
                              .get_name_var_and_index(o7, self.vars,
                                                      self.worker))

    def test_change_var(self):
        # Addition
        e1 = "A plus D"
        e2 = "add A plus D"
        e3 = "add A to var"
        e4 = "add A to B"
        e5 = "add D to A"
        e6 = "add B to A"
        e7 = "add E 1 to E i"
        e8 = "add C to D"
        e9 = "add C to D to C"
        self.assertFalse(Arithmetic.change_var(e1, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e2, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e3, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.change_var,
                          e4, self.vars, self.worker)
        self.assertFalse(Arithmetic.change_var(e5, self.vars, self.worker))
        self.assertTrue(Arithmetic.change_var(e6, self.vars, self.worker))
        self.assertEqual(18.5, self.vars["A"][0])
        self.assertTrue(Arithmetic.change_var(e7, self.vars, self.worker))
        self.assertEqual(3.0, self.vars["E"][0][1])
        self.assertTrue(Arithmetic.change_var(e8, self.vars, self.worker))
        self.assertEqual("AbbA", self.vars["D"][0])
        self.assertFalse(Arithmetic.change_var(e9, self.vars, self.worker))
        # Subtraction
        e1 = "A minus D"
        e2 = "subtract A minus D"
        e3 = "subtract A from var"
        e4 = "subtract A from B"
        e5 = "subtract B from A"
        e6 = "subtract E 1 from E i"
        e7 = "subtract B from A from A"
        self.assertFalse(Arithmetic.change_var(e1, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e2, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e3, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.change_var,
                          e4, self.vars, self.worker)
        self.assertTrue(Arithmetic.change_var(e5, self.vars, self.worker))
        self.assertEqual(10.5, self.vars["A"][0])
        self.assertTrue(Arithmetic.change_var(e6, self.vars, self.worker))
        self.assertEqual(2.0, self.vars["E"][0][1])
        self.assertFalse(Arithmetic.change_var(e7, self.vars, self.worker))
        # multiplication
        e1 = "A times D"
        e2 = "multiply A times D"
        e3 = "multiply var to A"
        e4 = "multiply B to A"
        e5 = "multiply A to B"
        e6 = "multiply E 1 to E i"
        e7 = "multiply B to A to A"
        self.assertFalse(Arithmetic.change_var(e1, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e2, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e3, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.change_var,
                          e4, self.vars, self.worker)
        self.assertTrue(Arithmetic.change_var(e5, self.vars, self.worker))
        self.assertEqual(84.0, self.vars["A"][0])
        self.assertTrue(Arithmetic.change_var(e6, self.vars, self.worker))
        self.assertEqual(2.0, self.vars["E"][0][0])
        self.assertFalse(Arithmetic.change_var(e7, self.vars, self.worker))
        # division
        e1 = "A divided by D"
        e2 = "divide A divided by D"
        e3 = "divide var by A"
        e4 = "divide B by A"
        e5 = "divide A by B"
        e6 = "divide E 1 by E i"
        e7 = "divide B by A by A"
        self.assertFalse(Arithmetic.change_var(e1, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e2, self.vars, self.worker))
        self.assertFalse(Arithmetic.change_var(e3, self.vars, self.worker))
        self.assertRaises(ArithmeticError, Arithmetic.change_var,
                          e4, self.vars, self.worker)
        self.assertTrue(Arithmetic.change_var(e5, self.vars, self.worker))
        self.assertEqual(10.5, self.vars["A"][0])
        self.assertTrue(Arithmetic.change_var(e6, self.vars, self.worker))
        self.assertEqual(1.0, self.vars["E"][0][0])
        self.assertFalse(Arithmetic.change_var(e7, self.vars, self.worker))

    def test_find_sum_strs(self):
        o1 = ["\"hello", "\'a"]
        o2 = ["\'", "\""]
        o3 = ["D", "A"]
        o4 = ["F 1", "F i"]
        o5 = ["\"ab\"", "\"ra\""]
        o6 = ["\'a\'", "\'b\'"]
        self.assertFalse(Arithmetic.find_sum_strs(o1, self.vars, self.worker))
        self.assertFalse(Arithmetic.find_sum_strs(o2, self.vars, self.worker))
        self.assertTrue(Arithmetic.find_sum_strs(o3, self.vars, self.worker))
        self.assertTrue(Arithmetic.find_sum_strs(o4, self.vars, self.worker))
        self.assertTrue(Arithmetic.find_sum_strs(o5, self.vars, self.worker))
        self.assertTrue(Arithmetic.find_sum_strs(o6, self.vars, self.worker))


if __name__ == "__main__":
    unittest.main()
