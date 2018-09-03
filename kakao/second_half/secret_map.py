#!/usr/bin/env python3
import sys


def main():
    pass


def solution(n, arr1, arr2):
    result = []
    arr1_list = []
    arr2_list = []
    for x in arr1:
        bin_arr1 = list("{:05b}".format(x))
        arr1_list.append(bin_arr1)

    for x in arr2:
        bin_arr2 = list("{:05b}".format(x))
        arr2_list.append(bin_arr2)

    for i, one_digit in enumerate(arr1_list):
        str = ""
        for j, x in enumerate(one_digit):
            y = arr2_list[i][j]
            or_r = int(x) | int(y)
            if or_r == 1:
                str = str + "#"
            else:
                str = str + " "
        result.append(str)
    return result


if __name__ == "__main__":
    sys.exit(main())
