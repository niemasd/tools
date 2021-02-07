#! /usr/bin/env python3
'''
Niema Moshiri 2021

Concatenate samtools depth files
'''
from gzip import open as gopen
from os.path import isdir,isfile
from sys import argv,stderr

# messages and constants
USAGE = "USAGE: %s <file1.depth.txt> [file2.depth.txt] [file3.depth.txt] ..." % argv[0]
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_PILEUP = "ERROR: File is not a samtools pileup output"
DUP_FILE = "ERROR: Duplicate file in arguments"
MULTIPLE_REFS = "ERROR: Multiple reference IDs were found (needs to be exactly 1)"

# check for validity and load data
if len(argv) == 1 or argv[1].lower() in {'-h', '--help', '-help'}:
    print(USAGE, file=stderr); exit(1)
data = dict(); ref_IDs = set()
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
max_len = max(len(data[fn]) for fn in data)
print('\t'.join(['Reference', 'Position'] + fns))
for i in range(max_len):
    print('\t'.join([ref_ID,str(i+1)] + [str(data[fn][i]) for fn in fns]))
