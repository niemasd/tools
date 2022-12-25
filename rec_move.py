#!/usr/bin/env python3
from glob import glob
from os import makedirs, remove, rename, rmdir
from os.path import abspath, expanduser, isdir, isfile
from sys import argv

# recursively move files
def rec_move(from_path, to_path, dryrun=False, reverse=False):
    if from_path.split('/')[-1].split('\\')[-1].lower() in {'desktop.ini'}:
        remove(from_path); return # skip desktop.ini files
    elif isdir(from_path):
        if isfile(to_path):
            raise ValueError('To path exists as file: "%s"' % to_path)
        elif not isdir(to_path):
            print('mkdir "%s"' % to_path)
            if not dryrun:
                makedirs(to_path)
        for fn in sorted(glob('%s/*' % from_path), reverse=reverse, key=lambda x: x.lower()):
            rec_move(fn, fn.replace(from_path, to_path), dryrun=dryrun)
        print('rmdir "%s"' % from_path)
        if not dryrun:
            rmdir(from_path)
    elif isfile(from_path):
        if isdir(to_path):
            raise ValueError('To path exists as dir: "%s"' % to_path)
        print('mv "%s" "%s"' % (from_path, to_path))
        if not dryrun:
            rename(from_path, to_path)
    else:
        raise ValueError('Path not found: "%s"' % from_path)

# main code
if __name__ == "__main__":
    if len(argv) < 3 or len(argv) > 4:
        print("USAGE: %s FROM_PATH TO_PATH [dryrun]" % argv[0]); exit(1)
    dryrun = False
    if len(argv) > 3:
        if argv[3].lower() in {'d', 'dry', 'dryrun'}:
            dryrun = True
        else:
            raise ValueError("INVALID ARGUMENT: %s" % argv[3])
    rec_move(abspath(expanduser(argv[1])), abspath(expanduser(argv[2])), dryrun=dryrun)