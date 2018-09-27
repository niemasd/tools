#! /usr/bin/env python3
'''
Niema Moshiri 2018

Replace ambiguous characters of a DNA FASTA with gaps
'''
import argparse
from random import sample
from sys import stdin,stdout
from common import readFASTA
VALID = {'A','C','G','T'}
GAP = '-'

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    args = parser.parse_args()
    return args.input, args.output

# main code execution
infile, outfile = parseArgs()
seqs = readFASTA(infile)
infile.close()
for key in seqs:
    outfile.write('>%s\n'%key)
    for c in seqs[key]:
        if c.upper() in VALID:
            outfile.write(c)
        else:
            outfile.write(GAP)
    outfile.write('\n')
outfile.close()
