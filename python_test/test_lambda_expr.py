#!/usr/bin/env python3
import unittest

from python_test import lambda_expr


class TestLambda(unittest.TestCase):

    def test_lambda(self):
        plus_ten_lambda = lambda x: x + 10
        self.assertEqual(plus_ten_lambda(1), lambda_expr.plus_ten(1))

    def test_lambda2(self):
        self.assertEqual((lambda x: x + 10)(1), lambda_expr.plus_ten(1))


if __name__ == '__main__':
    unittest.main()
