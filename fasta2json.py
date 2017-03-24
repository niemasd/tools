#! /usr/bin/env python
'''
Niema Moshiri 2016

Convert FASTA to JSON (keys = IDs, values = sequences). The key "__TYPE__" will
have a value of "DNA", "RNA", or "AMINO" depending on the alphabet.
'''
import argparse
from sys import stdin,stdout
DNA = {'-','?','A','C','B','D','G','H','K','M','N','S','R','T','W','V','Y','X','a','c','b','d','g','h','k','m','n','s','r','t','w','v','y'}
RNA = {'-','?','A','C','B','D','G','H','K','M','N','S','R','U','W','V','Y','X','a','c','b','d','g','h','k','m','n','s','r','u','w','v','y'}
AMINO = {'-','?','A','C','B','E','D','G','F','I','H','K','M','L','N','Q','P','S','R','T','W','V','Y','X','Z','a','c','b','e','d','g','f','i','h','k','m','l','n','q','p','s','r','t','w','v','y','x','z'}

# read FASTA stream
def readFASTA(stream, alphabet):
    ALPHABET = {"DNA":DNA, "RNA":RNA, "AMINO":AMINO}[alphabet]
    invalid = {chr(i) for i in range(256) if chr(i) not in ALPHABET}
    seqs = {"__TYPE__":alphabet}
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
            for c in l:
                assert c not in invalid, "Invalid character: %s" % c
            seq += l
    assert name is not None and len(seq) != 0, "Malformed FASTA"
    seqs[name] = seq
    return seqs

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA (default: standard input)")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output (default: standard output)")
    parser.add_argument('-a', '--alphabet', required=True, type=str, help="Alphabet (DNA, RNA, or AMINO)")
    args = parser.parse_args()
    assert args.alphabet in {"DNA", "RNA", "AMINO"}, "Invalid alphabet: %s" % args.alphabet
    return args.input, args.output, args.alphabet

# main code execution
if __name__ == "__main__":
    infile, outfile, alphabet = parseArgs()
    seqs = readFASTA(infile,alphabet)
    infile.close()
    outfile.write(str(seqs))
    outfile.close()