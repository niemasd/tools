#! /usr/bin/env python3
'''
Niema Moshiri 2017

Subsample the leaves of a given Newick file
'''
import argparse
from random import sample
from sys import stdin,stdout
from treeswift import read_tree_newick

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input Newick Tree")
    parser.add_argument('-o', '--output', required=False, type=argparse.FileType('w'), default=stdout, help="Output")
    parser.add_argument('-p', '--proportion', required=False, type=float, default=None, help="Proportion of Original Leaves to Sample")
    parser.add_argument('-n', '--number', required=False, type=int, default=None, help="Number of Leaves to Sample")
    args = parser.parse_args()
    assert args.proportion is not None or args.number is not None, "Must specify either proportion or number"
    assert args.proportion is None or args.number is None, "Cannot specify both proportion and number"
    if args.proportion is not None:
        assert args.proportion > 0 and args.proportion <= 1, "Proportion must be between 0 and 1"
    else:
        assert args.number > 0, "Number must be positive"
    return args.input, args.output, args.proportion, args.number

# main code execution
infile, outfile, p, n = parseArgs()
tree = read_tree_newick(infile.read())
infile.close()
leaves = [l.label for l in tree.traverse_leaves()]
if p is not None:
    out_labels = sample(leaves,int(p*len(leaves)))
else:
    out_labels = sample(leaves,n)
outfile.write(tree.extract_tree_with(out_labels).newick()); outfile.write('\n'); outfile.close()
