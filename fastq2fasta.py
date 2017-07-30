#! /usr/bin/env python3

# parse user arguments
from sys import stdin
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
args = parser.parse_args()
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)
c = 0
for line in args.input:
    i = c%4
    if i == 0:
        print(">%s" % line.strip()[1:])
    elif i == 1:
        print(line.strip())
    c += 1