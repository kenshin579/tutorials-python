from unittest import TestCase

from python3 import sort


class Test(TestCase):
    def setup(self):
        self. student_list = [
            {'name': 'Homer', 'age': 39},
            {'name': 'Homer1', 'age': 20},
            {'name': 'Homer2', 'age': 5},
            {'name': 'Bart', 'age': 10},
        ]


    def sort_list_by_age_using_lambda(self):

        sorted_list_by_age = sort.sort_list_by_age_using_lambda(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))


    def sort_list_by_age_using_itemgetter(self):

        sorted_list_by_age = sort.sort_list_by_age_using_itemgetter(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))

    def sort_list_by_age_using_cmp_lambda(self):

        sorted_list_by_age = sort.sort_list_by_age_using_cmp_lambda(self.student_list)
        for i in range(len(sorted_list_by_age) - 1):
            print(i, sorted_list_by_age[i].get('age'))
            self.assertLess(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))