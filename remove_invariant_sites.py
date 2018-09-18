#! /usr/bin/env python3
'''
Niema Moshiri 2017

Remove invariant sites from multiple sequence alignment.
'''
import argparse
from sys import stdin,stdout
from common import hamming,readFASTA

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    parser.add_argument('-p', '--proportion', required=False, type=float, default=1., help="Minimum proportion of sequences to remove site")
    args = parser.parse_args()
    return args.input, args.output, args.proportion

# main code execution
infile, outfile, prop = parseArgs()
seqs = readFASTA(infile)
infile.close()
L = None
for k in seqs:
    if L is None:
        L = len(seqs[k])
    assert L == len(seqs[k]), "All sequences must be of equal length"
freq = [dict() for _ in range(L)]
T = [int(len(seqs)*prop)]*L
for k in seqs:
    for i in range(L):
        c = seqs[k][i]
        if c == '-': # ignore gaps
            T[i] -= 1; continue
        elif c not in {'A','C','G','T'}:
            c = 'C' # resolve all ambiguities as C TODO REMOVE
        if c not in freq[i]:
            freq[i][c] = 0
        freq[i][c] += 1
to_remove = set()
for i in range(L):
    if max(freq[i].values()) >= T[i]:
        to_remove.add(i)
for k in seqs:
    outfile.write('>%s\n'%k)
    for i in range(L):
        if i not in to_remove:
            outfile.write(seqs[k][i])
    outfile.write('\n')
