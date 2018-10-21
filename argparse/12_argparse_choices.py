#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--count", action='store', choices=["ack-time", "send-time"],
                    help="count the given string from log files")
args = parser.parse_args()
print("args", args)
