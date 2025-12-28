#!/usr/bin/env python3
import unittest
from functools import reduce


class TestLambda(unittest.TestCase):

    def test_lambda_single_parameter1(self):
        plus_ten_lambda = lambda x: x + 10
        result = plus_ten_lambda(1)
        self.assertEqual(result, 11)

    def test_lambda_single_parameter2(self):
        result = (lambda x: x + 10)(1)
        self.assertEqual(result, 11)

    def test_lambda_multiple_parameters(self):
        result = (lambda x, y: x + y)(1, 2)
        self.assertEqual(result, 3)

    def test_map(self):
        result = list(map(lambda x: x + 1, range(5)))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_reduce(self):
        result = reduce(lambda x, y: x + y, [1, 2, 3])
        self.assertEqual(result, 6)

    def test_filter(self):
        result = list(filter(lambda x: x > 5, range(10)))
        self.assertEqual(result, [6, 7, 8, 9])


if __name__ == '__main__':
    unittest.main()
