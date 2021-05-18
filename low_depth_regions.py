#! /usr/bin/env python3
'''
Given a samtools depth file, output all regions below the threshold
'''

# imports
import argparse

# main content
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Depth File (samtools depth format)")
    parser.add_argument('-m', '--min_depth', required=False, type=float, default=10, help="Minimum Depth (otherwise N)")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File (FASTA format)")
    args = parser.parse_args()
    if args.input == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output, 'w')

    # create mask regions
    mask = False
    for line in infile:
        chrom, pos, depth = line.strip().split('\t')
        chrom = chrom.strip(); pos = int(pos); depth = int(depth)
        if depth < args.min_depth:
            if not mask: # starting a mask region
                mask = True; outfile.write('%s\t%d\t' % (chrom,pos))
        else:
            if mask: # ending a mask region
                mask = False; outfile.write('%d\n' % (pos-1))
    if mask: # close trailing mask region
        mask = False; outfile.write('%d\n' % pos)
    outfile.close()
