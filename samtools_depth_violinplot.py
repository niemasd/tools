#! /usr/bin/env python3
'''
Niema Moshiri 2021

Create a violin plot from samtools depth file(s)
'''
from gzip import open as gopen
from os.path import isdir,isfile
from seaborn import violinplot
from sys import argv,stderr
import matplotlib.pyplot as plt

# messages and constants
USAGE = "USAGE: %s <file1.depth.txt> [file2.depth.txt] [file3.depth.txt] ..." % argv[0]
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_PILEUP = "ERROR: File is not a samtools pileup output"
DUP_FILE = "ERROR: Duplicate file in arguments"
INCH_PER_SAMPLE = 0.25

# check for validity and load data
if len(argv) == 1 or argv[1].lower() in {'-h', '--help', '-help'}:
    print(USAGE, file=stderr); exit(1)
x = list(); y = list(); fns = set()
for fn in argv[1:]:
    if not isfile(fn):
        if isdir(fn):
            print("%s: %s" % (FOLDER_NOT_FILE, fn), file=stderr)
        else:
            print("%s: %s" % (FILE_NOT_FOUND, fn), file=stderr)
        exit(1)
    fn_name = fn.split('/')[-1].strip()
    if fn_name in fns:
        ptin("%s: %s" % (DUP_FILE, fn_name), file=stderr)
    else:
        fns.add(fn_name)
    try:
        if fn.lower().endswith('.gz'):
            curr = [int(l.split('\t')[2]) for l in gopen(fn).read().decode().splitlines()]
        else:
            curr = [int(l.split('\t')[2]) for l in open(fn)]
        x += [fn_name]*len(curr); y += curr
    except:
        print("%s: %s" % (NOT_PILEUP, fn), file=stderr); exit(1)

# create violin plot
try:
    fig, ax = plt.subplots()
    headless = False
except:
    import matplotlib
    matplotlib.use('Agg')
    fig, ax = plt.subplots()
    headless = True
fig.set_size_inches(INCH_PER_SAMPLE*len(fns), 4.8)
violinplot(x=x, y=y)
plt.ylim(ymin=1)
ax.set_yscale('log')
plt.title("Distribution of Mapping Depth")
plt.xlabel("Sample")
plt.ylabel("Mapping Depth (per site)")
plt.xticks(rotation=90)
fig.savefig('depth_violin.pdf', format='pdf', bbox_inches='tight')
