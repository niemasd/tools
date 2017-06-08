#! /usr/bin/env python

# parse user arguments
from sys import stdin
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=file, default=stdin, help="Input file stream (JSON)")
parser.add_argument('-x', '--x', required=True, type=str, help="Key for X Values")
parser.add_argument('-y', '--y', required=True, type=str, help="Key for Y Values")
parser.add_argument('-in', '--inner', required=False, type=str, default=None, help="Violen interior")
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
args = parser.parse_args()

# create figure+axes
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
df = pd.DataFrame(eval(args.input.read()))
fig, ax = plt.subplots()

# plot the violin plots
sns.violinplot(data=df, x=args.x.strip(), y=args.y.strip(), inner=args.inner)

# set figure title and labels (if applicable)
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

# set Y-axis range (if applicable)
if args.ymin is not None and args.ymax is not None:
    plt.ylim(args.ymin,args.ymax)
elif args.ymin is not None:
    plt.ylim(ymin=args.ymin)
elif args.ymax is not None:
    plt.ylim(ymax=args.ymax)

# clean up the figure and show
plt.tight_layout()
sns.plt.show()