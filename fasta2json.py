#! /usr/bin/env python3
'''
Niema Moshiri 2016

Convert FASTA to JSON (keys = IDs, values = sequences). The key "__TYPE__" will
have a value of "DNA", "RNA", or "AMINO" depending on the alphabet.
'''
import argparse
from sys import stdin,stdout
from common import readFASTA

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
outfile.write(str(seqs))
outfile.close()
