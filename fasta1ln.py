#! /usr/bin/env python3
'''
Niema Moshiri 2017

Convert multiline FASTA to one-line
'''
import argparse
from sys import stdin
from common import convert_fasta_1ln

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    args = parser.parse_args()
    return args.input

# main code execution
infile = parseArgs()
convert_fasta_1ln(infile)
