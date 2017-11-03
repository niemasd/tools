#!/usr/bin/env python3
'''
Convert names of FASTA file to random safe names.
Sequences are output to STDOUT.
Dictionary of name mappings is output to STDERR.
'''
from common import ran_str,readFASTA
K = 20 # safenames will be length 20
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

from sys import stdin,stderr
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
args = parser.parse_args()
seqs = readFASTA(args.input)
map = {}
for key in seqs:
    safe = ran_str(ALPHABET,K)
    while safe in map:
        safe = ran_str(ALPHABET,K)
    map[safe] = key
    print('>%s\n%s\n' % (safe,seqs[key]))
print(str(map), file=stderr)
