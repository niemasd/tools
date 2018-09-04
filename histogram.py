#! /usr/bin/env python3

# parse user arguments
import argparse
from sys import stdin
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
parser.add_argument('-c', '--cumulative', action='store_true', help="Cumulative Density (instead of Probability Density)")
parser.add_argument('-k', '--kde', action='store_true', help="Show Kernel Density Estimation (KDE)")
parser.add_argument('-kl', '--kde_linestyle', required=False, type=str, default='-', help="KDE Linestyle")
parser.add_argument('-nh', '--nohist', action='store_true', help="Hide Histogram")
parser.add_argument('-b', '--binsize', required=False, type=float, default=None, help="Bin Size")
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-xmin', '--xmin', required=False, type=float, default=None, help="X-Axis Minimum")
parser.add_argument('-xmax', '--xmax', required=False, type=float, default=None, help="X-Axis Maximum")
parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
parser.add_argument('-xlog', '--xlog', action='store_true', help="Log-Scaled X-Axis")
parser.add_argument('-ylog', '--ylog', action='store_true', help="Log-Scaled Y-Axis")
parser.add_argument('-xint', '--xint', action='store_true', help="Integer Ticks on X-Axis")
parser.add_argument('-yint', '--yint', action='store_true', help="Integer Ticks on Y-Axis")
args = parser.parse_args()
assert args.kde or not args.nohist, "Must show either Histogram or Kernel Density Estimation (or both)"
if args.input == 'stdin':
    args.input = stdin
else:
    args.input = open(args.input)

# create figure+axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
data = [float(i) for i in args.input.read().strip().split()]
fig, ax = plt.subplots()

# set integer ticks (if applicable)
if args.xint:
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
if args.yint:
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# create custom bins (if applicable)
MIN = min(data); MAX = max(data)
if args.binsize:
    bins = [MIN]
    while bins[-1] < MAX:
        bins.append(bins[-1] + args.binsize)
else:
    bins = None

# plot the histogram
kde_kws = {'linestyle':args.kde_linestyle}; hist_kws = dict()
if args.cumulative:
    kde_kws['cumulative'] = True; hist_kws['cumulative'] = True
sns.distplot(data, bins=bins, kde=args.kde, hist=(not args.nohist), kde_kws=kde_kws, hist_kws=hist_kws)

# set figure title and labels (if applicable)
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

# log-scale the axes (if applicable)
if args.xlog:
    ax.set_xscale('log')
if args.ylog:
    ax.set_yscale('log')

# set X-axis range (if applicable)
if args.xmin is not None and args.xmax is not None:
    plt.xlim(args.xmin,args.xmax)
elif args.xmin is not None:
    plt.xlim(xmin=args.xmin)
elif args.xmax is not None:
    plt.xlim(xmax=args.xmax)

# set Y-axis range (if applicable)
if args.ymin is not None and args.ymax is not None:
    plt.ylim(args.ymin,args.ymax)
elif args.ymin is not None:
    plt.ylim(ymin=args.ymin)
elif args.ymax is not None:
    plt.ylim(ymax=args.ymax)

# clean up the figure and show
plt.tight_layout()
plt.show()