#! /usr/bin/env python
from sys import stdin,argv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
if len(argv) not in {2,4}:
    print("ERROR: Incorrect number of arguments. Use -h argument for help")
    exit(-1)
if argv[1] in {'-h','-help','--help'}:
    print("Creates histogram from list of numbers passed in via STDIN")
    print("USAGE: python histogram.py <title> <xlabel> <ylabel>")
    exit(0)
data = [float(i) for i in stdin.read().strip().split()]
fig, ax = plt.subplots()
#ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # integer ticks x axis
#ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) # integer ticks y axis
sns.distplot(data, kde=False) # kde=False removes the curve
plt.title(argv[1])
plt.xlabel(argv[2])
plt.ylabel(argv[3])
#plt.xlim(0,10) # x range
#plt.ylim(0,18) # y range
plt.tight_layout()
sns.plt.show()