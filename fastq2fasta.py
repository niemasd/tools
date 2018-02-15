#! /usr/bin/env python3

# parse user arguments
from sys import stdin,stdout
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File Stream")
args = parser.parse_args()
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)
if args.output == 'stdout':
    args.output = stdout
else:
    args.output = open(args.output)
c = 0
for line in args.input:
    i = c%4
    if i == 0:
        args.output.write(">%s\n" % line.strip()[1:])
    elif i == 1:
        args.output.write("%s\n" % line.strip())
    c += 1