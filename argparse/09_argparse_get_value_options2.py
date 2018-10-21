#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", action='store', dest="date", help="date input")
parser.add_argument("-m", action='store', dest="message", type=str, help="enter message")
parser.add_argument("-n", action='store', dest="number", type=int, help="enter number")
args = parser.parse_args()
print("args", args)

