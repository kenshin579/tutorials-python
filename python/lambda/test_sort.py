#!/usr/bin/env python3
import unittest

from python_test import sort


class SortTest(unittest.TestCase):
    student_list = [
        {'name': 'Homer', 'age': 39},
        {'name': 'Homer1', 'age': 20},
        {'name': 'Homer2', 'age': 5},
        {'name': 'Bart', 'age': 10},
    ]

    def setup(self):
        print('setUp is called')

    def test_simple_sort(self):
        a_list = [3, 2, 1, 7]
        a_list.sort()
        self.assertEqual(a_list, [1, 2, 3, 7])

    def test_simple_sorted(self):
        a_list = [3, 2, 1, 7]
        new_list = sorted(a_list)
        self.assertEqual(new_list, [1, 2, 3, 7])

    def test_sort_list_by_age_using_lambda(self):
        result = sort.sort_list_by_age_using_lambda(self.student_list)
        for i in range(len(result) - 1):
            print(i, result[i].get('age'))
            self.assertLess(result[i].get('age'), result[i + 1].get('age'))

    def test_sort_list_by_age_using_itemgetter(self):
        result = sort.sort_list_by_age_using_itemgetter(self.student_list)
        for i in range(len(result) - 1):
            print(i, result[i].get('age'))
            self.assertLess(result[i].get('age'), result[i + 1].get('age'))

    @unittest.skip
    def test_sort_list_by_age_using_cmp_lambda(self):
        result = sort.sort_list_by_age_using_cmp_lambda(self.student_list)
        for i in range(len(result) - 1):
            print(i, result[i].get('age'))
            self.assertLess(result[i].get('age'), result[i + 1].get('age'))

    def test_sort_list_by_two_keys_using_itemgetter(self):
        student_list = [
            {'name': 'Homer', 'age': 39},
            {'name': 'Homer2', 'age': 5},
            {'name': 'Homer3', 'age': 5},
            {'name': 'Bart', 'age': 10},
        ]
        result = sort.sort_list_by_two_keys_using_itemgetter(student_list)
        for i in range(len(result) - 1):
            if result[i].get('age') == result[i + 1].get('age'):
                self.assertLess(result[i].get('name'), result[i + 1].get('name'))
            else:
                self.assertLess(result[i].get('age'), result[i + 1].get('age'))

    def test_sort_list_by_two_keys_using_lambda(self):
        student_list = [
            {'name': 'Homer', 'age': 39},
            {'name': 'Homer2', 'age': 5},
            {'name': 'Homer3', 'age': 5},
            {'name': 'Bart', 'age': 10},
        ]
        result = sort.sort_list_by_two_keys_using_lambda(student_list)
        for i in range(len(result) - 1):
            if result[i].get('age') == result[i + 1].get('age'):
                self.assertLess(result[i].get('name'), result[i + 1].get('name'))
            else:
                self.assertLess(result[i].get('age'), result[i + 1].get('age'))


if __name__ == '__main__':
    unittest.main()
