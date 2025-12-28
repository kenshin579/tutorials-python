#!/usr/bin/env python3
from _operator import itemgetter


def sort_list_by_age_using_lambda(student_list):
    return sorted(student_list, key=lambda k: k['age'])

def sort_list_by_two_keys_using_lambda(student_list):
    return sorted(student_list, key=lambda k: (k['age'], k['name']))

def sort_list_by_age_using_itemgetter(student_list):
    return sorted(student_list, key=itemgetter('age'))

def sort_list_by_two_keys_using_itemgetter(student_list):
    return sorted(student_list, key=itemgetter('age', 'name'))

def sort_list_by_age_using_cmp_lambda(student_list):
    return sorted(student_list, cmp=lambda x, y: cmp(x['age'], y['age']))