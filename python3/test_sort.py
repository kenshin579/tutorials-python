from unittest import TestCase


class Test(TestCase):
    def test_sort_list_by_age(self):
        student_list = [
            {'name': 'Homer', 'age': 39},
            {'name': 'Bart', 'age': 10}
        ]
        sort.sort_list_by_age(student_list)
        # self.fail()
