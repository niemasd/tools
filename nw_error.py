#!/usr/bin/env python3
'''
Compute various tree distance metrics on two given Newick-format trees.
* URF = Unweighted Robinson-Foulds
* WRF = Weighted Robinson-Foulds
'''
from dendropy.calculate.treecompare import unweighted_robinson_foulds_distance,weighted_robinson_foulds_distance
from dendropy import TaxonNamespace,Tree
from gzip import open as gopen
from os.path import isfile
METRICS = {'URF':unweighted_robinson_foulds_distance, 'WRF':weighted_robinson_foulds_distance}
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t1', '--tree1', required=True, type=str, help="Tree 1")
    parser.add_argument('-t2', '--tree2', required=True, type=str, help="Tree 2")
    parser.add_argument('-m', '--metric', required=True, type=str, help="Distance Metric (%s)" % ', '.join(sorted(METRICS.keys())))
    parser.add_argument('-n', '--normalize', action='store_true', help="Normalize")
    args = parser.parse_args()
    assert args.metric in METRICS, "Invalid distance metric: %s" % args.metric
    assert isfile(args.tree1), "Invalid file: %s" % args.tree1
    assert isfile(args.tree2), "Invalid file: %s" % args.tree2
    if args.tree1.lower().endswith('.gz'):
        t1_str = gopen(args.tree1).read().decode().strip()
    else:
        t1_str = open(args.tree1).read().strip()
    if args.tree2.lower().endswith('.gz'):
        t2_str = gopen(args.tree2).read().decode().strip()
    else:
        t2_str = open(args.tree2).read().strip()
    tns = TaxonNamespace()
    t1 = Tree.get(data=t1_str, schema='newick', taxon_namespace=tns)
    t2 = Tree.get(data=t2_str, schema='newick', taxon_namespace=tns)
    t1.encode_bipartitions()
    t2.encode_bipartitions()
    d = METRICS[args.metric](t1,t2)
    if args.normalize:
        if args.metric == 'URF':
            d /= 2*len(tns)-3
        else:
            raise ValueError("Cannot normalize metric: %s" % args.metric)
    print(d)
