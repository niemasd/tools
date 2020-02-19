#! /usr/bin/env python3

# parse user arguments
import argparse
from sys import stdin
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
parser.add_argument('-ylog', '--ylog', action='store_true', help="Log-Scaled Y-Axis")
parser.add_argument('-yint', '--yint', action='store_true', help="Integer Ticks on Y-Axis")
parser.add_argument('-nx', '--no_x', action='store_true', help="Hide the Category (X-Axis) Labels")
args = parser.parse_args()
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)

# parse data
count = dict(); x = list()
for line in args.input.read().strip().splitlines():
    l = line.strip()
    if l in count:
        count[l] += 1
    else:
        count[l] = 1; x.append(l)
y = [count[l] for l in x]

# create figure+axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
fig, ax = plt.subplots()

# set integer ticks (if applicable)
if args.yint:
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# plot the barplot
sns.barplot(x=x, y=y, ax=ax)

# set figure title and labels (if applicable)
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

# log-scale the axes (if applicable)
if args.ylog:
    ax.set_yscale('log')

# set Y-axis range (if applicable)
if args.ymin is not None and args.ymax is not None:
    plt.ylim(args.ymin,args.ymax)
elif args.ymin is not None:
    plt.ylim(ymin=args.ymin)
elif args.ymax is not None:
    plt.ylim(ymax=args.ymax)

# hide category (X-axis) labels (if applicable)
if args.no_x:
    ax.set_xticks(list())

# clean up the figure and show
plt.tight_layout()
plt.show()
