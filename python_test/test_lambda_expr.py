from unittest import TestCase

from python_test import lambda_expr


class TestPlus_ten(TestCase):
    def test_plus_ten(self):
        self.fail()

    def test_lambda(self):
        plus_ten_lambda = lambda x : x + 10
        self.assertEqual(plus_ten_lambda(1), lambda_expr.plus_ten(1))
