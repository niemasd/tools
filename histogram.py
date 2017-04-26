#! /usr/bin/env python
from sys import stdin,argv
import matplotlib.pyplot as plt
import seaborn as sns
if len(argv) not in {2,4}:
    print("ERROR: Incorrect number of arguments. Use -h argument for help")
    exit(-1)
if argv[1] in {'-h','-help','--help'}:
    print("Creates histogram from list of numbers passed in via STDIN")
    print("USAGE: python histogram.py <title> <xlabel> <ylabel>")
    exit(0)
data = [int(i) for i in stdin.read().strip().split()]
sns.distplot(data)
plt.title(argv[1])
plt.xlabel(argv[2])
plt.ylabel(argv[3])
sns.plt.show()