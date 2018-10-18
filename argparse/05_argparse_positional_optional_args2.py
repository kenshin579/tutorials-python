#!/usr/bin/env python3

import argparse

'''
Combining Positional and Optional arguments
- acion='count' : 특정 옵션이 몇번 일어나는지 개수를 카운트하는 또 다른 action 타입이다.

'''

parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="increase output verbosity")
args = parser.parse_args()
print("args.verbosity", args.verbosity)
answer = args.square**2
if args.verbosity >= 2:
    print("the square of {} equals {}".format(args.square, answer))
elif args.verbosity >= 1:
    print("{}^2 == {}".format(args.square, answer))
else:
    print(answer)