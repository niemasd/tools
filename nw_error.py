#!/usr/bin/env python3
'''
Compute various tree distance metrics on two given Newick-format trees.
* URF = Unweighted Robinson-Foulds
* WRF = Weighted Robinson-Foulds
'''
from dendropy.calculate.treecompare import unweighted_robinson_foulds_distance,weighted_robinson_foulds_distance
from dendropy import TaxonNamespace,Tree
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
    tns = TaxonNamespace()
    t1 = Tree.get(path=args.tree1, schema='newick', taxon_namespace=tns)
    t2 = Tree.get(path=args.tree2, schema='newick', taxon_namespace=tns)
    t1.encode_bipartitions()
    t2.encode_bipartitions()
    d = METRICS[args.metric](t1,t2)
    if args.normalize:
        if args.metric == 'URF':
            d /= 2*len(tns)-3
        else:
            raise ValueError("Cannot normalize metric: %s" % args.metric)
    print(d)
