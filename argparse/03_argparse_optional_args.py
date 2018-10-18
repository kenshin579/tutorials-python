#!/usr/bin/env python3

import argparse

'''
Optional Argument 지정할때 
- action 키워드에 'store_true'값으로 지정하면, 해당 옵션이 명시될때 True값이 지정되고 없으면 False로 지정된다


Short Option 추가하려면
- 이렇게 추가하면 된다. ("-v", "--verbosity")
'''

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", action='store_true', help="increase output verbosity")
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")
