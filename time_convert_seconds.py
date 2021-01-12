#! /usr/bin/env python3
'''
Niema Moshiri 2021

Convert ##m##s time to seconds
'''
import argparse
from sys import stdin

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input GNU Time Measurements")
    args = parser.parse_args()
    return args.input

# main code execution
for l in parseArgs():
    if len(l.strip()) == 0:
        continue
    c1,c2 = [v.strip() for v in l.strip().split()]
    m,s = [float(v) for v in c2.rstrip('s').split('m')]
    print("%s\t%f" % (c1, 60*m + s))
