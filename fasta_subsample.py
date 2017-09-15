#! /usr/bin/env python3
'''
Niema Moshiri 2017

Subsample the sequences of a given FASTA file
'''
import argparse
from random import sample
from sys import stdin,stdout

# read FASTA stream
def readFASTA(stream):
    seqs = {}
    name = None
    seq = ''
    for line in stream:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if name is not None:
                assert len(seq) != 0, "Malformed FASTA"
                seqs[name] = seq
            name = l[1:]
            assert name not in seqs, "Duplicate sequence ID: %s" % name
            seq = ''
        else:
            seq += l
    assert name is not None and len(seq) != 0, "Malformed FASTA"
    seqs[name] = seq
    return seqs

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    parser.add_argument('-p', '--proportion', required=False, type=float, default=None, help="Proportion of Original FASTA to Sample")
    parser.add_argument('-n', '--number', required=False, type=int, default=None, help="Number of Sequences to Sample")
    args = parser.parse_args()
    assert args.proportion is not None or args.number is not None, "Must specify either proportion or number"
    assert args.proportion is None or args.number is None, "Cannot specify both proportion and number"
    if args.proportion is not None:
        assert args.proportion > 0 and args.proportion <= 1, "Proportion must be between 0 and 1"
    else:
        assert args.number > 0, "Number must be positive"
    return args.input, args.output, args.proportion, args.number

# main code execution
if __name__ == "__main__":
    infile, outfile, p, n = parseArgs()
    seqs = readFASTA(infile)
    infile.close()
    if p is not None:
        out_keys = sample(seqs.keys(),int(p*len(seqs)))
    else:
        out_keys = sample(seqs.keys(),n)
    for key in out_keys:
        outfile.write('>%s\n%s\n' % (key,seqs[key]))
    outfile.close()
