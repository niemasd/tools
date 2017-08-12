#! /usr/bin/env python3

# parse user arguments
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default="stdin", help="Input FASTQ file (default is standard input)")
parser.add_argument('--instrument', required=False, type=str, default='M00805', help="Instrument")
parser.add_argument('--runID', required=False, type=int, default=5, help="Run ID")
parser.add_argument('--flowcellID', required=False, type=str, default='000000000-A0VLL', help="Flow Cell ID")
parser.add_argument('--lane', required=False, type=int, default=1, help="Lane")
parser.add_argument('--tile', required=False, type=int, default=1101, help="Tile")
parser.add_argument('--readnum', required=True, type=int, help="Read Number (1 or 2)")
parser.add_argument('--samplenum', required=False, type=int, default=1, help="Sample Number")
args = parser.parse_args()

# create input filestream f
from sys import stdin
if args.input == 'stdin':
    f = stdin
elif args.input[-3:] in {'.gz','.GZ','.Gz','.gZ'}:
    import gzip
    f = gzip.open(args.input)
else:
    f = open(args.input)

# parse FASTQ and rename headers
x = 1
y = 1
for line in f:
    l = line.strip()
    if len(l) == 0:
        continue
    elif l[0] == '@': # header line
        print("@%s:%s:%s:%s:%s:%d:%d %s:N:0:%s" % (args.instrument,args.runID,args.flowcellID,args.lane,args.tile,x,y,args.readnum,args.samplenum))
        x += 1
    else:
        print(l)

# @Instrument:RunID:FlowCellID:Lane:Tile:X:Y[:UMI] ReadNum:FilterFlag:0:SampleNumber
