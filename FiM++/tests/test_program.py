import unittest
from program import Program


class TestProgram(unittest.TestCase):
    def test_find_main_method(self):
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_main_method)
        p2 = Program("../test_pr_2.fpp")
        self.assertRaises(SyntaxError, p2.find_main_method)
        p3 = Program("../test.fpp")
        self.assertTupleEqual(("An example letter", "very much new", 20),
                              p3.find_main_method())

    def test_find_end_if(self):
        # when ifProgram fails
        p = Program("../examples/many ifs.fpp")
        self.assertEqual(12, p.find_end_if(4))
        self.assertEqual(11, p.find_end_if(6))
        self.assertEqual(10, p.find_end_if(8))
        self.assertEqual(29, p.find_end_if(14))
        self.assertEqual(18, p.find_end_if(16))
        self.assertEqual(27, p.find_end_if(20))
        self.assertEqual(24, p.find_end_if(22))
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_end_if, 3)

    def test_find_end_else(self):
        # when if done
        p = Program("../examples/many ifs.fpp")
        self.assertEqual(30, p.find_end_else(12))
        self.assertEqual(26, p.find_end_else(24))
        self.assertEqual(28, p.find_end_else(18))
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_end_else, 7)
        self.assertRaises(SyntaxError, p1.find_end_else, 13)

    def test_find_end_loop(self):
        # when loop finished
        p = Program("../examples/many loops.fpp")
        self.assertEqual(12, p.find_end_loop(4))
        self.assertEqual(11, p.find_end_loop(6))
        self.assertEqual(9, p.find_end_loop(7))
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_end_loop, 20)

    def test_find_next_case_switch(self):
        # when case fails
        p = Program("../examples/switch.fpp")
        self.assertEqual(7, p.find_next_case_switch(5))
        self.assertEqual(9, p.find_next_case_switch(7))
        self.assertEqual(11, p.find_next_case_switch(9))
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_next_case_switch, 26)

    def test_find_end_switch(self):
        # when case done
        p = Program("../examples/switch.fpp")
        self.assertEqual(13, p.find_end_switch(5))
        self.assertEqual(13, p.find_end_switch(7))
        self.assertEqual(13, p.find_end_switch(9))
        self.assertEqual(13, p.find_end_switch(11))
        p1 = Program("../test_pr_1.fpp")
        self.assertRaises(SyntaxError, p1.find_end_switch, 26)


if __name__ == "__main__":
    unittest.main()
