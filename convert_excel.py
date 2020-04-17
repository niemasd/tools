#! /usr/bin/env python3
'''
Convert an Excel spreadsheet to CSV/TSV/etc.
'''
from gzip import open as gopen
from xlrd import open_workbook
from sys import stdin,stdout

# human-readable delimiters
WORD_TO_SYMBOL = {
    'comma':    ',',
    'newline': '\n',
    'space':    ' ',
    'tab':     '\t',
}

# parse args
import argparse
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File Stream")
parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File Stream")
parser.add_argument('-d', '--delimiter', required=False, type=str, default='tab', help="Column Delimiter (enter symbol or one of: %s)" % ', '.join(sorted(WORD_TO_SYMBOL.keys())))
args = parser.parse_args()
if args.delimiter.lower() in WORD_TO_SYMBOL:
    args.delimiter = WORD_TO_SYMBOL[args.delimiter.lower()]
if args.input == 'stdin':
    data = stdin.read()
elif args.input.lower().endswith('.gz'):
    data = gopen(args.input).read()
else:
    data = open(args.input, 'rb').read()
if args.output == 'stdout':
    out = stdout
elif args.output.lower().endswith('.gz'):
    out = gopen(args.output, 'w')
else:
    out = open(args.output, 'w')

# convert spreadsheet
sheet = open_workbook(file_contents=data).sheet_by_index(0)
for rowx in range(sheet.nrows):
    out.write(args.delimiter.join(sheet.row_values(rowx))); out.write('\n')
