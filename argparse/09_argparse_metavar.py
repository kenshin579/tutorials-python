#!/usr/bin/env python3

import argparse

TIMEOUT_DEFAULT=30

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument('-t', '--timeout', action='store', type=int, default=TIMEOUT_DEFAULT, metavar='SECS',
            help='Specify timeout period in seconds. Default is %(default)s')
args = parser.parse_args()
if args.verbose:
    print("timeout=", args.timeout)
