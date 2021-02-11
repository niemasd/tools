#! /usr/bin/env python3
'''
Niema Moshiri 2021

For each <depth.txt>, call "GO" if <proportion> positions in the window from <start_pos> to <end_pos> have coverage above <cov_thres>, otherwise "NO GO"
'''
from gzip import open as gopen
from os.path import isdir,isfile
from sys import argv,stderr

# messages and constants
USAGE = "USAGE: %s <start_pos> <end_pos> <cov_thresh> <proportion> <file1.depth.txt> [file2.depth.txt] [file3.depth.txt] ..." % argv[0]
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_PILEUP = "ERROR: File is not a samtools pileup output"
DUP_FILE = "ERROR: Duplicate file in arguments"
MULTIPLE_REFS = "ERROR: Multiple reference IDs were found (needs to be exactly 1)"
INVALID_INT = "ERROR: Invalid integer"
INVALID_FLOAT = "ERROR: Invalid float"

# check for validity
if len(argv) < 6:
    print(USAGE, file=stderr); exit(1)
try:
    START = int(argv[1])
except:
    print("%s: %s" % (INVALID_INT, argv[1])); exit(1)
try:
    END = int(argv[2])
except:
    print("%s: %s" % (INVALID_INT, argv[2])); exit(1)
try:
    THRESH = int(argv[3])
except:
    print("%s: %s" % (INVALID_INT, argv[3])); exit(1)
try:
    PROP = float(argv[4])
except:
    print("%s: %s" % (INVALID_FLOAT, argv[4])); exit(1)
GO_NOGO_CUTOFF = (END-START+1)*PROP

# load data
data = dict(); ref_IDs = set()
for fn in argv[5:]:
    if not isfile(fn):
        if isdir(fn):
            print("%s: %s" % (FOLDER_NOT_FILE, fn), file=stderr)
        else:
            print("%s: %s" % (FILE_NOT_FOUND, fn), file=stderr)
        exit(1)
    fn_name = fn.split('/')[-1].strip()
    if fn_name in data:
        print("%s: %s" % (DUP_FILE, fn_name), file=stderr)
    try:
        if fn.lower().endswith('.gz'):
            lines = [l.strip() for l in gopen(fn).read().decode().splitlines()]
        else:
            lines = [l.strip() for l in open(fn)]
        data[fn] = [int(l.split('\t')[2]) for l in lines]
        ref_IDs |= {l.split('\t')[0].strip() for l in lines}
    except:
        print("%s: %s" % (NOT_PILEUP, fn), file=stderr); exit(1)
if len(ref_IDs) != 1:
    print("%s: %s" % (MULTIPLE_REFS, ', '.join(sorted(ref_IDs)))); exit(1)
ref_ID = list(ref_IDs)[0]; fns = sorted(data.keys())

# concatenate
print('File Name\tNum. Positions between %d and %d >= %d\tGO vs NOGO (GO means >= %s*%d=%s)' % (START, END, THRESH, str(PROP).rstrip('0').rstrip('.'), END-START+1, GO_NOGO_CUTOFF))
for fn in fns:
    above = sum(1 for i,cov in enumerate(data[fn]) if i >= START and i <= END and cov >= THRESH)
    go_nogo = {True:'GO',False:'NOGO'}[above >= GO_NOGO_CUTOFF]
    print('%s\t%d\t%s' % (fn,above,go_nogo))
