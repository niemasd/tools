#! /usr/bin/env python3
'''
Niema Moshiri 2017

Compute all pairwise Jukes-Cantor 69 (JC69) distances from a given multiple sequence alignment
'''
import argparse
from sys import stdin,stdout
from common import jc69,readFASTA

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    parser.add_argument('-a', '--alpha', required=False, type=float, default=float('inf'), help="Gamma distribution alpha parameter")
    args = parser.parse_args()
    return args.input, args.output, args.alpha

# main code execution
infile, outfile, alpha = parseArgs()
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
        outfile.write('%f\n'%jc69(seqs[keys[i]],seqs[keys[j]],alpha))
