#!/usr/bin/env python
# imports
from __future__ import print_function
PYTHON3 = True
try: # Python 3
    from urllib.request import urlopen
except: # Python 2
    PYTHON3 = False
    from urllib2 import urlopen
    input = raw_input
from os.path import isfile
from sys import argv,stdout

# check user args
if len(argv) != 3:
    print("USAGE: %s <m3u8_file> <out_file>" % argv[0]); exit(1)
if isfile(argv[2]):
    print("File exists: %s" % argv[2])
    overwrite = 'd'
    while len(overwrite) == 0 or (overwrite[0].lower() != 'y' and overwrite[0].lower() != 'n'):
        overwrite = input("Overwrite? (y,n) ")
    if overwrite[0].lower() == 'n':
        exit(1)

# read m3u8 and prepare for download
if PYTHON3:
    lines = [l.strip() for l in urlopen(argv[1]).read().decode().strip().splitlines()]
else:
    lines = [l.strip() for l in urlopen(argv[1]).read().strip().splitlines()]
out = open(argv[2],'wb')
TOTAL = sum(l.startswith('#EXTINF:') for l in lines); COUNT = 1
print("Downloading video file with %d parts to file: %s" % (TOTAL,argv[2]))

# download m3u8 stream
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF:'):
        print("Downloading part %d of %d..." % (COUNT,TOTAL), end='\r'); stdout.flush(); COUNT += 1
        if lines[i+1].lower().startswith('http'):
            url = lines[i+1]
        else:
            url = '/'.join(argv[1].split('/')[:-1]) + '/' + lines[i+1]
        out.write(urlopen(url).read())
out.close()
print("Download successfully completed")
