#! /usr/bin/env python3
'''
Niema Moshiri 2017

Cut each sequence of a given FASTA stream to be length k
'''
import argparse
from sys import stdin
from common import cut_fasta_seqs

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-k', '--length', required=True, type=int, help="Sequence Length")
    args = parser.parse_args()
    return args.input,args.length

# main code execution
infile,k = parseArgs()
assert k > 0, "k must be a positive integer"
cut_fasta_seqs(infile,k)
