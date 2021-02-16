#! /usr/bin/env python3
'''
Niema Moshiri 2021

Trim the ends of a multiple sequence alignment (FASTA)
'''
import argparse
from sys import stdin,stdout

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output FASTA")
    parser.add_argument('-s', '--start', required=False, type=int, default=0, help="Length to Trim from Start")
    parser.add_argument('-e', '--end', required=False, type=int, default=0, help="Length to Trim from End")
    args = parser.parse_args()
    return args.input, args.output, args.start, args.end

# main code execution
infile, outfile, start, end = parseArgs()
assert start >= 0, "Length to trim from start must be non-negative integer"
assert end >= 0, "Length to trim from end must be non-negative integer"
curr_ID = None; curr_seq = None
for line in infile:
    l = line.strip()
    if len(l) == 0:
        continue
    if l[0] == '>':
        if curr_ID is not None:
            outfile.write("%s\n%s\n" % (curr_ID, curr_seq[start:-end]))
        curr_ID = l; curr_seq = ''
    else:
        assert curr_seq is not None, "Invalid input FASTA"
        curr_seq += l
if curr_ID is not None:
    outfile.write("%s\n%s\n" % (curr_ID, curr_seq[start:-end]))
infile.close(); outfile.close()
