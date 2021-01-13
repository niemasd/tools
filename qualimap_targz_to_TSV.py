#! /usr/bin/env python3
'''
Niema Moshiri 2021

Create a TSV file from Qualimap file(s) that has all of the summary stats
'''
from os.path import isdir,isfile
from sys import argv,stderr
from tarfile import open as topen

# messages
USAGE = "USAGE: %s <file1.stats.tar.gz> [file2.stats.tar.gz] [file3.stats.tar.gz] ..." % argv[0]
QUALIMAP_REPORT_HTML = 'qualimapReport.html'
FOLDER_NOT_FILE = "ERROR: Argument is a folder, not a file"
FILE_NOT_FOUND = "ERROR: File not found"
NOT_TAR_GZ = "ERROR: File is not tar.gz"
HTML_NOT_FOUND = "ERROR: Qualimap report HTML file (%s) not found" % QUALIMAP_REPORT_HTML

# check for validity
if len(argv) == 1 or argv[1].lower() in {'-h', '--help', '-help'}:
    print(USAGE, file=stderr); exit(1)
for fn in argv[1:]:
    if not isfile(fn):
        if isdir(fn):
            print("%s: %s" % (FOLDER_NOT_FILE, fn), file=stderr)
        else:
            print("%s: %s" % (FILE_NOT_FOUND, fn), file=stderr)
        exit(1)
    if not fn.lower().endswith('.tar.gz'):
        print("%s: %s" % (NOT_TAR_GZ, fn), file=stderr); exit(1)

# load data to dict
stats = dict(); header_order = list(); item_order = dict()
for fn_num,full_fn in enumerate(argv[1:]):
    # load tar.gz and check for validity
    tar = topen(full_fn, 'r:gz'); fn = full_fn.split('/')[-1]
    html_fn = None
    for tar_fn in tar.getnames():
        if tar_fn.split('/')[-1].lower() == QUALIMAP_REPORT_HTML.lower():
            html_fn = tar_fn; break
    if html_fn is None:
        print("%s: %s" % (HTML_NOT_FOUND, fn), file=stderr); exit(1)

    # prep for parsing this HTML file
    html_lines = [l.strip() for l in tar.extractfile(html_fn).read().decode().strip().splitlines()]
    stats[fn] = dict(); i = -1

    # load data from this HTML file
    while i < len(html_lines)-1:
        # move to next line of HTML (skip if not beginning of table)
        i += 1
        if not html_lines[i].startswith('<table class="summary'):
            continue

        # now, I'm at the start of a table: <table class="summary hovertable">
        header = html_lines[i-1].split('>')[1].split('<')[0].strip() # table header is on previous line: <h3>HEADER NAME</h3>
        if fn_num == 0:                                              # keep track of header order for output
            header_order.append(header); item_order[header] = list()
        stats[fn][header] = dict()                                   # get ready to load data from this table
        i += 1                                                       # move to row line: <tr ...>

        # handle "QualiMap command line" table in a special manner (it's the only one where a row has 1 column)
        if header.lower().endswith('command line'):
            if fn_num == 0:
                item_order[header] = ['']                            # don't append anything to "QualiMap command line" in output
            stats[fn][header][''] = html_lines[i+1].split('>')[1].split('<')[0].strip()
            i += 4
            continue

        # iterate over rows of this table
        while html_lines[i].startswith('<tr '):
            item_key,item_value = [html_lines[x].split('>')[1].split('<')[0].strip().rstrip(':').strip() for x in range(i+1,i+3)]
            if fn_num == 0:
                item_order[header].append(item_key)
            stats[fn][header][item_key] = item_value
            i += 4 # move to next row

    # output to TSV
    if fn_num == 0:
        print('\t'.join(["Qualimap Stats Filename"] + ['%s: %s' % (header,s) if s != '' else header for header in header_order for s in item_order[header]]))
    print('\t'.join([fn] + [stats[fn][header][s] for header in header_order for s in item_order[header]]))
