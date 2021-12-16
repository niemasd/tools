#! /usr/bin/env python3
'''
Niema Moshiri 2021

Convert time from `time` command to seconds
'''
import argparse
from sys import stdin

# parse arguments
def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=argparse.FileType('r'), default=stdin, help="Input GNU Time Measurements")
    args = parser.parse_args()
    return args.input

# main code execution
for l in parseArgs():
    if len(l.strip()) == 0:
        continue
    end = l.split()[-1]
    if "Elapsed (wall clock) time (h:mm:ss or m:ss):" in l:
        parts = end.split(':')
        if len(parts) == 3: # h:mm:ss
            t = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
        elif len(parts) == 2: # m:ss
            t = float(parts[0])*60 + float(parts[1])
        else:
            assert False, "Invalid time: %s" % ':'.join(parts)
        print("Elapsed (wall clock) time (seconds): %s" % t)
    elif 'm' in end: # `time` (0m0.000s)
        try:
            c1,c2 = [v.strip() for v in l.strip().split()]
            m,s = [float(v) for v in c2.rstrip('s').split('m')]
            print("%s\t%f" % (c1, 60*m + s))
        except:
            pass
