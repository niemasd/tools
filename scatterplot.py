#! /usr/bin/env python
# see pyplot documentation for help: https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plot

# parse user arguments
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-x', '--xvals', required=True, type=file, help="File with X values (whitespace-delimited)")
parser.add_argument('-y', '--yvals', required=True, type=file, help="File with Y values (whitespace-delimited)")
parser.add_argument('-c', '--color', required=False, type=str, default=None)
parser.add_argument('-ls', '--linestyle', required=False, type=str, default=None)
parser.add_argument('-lw', '--linewidth', required=False, type=float, default=None)
parser.add_argument('-m', '--marker', required=False, type=str, default=None)
parser.add_argument('-ms', '--markersize', required=False, type=float, default=None)
parser.add_argument('-t', '--title', required=False, type=str, default=None, help="Figure Title")
parser.add_argument('-xl', '--xlabel', required=False, type=str, default=None, help="X-Axis Label")
parser.add_argument('-yl', '--ylabel', required=False, type=str, default=None, help="Y-Axis Label")
parser.add_argument('-xmin', '--xmin', required=False, type=int, default=None, help="X-Axis Minimum")
parser.add_argument('-xmax', '--xmax', required=False, type=int, default=None, help="X-Axis Maximum")
parser.add_argument('-ymin', '--ymin', required=False, type=int, default=None, help="Y-Axis Minimum")
parser.add_argument('-ymax', '--ymax', required=False, type=int, default=None, help="Y-Axis Maximum")
parser.add_argument('-xint', '--xint', action='store_true', help="Integer Ticks on X-Axis")
parser.add_argument('-yint', '--yint', action='store_true', help="Integer Ticks on Y-Axis")
args = parser.parse_args()

# create histogram
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
x = [float(i) for i in args.xvals.read().split()]
y = [float(i) for i in args.yvals.read().split()]
assert len(x) == len(y), "X and Y must have the same number of elements"
fig, ax = plt.subplots()

# set integer ticks (if applicable)
if args.xint:
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
if args.yint:
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# plot the scatterplot
plt.plot(x, y, linestyle=args.linestyle, linewidth=args.linewidth, marker=args.marker, markersize=args.markersize, color=args.color)

# set figure title and labels (if applicable)
if args.title is not None:
    plt.title(args.title)
if args.xlabel is not None:
    plt.xlabel(args.xlabel)
if args.ylabel is not None:
    plt.ylabel(args.ylabel)

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
sns.plt.show()