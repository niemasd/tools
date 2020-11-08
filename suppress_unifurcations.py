#!/usr/bin/env python3
# Randomly resolve tree passed in via standard input
from sys import stdin
from treeswift import read_tree_newick
t = read_tree_newick(stdin.read())
t.suppress_unifurcations()
print(t.newick())
