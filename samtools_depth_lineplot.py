#! /usr/bin/env python3
'''
Niema Moshiri 2021

Create line plot(s) from samtools depth file(s)
'''
from gzip import open as gopen
from os.path import isdir,isfile
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
from seaborn import FacetGrid,lineplot,relplot
from sys import argv,stderr

# headless matplotlib
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# messages and constants
USAGE = "USAGE: %s <file1.depth.txt> [file2.depth.txt] [file3.depth.txt] ..." % argv[0]
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_PILEUP = "ERROR: File is not a samtools pileup output"
DUP_FILE = "ERROR: Duplicate file in arguments"
INCH_PER_SAMPLE = 2

# check for validity and load data
if len(argv) == 1 or argv[1].lower() in {'-h', '--help', '-help'}:
    print(USAGE, file=stderr); exit(1)
#x = list(); y = list(); sample = list(); fns = set()
data = dict()
for fn in argv[1:]:
    if not isfile(fn):
        if isdir(fn):
            print("%s: %s" % (FOLDER_NOT_FILE, fn), file=stderr)
        else:
            print("%s: %s" % (FILE_NOT_FOUND, fn), file=stderr)
        exit(1)
    fn_name = fn.split('/')[-1].strip()
    if fn_name in data:#fns:
        ptin("%s: %s" % (DUP_FILE, fn_name), file=stderr)
    #else:
    #    fns.add(fn_name)
    try:
        if fn.lower().endswith('.gz'):
            curr = [int(l.split('\t')[2]) for l in gopen(fn).read().decode().splitlines()]
        else:
            curr = [int(l.split('\t')[2]) for l in open(fn)]
        #sample += [fn_name]*len(curr); y += curr; x += [i+1 for i in range(len(curr))]
        data[fn] = curr#{'x': [i+1 for i in range(len(curr))], 'y':curr}
    except:
        print("%s: %s" % (NOT_PILEUP, fn), file=stderr); exit(1)
fns = sorted(data.keys())

# create line plots
XMAX = max(len(data[fn]) for fn in data)+1
YMAX = max(max(data[fn]) for fn in data)
with PdfPages('depth_lineplot.pdf') as pdf_pages:
    for i,fn in enumerate(fns):
        fig = plt.figure(i)
        plt.plot([1+i for i in range(len(data[fn]))], data[fn])
        plt.xlim((1,XMAX))
        plt.ylim((1,YMAX))
        plt.yscale('log')
        plt.xlabel('Genome Position')
        plt.ylabel('Mapping Depth')
        plt.title(fn, fontsize=8)
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        pdf_pages.savefig(fig)
        plt.close(fig)
