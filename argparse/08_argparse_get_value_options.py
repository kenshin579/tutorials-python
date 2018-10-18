#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument('-t', action='store', dest='title', type=str, required=True)
parser.add_argument('-m', action='store', dest='msg', type=str, required=True)
args = parser.parse_args()
if args.verbose:
    print("title=", args.title, "msg=", args.msg)
