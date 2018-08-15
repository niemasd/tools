#! /usr/bin/env python3
'''
Niema Moshiri 2017

Compute all pairwise Hamming distances from a given multiple sequence alignment
'''
import argparse
from sys import stdin,stdout
from common import hamming,readFASTA

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    parser.add_argument('-p', '--proportion', action='store_true', help="Hamming Distance as proportion of length (instead of count)")
    args = parser.parse_args()
    return args.input, args.output, args.proportion

# main code execution
infile, outfile, prop = parseArgs()
seqs = readFASTA(infile)
infile.close()
keys = list(seqs.keys())
L = None
for k in keys:
    if L is None:
        L = len(seqs[k])
    assert L == len(seqs[k]), "All sequences must be of equal length"
for i in range(len(keys)-1):
    for j in range(i+1,len(keys)):
        if prop:
            outfile.write('%f\n'%hamming(seqs[keys[i]],seqs[keys[j]],prop=True))
        else:
            outfile.write('%d\n'%hamming(seqs[keys[i]],seqs[keys[j]],prop=False))
