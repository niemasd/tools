#! /usr/bin/env python3
'''
Niema Moshiri 2017

Convert multiline FASTA to one-line
'''
import argparse
from sys import stdin

# convert multiline FASTA to one-line
def convert(stream):
    seq = ''
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            print(seq)
            print(l)
            seq = ''
        else:
            seq += l.strip()
    print(seq)

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    args = parser.parse_args()
    return args.input

# main code execution
if __name__ == "__main__":
    infile = parseArgs()
    convert(infile)