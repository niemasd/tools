#! /usr/bin/env python3
'''
Niema Moshiri 2017

Compute all patristic distances from the given tree
'''
import argparse
from sys import stdin,stdout
from treeswift import read_tree_newick

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input FASTA")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    args = parser.parse_args()
    return args.input, args.output

# main code execution
infile, outfile = parseArgs()
dm = read_tree_newick(infile.read()).distance_matrix()
infile.close()
keys = list(dm.keys())
for i in range(len(keys)-1):
    for j in range(i+1,len(keys)):
        outfile.write('%f\n'%dm[keys[i]][keys[j]])
