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


    def test_sort_list_by_age_using_lambda(self):
        sorted_list_by_age = sort.sort_list_by_age_using_lambda(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))


    def test_sort_list_by_age_using_itemgetter(self):
        sorted_list_by_age = sort.sort_list_by_age_using_itemgetter(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))

    def test_sort_list_by_age_using_cmp_lambda(self):
        sorted_list_by_age = sort.sort_list_by_age_using_cmp_lambda(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))


if __name__ == '__main__':
    unittest.main()