#!/usr/bin/env python3

import argparse
import datetime


def valid_date_type(arg_date_str):
    try:
        datetime.datetime.strptime(arg_date_str, "%Y-%m-%d")
        return arg_date_str
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser()
parser.add_argument("--date", action='store', dest="date", type=valid_date_type, help="date input")
parser.add_argument("-m", action='store', dest="message", type=str, help="enter message")
parser.add_argument("-n", action='store', dest="number", type=int, help="enter number")
args = parser.parse_args()
print("args", args)
