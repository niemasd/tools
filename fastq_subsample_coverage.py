#! /usr/bin/env python3
'''
Niema Moshiri 2022

Subsample FASTQ(s) to have minimum coverage based on (trimmed) BAM.
'''
from gzip import open as gopen
from io import BufferedReader, TextIOWrapper
from os.path import isfile
import argparse
import pysam

# main content
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--fastq', required=True, type=str, nargs='*', help="Input FASTQ(s)")
    parser.add_argument('-b', '--bam', required=True, type=str, nargs='*', help="Input BAM (or SAM)")
    parser.add_argument('-m', '--min_cov', required=True, type=int, help="Minimum Coverage")
    parser.add_argument('-o', '--output', required=True, type=str, nargs='*', help="Output FASTQ(s) (same length as --fastq)")
    parser.add_argument('-mq', '--min_map_qual', required=False, type=int, default=0, help="Minimum Mapping Quality")
    parser.add_argument('-bq', '--min_base_qual', required=False, type=int, default=20, help="Minimum Base Quality")
    args = parser.parse_args()
    assert args.min_cov > 0, "Minimum coverage must be positive"
    assert args.min_map_qual >= 0, "Minimum mapping quality must be non-negative"
    assert args.min_base_qual >= 0, "Minimum base quality must be non-negative"
    assert len(args.output) == len(args.fastq), "Length of --output must be the same as length of --fastq"
    for i in range(len(args.fastq)):
        assert isfile(args.fastq[i]), "Input FASTQ file not found: %s" % args.fastq[i]
        assert not isfile(args.output[i]), "Output FASTQ file exists: %s" % args.output[i]
    for b in args.bam:
        assert isfile(b), "Input BAM/SAM file not found: %s" % b

    # set things up
    cov = list() # cov[i] = coverage at position i
    keep = set() # names of reads to keep

    # compute minimum reads to have minimum coverage
    for b in args.bam:
        # open BAM/SAM file
        tmp = pysam.set_verbosity(0)
        if b.lower().endswith('.bam'):
            aln = pysam.AlignmentFile(b, 'rb')
        else:
            aln = pysam.AlignmentFile(b, 'r')
        pysam.set_verbosity(tmp)

        # iterate over reads in BAM/SAM file
        for read_num, read in enumerate(aln.fetch(until_eof=True)):
            # skip this read if unmapped or mapping quality is too low
            if read.is_unmapped or read.mapping_quality < args.min_map_qual:
                continue

            # check if we will want to include this read
            include = False; quals = read.query_qualities; pairs = list(read.get_aligned_pairs(matches_only=True, with_seq=False))
            while len(cov) <= max(ref_pos for read_pos, ref_pos in pairs):
                cov.append(0)
            for read_pos, ref_pos in pairs:
                if quals[read_pos] >= args.min_base_qual and (len(cov) <= ref_pos or cov[ref_pos] < args.min_cov):
                    include = True; break
            if not include:
                continue

            # if including read, add to `keep` and increment coverage
            keep.add(read.query_name)
            for read_pos, ref_pos in pairs:
                cov[ref_pos] += 1
    print(cov); exit()

    # load FASTQs and output just the reads in `keep`
    for fq_num in range(len(args.fastq)):
        # open input and output FASTQ files
        if args.fastq[fq_num].lower().endswith('.gz'):
            in_fq = TextIOWrapper(BufferedReader(gopen(args.fastq[fq_num])))
        else:
            in_fq = TextIOWrapper(BufferedReader(open(args.fastq[fq_num])))
        if args.output[fq_num].lower().endswith('.gz'):
            out_fq = gopen(args.output[fq_num], 'wb'); out_gz = True
        else:
            out_fq = open(args.output[fq_num], 'w'); out_gz = False
        
        # parse FASTQ and output the reads
        write = False
        for i, l in enumerate(in_fq):
            if (i % 4) == 0 and l[1:].split()[0].strip() in keep:
                write = True
            if write:
                if out_gz:
                    out_fq.write(l.encode())
                else:
                    out_fq.write(l)
                if (i % 4) == 3:
                    write = False
        in_fq.close(); out_fq.close()
