#! /usr/bin/env python3
'''
Niema Moshiri 2016

Convert MSA from FASTA to Phylip
'''
import argparse
from common import readFASTA
from sys import stdin,stdout

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
k = len(seqs[list(seqs.keys())[0]])
for key in seqs:
    assert len(seqs[key]) == k, "Sequences must be of same length"
outfile.write(" %d %d\n" % (len(seqs),k))
for key in seqs:
    outfile.write("%s %s\n" % (key,seqs[key]))
outfile.close()
