import unittest
from comparison import Comparison
from program import Program
from variables_types import TypeVariable


class TestComparison(unittest.TestCase):
    def setUp(self):
        program = Program("../test.fpp")
        self.worker = program.worker
        current_class, current_method, i = program.find_main_method()
        self.worker.set_up(current_class, current_method,
                           program.classes, program)
        self.vars = {"A": (10, TypeVariable.number, False),
                     "B": (False, TypeVariable.logic, True),
                     "C": ("ABC", TypeVariable.phrase, False),
                     "D": ("abc", TypeVariable.phrase, False),
                     "E": (20, TypeVariable.number, False),
                     "F": ([1.0, 2.0, 3.0, 4.0], TypeVariable.arrayNumbers,
                           False, TypeVariable.number),
                     "G": (True, TypeVariable.logic, False),
                     "i": (3.0, TypeVariable.number, False)}
        self.worker.vars = {current_method: self.vars}
        self.worker.program.worker = self.worker
        self.op1 = "10 is 10"
        self.op2 = "A was 10"
        self.op3 = "B have no"
        self.op4 = "10 isn\'t 1"
        self.op5 = "A are not B"
        self.op6 = "D is less than C"
        self.op7 = "\'A\' are less than \'B\'"
        self.op8 = "C isn\'t more than D"
        self.op9 = "\'A\' are not more than \'B\'"
        self.op10 = "15 is not greater than 20"
        self.op11 = "20 is greater than 15"
        self.op12 = "C are more than D"
        self.op13 = "20 is not less than 20"
        self.op14 = "E aren\'t less than A"
        self.op15 = "30 is A added to E"
        self.op16 = "A times 10 is less than multiply A and E"
        self.op17 = "G"
        self.op18 = "F 1 is 1"
        self.op19 = "F 1 times 42 is random"
        self.op20 = "random is 42"
        self.op21 = "G"

    def test_parse_type_operand(self):
        self.assertEqual("Equal", Comparison.parse_type_operand(self.op1))
        self.assertEqual("Equal", Comparison.parse_type_operand(self.op2))
        self.assertEqual("Equal", Comparison.parse_type_operand(self.op3))
        self.assertEqual("Not equal", Comparison
                         .parse_type_operand(self.op4))
        self.assertEqual("Not equal", Comparison
                         .parse_type_operand(self.op5))
        self.assertEqual("Less", Comparison.parse_type_operand(self.op6))
        self.assertEqual("Less", Comparison.parse_type_operand(self.op7))
        self.assertEqual("Less or equal", Comparison
                         .parse_type_operand(self.op8))
        self.assertEqual("Less or equal", Comparison
                         .parse_type_operand(self.op9))
        self.assertEqual("Less or equal", Comparison
                         .parse_type_operand(self.op10))
        self.assertEqual("Greater", Comparison
                         .parse_type_operand(self.op11))
        self.assertEqual("Greater", Comparison
                         .parse_type_operand(self.op12))
        self.assertEqual("Greater or equal", Comparison
                         .parse_type_operand(self.op13))
        self.assertEqual("Greater or equal", Comparison
                         .parse_type_operand(self.op14))
        self.assertEqual("Equal", Comparison.parse_type_operand(self.op15))
        self.assertEqual("Less", Comparison.parse_type_operand(self.op16))
        self.assertIsNone(Comparison.parse_type_operand(self.op21))

    def test_solve_operand(self):
        self.assertTrue(Comparison.solve_operand(self.op1, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op2, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op3, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op4, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op5, self.vars,
                                                 self.worker))
        self.assertFalse(Comparison.solve_operand(self.op6, self.vars,
                                                  self.worker))
        self.assertTrue(Comparison.solve_operand(self.op7, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op8, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op9, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op10, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op11, self.vars,
                                                 self.worker))
        self.assertFalse(Comparison.solve_operand(self.op12, self.vars,
                                                  self.worker))
        self.assertTrue(Comparison.solve_operand(self.op13, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op14, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op15, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op16, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op17, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op18, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op19, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op20, self.vars,
                                                 self.worker))
        self.assertTrue(Comparison.solve_operand(self.op21, self.vars,
                                                 self.worker))
        exop1 = "not " + self.op1
        exop2 = "not " + self.op5
        exop3 = "it’s not the case that " + self.op16
        exop4 = "it’s not the case that " + self.op21
        self.assertFalse(Comparison.solve_operand(exop1, self.vars,
                                                  self.worker))
        self.assertFalse(Comparison.solve_operand(exop2, self.vars,
                                                  self.worker))
        self.assertFalse(Comparison.solve_operand(exop3, self.vars,
                                                  self.worker))
        self.assertFalse(Comparison.solve_operand(exop4, self.vars,
                                                  self.worker))

    def test_solve_operands(self):
        # expr_1 and expr_2 and ...
        ops1 = [self.op1, self.op2]
        ops2 = [self.op3]
        ops3 = [self.op11, self.op6]
        ops4 = [self.op1, self.op2, self.op3, self.op4,
                self.op5, self.op8, self.op9]
        ops5 = ["it’s not the case that " + self.op1, self.op2]
        ops6 = [self.op21, "B"]
        ops7 = [self.op19, self.op20]
        self.assertTrue(Comparison.solve_operands(ops1, self.vars,
                                                  self.worker))
        self.assertTrue(Comparison.solve_operands(ops2, self.vars,
                                                  self.worker))
        self.assertFalse(Comparison.solve_operands(ops3, self.vars,
                                                   self.worker))
        self.assertTrue(Comparison.solve_operands(ops4, self.vars,
                                                  self.worker))
        self.assertFalse(Comparison.solve_operands(ops5, self.vars,
                                                   self.worker))
        self.assertFalse(Comparison.solve_operands(ops6, self.vars,
                                                   self.worker))
        self.assertTrue(Comparison.solve_operands(ops7, self.vars,
                                                  self.worker))

    def test_solve_expression(self):
        # expr_1 [and/or] expr_2 [and/or] ...
        ex1 = self.op1 + " or " + self.op2
        ex2 = self.op3 + " and " + self.op4 + " or " + \
                                              self.op5 + " and " + self.op6
        ex3 = self.op11
        ex4 = "not " + self.op3 + " and " + self.op4 + " or " \
              + self.op5 + " and " + self.op6
        self.assertTrue(Comparison.solve_expression(ex1, self.vars,
                                                    self.worker))
        self.assertTrue(Comparison.solve_expression(ex2, self.vars,
                                                    self.worker))
        self.assertTrue(Comparison.solve_expression(ex3, self.vars,
                                                    self.worker))
        self.assertFalse(Comparison.solve_expression(ex4, self.vars,
                                                     self.worker))

    def test_isnumber(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = None
        self.assertEqual(False, Comparison.isnumber(v1))
        self.assertEqual(False, Comparison.isnumber(v2))
        self.assertEqual(True, Comparison.isnumber(v3))
        self.assertEqual(True, Comparison.isnumber(v4))
        self.assertEqual(False, Comparison.isnumber(v5))
        self.assertEqual(False, Comparison.isnumber(v6))

    def test_isint(self):
        v1 = "qwe"
        v2 = ""
        v3 = "120"
        v4 = "120.5"
        v5 = "12 + 2j"
        v6 = "5"
        v7 = None
        self.assertFalse(Comparison.isint(v1))
        self.assertFalse(Comparison.isint(v2))
        self.assertTrue(Comparison.isint(v3))
        self.assertFalse(Comparison.isint(v4))
        self.assertFalse(Comparison.isint(v5))
        self.assertTrue(Comparison.isint(v6))
        self.assertFalse(Comparison.isint(v7))

    def test_get_val_in_array(self):
        v1 = "D"
        v2 = "F index"
        v3 = "F 0"
        v4 = "F 1"
        v5 = "F i"
        self.assertIsNone(Comparison.get_val_in_array(v1, "D", self.vars,
                                                      self.worker))
        self.assertIsNone(Comparison.get_val_in_array(v2, "F", self.vars,
                                                      self.worker))
        self.assertIsNone(Comparison.get_val_in_array(v3, "F", self.vars,
                                                      self.worker))
        self.assertEqual(1.0, Comparison.get_val_in_array(v4, "F", self.vars,
                                                          self.worker))
        self.assertEqual(3.0, Comparison.get_val_in_array(v5, "F", self.vars,
                                                          self.worker))

    def test_parse_val(self):
        v1 = "A"
        v2 = "F i"
        v3 = "10"
        v4 = "11.1"
        v5 = ""
        v6 = "\"Hello\'"
        v7 = "\'Hello\""
        v8 = "\"Qre"
        v9 = "Qre\""
        v10 = "\'a"
        v11 = "a\'"
        v12 = "\'abs\'"
        v13 = "\'a\'"
        v14 = "no"
        v15 = "false"
        v16 = "yes"
        v17 = "correct"
        v18 = "F i plus random"
        v19 = "random"
        v20 = "Variable"
        self.assertEqual(10.0, Comparison.parse_val(v1, self.vars,
                                                    self.worker))
        self.assertEqual(3.0, Comparison.parse_val(v2, self.vars,
                                                   self.worker))
        self.assertEqual(10.0, Comparison.parse_val(v3, self.vars,
                                                    self.worker))
        self.assertEqual(11.1, Comparison.parse_val(v4, self.vars,
                                                    self.worker))
        self.assertIsNone(Comparison.parse_val(v5, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v6, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v7, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v8, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v9, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v10, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v11, self.vars, self.worker))
        self.assertIsNone(Comparison.parse_val(v12, self.vars, self.worker))
        self.assertEqual("a", Comparison.parse_val(v13, self.vars,
                                                   self.worker))
        self.assertFalse(Comparison.parse_val(v14, self.vars, self.worker))
        self.assertFalse(Comparison.parse_val(v15, self.vars, self.worker))
        self.assertTrue(Comparison.parse_val(v16, self.vars, self.worker))
        self.assertTrue(Comparison.parse_val(v17, self.vars, self.worker))
        self.assertEqual(45.0, Comparison.parse_val(v18, self.vars,
                                                    self.worker))
        self.assertEqual(42.0, Comparison.parse_val(v19, self.vars,
                                                    self.worker))
        self.assertIsNone(Comparison.parse_val(v20, self.vars, self.worker))


if __name__ == "__main__":
    unittest.main()
