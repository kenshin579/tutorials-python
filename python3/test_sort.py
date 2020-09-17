from unittest import TestCase

from python3 import sort


class Test(TestCase):
    def test_sort_list_by_age(self):
        student_list = [
            {'name': 'Homer', 'age': 39},
            {'name': 'Homer1', 'age': 20},
            {'name': 'Homer2', 'age': 5},
            {'name': 'Bart', 'age': 10},
        ]

        sorted_list_by_age = sort.sort_list_by_age(student_list)
        for i in range(len(sorted_list_by_age)):
            print(i, sorted_list_by_age[i].get('age'))
            # self.assertGreater(sorted_list_by_age[i].get('age'), sorted_list_by_age[i + 1].get('age'))
        # for i, student in enumerate(sorted_list_by_age):
        # print(i, student)
        # print(sorted_list_by_age)
        # self.assertGreater(student[i].age)
