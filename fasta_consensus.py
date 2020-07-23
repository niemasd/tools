#! /usr/bin/env python3

# parse user arguments
from sys import stdin,stdout
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File Stream")
parser.add_argument('-l', '--ignore_length', action='store_true', help="Don't check sequence lengths")
args = parser.parse_args()
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)
if args.output == 'stdout':
    args.output = stdout
else:
    args.output = open(args.output)

# compute position symbol counts
count = list(); col = 0
for line in args.input:
    l = line.strip()
    if len(l) == 0:
        continue
    if l[0] == '>':
        if not args.ignore_length and col != len(count):
            raise ValueError("Sequence lengths differ")
        col = 0
    else:
        for i in range(len(l)):
            if col >= len(count):
                count.append(dict())
            if l[i] not in count[col]:
                count[col][l[i]] = 0
            count[col][l[i]] += 1; col += 1
if not args.ignore_length and col != len(count):
    raise ValueError("Sequence lengths differ")

# output consensus
for c in count:
    if '-' in c and len(c) != 1:
        del c['-']
    nuc = max(c.keys(), key=lambda x: c[x])
    args.output.write(nuc)
args.output.write('\n')
