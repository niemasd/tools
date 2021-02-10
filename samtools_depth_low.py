#! /usr/bin/env python3
'''
Niema Moshiri 2021

List all sites that have lower mapping coverage than a user-specified threshold within a user-specified window (1-based indexing)
'''
from gzip import open as gopen
from os.path import isdir,isfile
from sys import argv,stderr

# messages and constants
USAGE = "USAGE: %s <start_pos> <end_pos> <cov_thresh> <file1.depth.txt> [file2.depth.txt] [file3.depth.txt] ..." % argv[0]
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_PILEUP = "ERROR: File is not a samtools pileup output"
DUP_FILE = "ERROR: Duplicate file in arguments"
MULTIPLE_REFS = "ERROR: Multiple reference IDs were found (needs to be exactly 1)"
INVALID_INT = "ERROR: Invalid integer"

# check for validity
if len(argv) < 5:
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

# load data
data = dict(); ref_IDs = set()
for fn in argv[4:]:
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
print('File Name\tNumber of Positions Below %d\tPositions Below %d (CSV)' % (THRESH,THRESH))
for fn in fns:
    below = [str(i+1) for i,cov in enumerate(data[fn]) if i >= START and i <= END and cov < THRESH]
    print('%s\t%d\t%s' % (fn, len(below), ','.join(below)))
exit()
for i in range(max_len):
    print('\t'.join([ref_ID,str(i+1)] + [str(data[fn][i]) for fn in fns]))
