#! /usr/bin/env python3
'''
Niema Moshiri 2017

Merge multiple FASTQ files (handle fixing duplicate IDs)
'''
from sys import argv
for f in argv[1:]:
    name = '.'.join(f.split('/')[-1].split('.')[:-1])
    i = 0
    for line in open(f):
        if i % 4 == 0: # header line
            print("@%s_%d" % (name,i/4))
        else:
            print(line.strip())
        i += 1
