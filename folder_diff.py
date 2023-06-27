#! /usr/bin/env python3
from glob import glob
from os.path import abspath, expanduser, getsize, isdir, isfile
from sys import argv
from time import time

# returns dict where keys are paths and values are sizes of all files nested within `path`
def get_all_files(path, verbose=True):
    out = dict(); to_explore = [abspath(expanduser(path)).rstrip('/')]
    if verbose:
        print("Loading files from: %s" % path); num_checked = 0; start_time = time()
    while len(to_explore) != 0:
        path = to_explore.pop()
        if isfile(path):
            out[path] = getsize(path)
        elif isdir(path):
            to_explore += [fn for fn in glob('%s/*' % path.rstrip('/'))]
        if verbose:
            num_checked += 1; print("Checked %d item(s)..." % num_checked, end='\r')
    if verbose:
        end_time = time(); print("Checked %d item(s) in %d seconds" % (num_checked, end_time-start_time))
    return out

if len(argv) != 3:
    print("USAGE: %s <folder1> <folder2>" % argv[0]); exit(1)
folder1 = abspath(expanduser(argv[1]))
folder2 = abspath(expanduser(argv[2]))
files1 = get_all_files(folder1)
files2 = get_all_files(folder2)
for path1, size1 in sorted(files1.items()):
    path2 = '%s/%s' % (folder2, folder1.join(path1.split(folder1)[1:]).lstrip('/'))
    size2 = 'MISSING'
    if path2 in files2:
        size2 = files2[path2]
    if size1 != size2:
        print('%s\t%s\t%s\t%s' % (path1, size1, path2, size2))
for path2, size2 in sorted(files2.items()):
    path1 = '%s/%s' % (folder1, folder2.join(path2.split(folder2)[1:]).lstrip('/'))
    if path1 not in files1:
        print("%s\tMISSING\t%s\t%s" % (path1, path2, size2))
