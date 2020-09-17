#!/usr/bin/env python3


def sort_list_by_age(student_list):
    print('list', student_list)
    return sorted(student_list, key=lambda k: k['age'])
