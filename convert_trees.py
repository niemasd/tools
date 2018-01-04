#!/usr/bin/env python3
'''
Convert branch support values from 0-1 to 0-100 or vice-versa. Convert tree schema.
Also set all branches without support to a given default value if wanted.
'''
SCHEMA = {'newick','nexus','phyloxml','nexml'}
if __name__ == "__main__":
    # parse user arguments
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input Tree File")
    parser.add_argument('-is', '--in_schema', required=False, type=str, default='newick', help="Input Tree Schema")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output Tree File")
    parser.add_argument('-os', '--out_schema', required=False, type=str, default='newick', help="Output Tree Schema")
    parser.add_argument('-f', '--format', required=True, type=str, help="Format: (d)ecimal or (p)ercentage")
    parser.add_argument('-d', '--default', required=False, type=int, default=None, help="Default Support for Missing (percentage as int)")
    args = parser.parse_args()
    args.in_schema = args.in_schema.lower()
    assert args.in_schema in SCHEMA, "Input Schema must be one of the following: %s" % str(SCHEMA)
    args.out_schema = args.out_schema.lower()
    assert args.out_schema in SCHEMA, "Output Schema must be one of the following: %s" % str(SCHEMA)
    args.format = args.format.lower()[0]
    assert args.format in {'d','p'}, "Format must be either (d)ecimal (-f d) or (p)ercentage (-f p)"
    assert args.default is None or (args.default >= 0 and args.default <= 100), "Default support value must be an integer between 0 and 1"
    if args.format == 'd' and args.default is not None:
        args.default /= 100.
    if args.input == 'stdin':
        from sys import stdin; infile = stdin
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout; outfile = stdout
    else:
        outfile = open(args.output,'w')
    from Bio import Phylo
    trees = [tree for tree in Phylo.parse(infile,args.in_schema)]

    # convert/fix branch support values
    for tree in trees:
        tree.rooted = True
        decimal = True
        for node in tree.find_clades(order='preorder'):
            if node.confidence is not None and node.confidence > 1:
                decimal = False; break
        for node in tree.find_clades(order='preorder'):
            if not node.is_terminal():
                if node.confidence is None:
                    node.confidence = args.default
                elif args.format == 'p' and decimal:
                    node.confidence *= 100
                elif args.format == 'd' and not decimal:
                    node.confidence /= 100

    # output trees
    Phylo.write(trees,outfile,args.out_schema); outfile.close()
