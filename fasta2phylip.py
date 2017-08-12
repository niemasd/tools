#! /usr/bin/env python3
'''
Niema Moshiri 2016

Convert MSA from FASTA to Phylip
'''
import argparse
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
    args = parser.parse_args()
    return args.input, args.output

# main code execution
if __name__ == "__main__":
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