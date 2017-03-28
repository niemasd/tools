#! /usr/bin/env python
'''
Niema Moshiri 2017

Merge multiple bib files into a single file: merged.bib
'''
import sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter

if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in {'h','-h','--h','help','-help','--help'}):
        sys.stderr.write("USAGE: python printbib.py <file1.bib> <file2.bib> ...\n")
        exit(0)
    if len(sys.argv) == 2:
        sys.stderr.write("ERROR: Only 1 file specified\n")
        sys.stderr.write("USAGE: python printbib.py <file1.bib> <file2.bib> ...\n")
        exit(-1)
    try:
        entrylists = [(f,BibTexParser(open(f).read()).get_entry_list()) for f in sys.argv[1:]] # (file,entrylist) tuples
    except:
        sys.stderr.write("ERROR: Failed to read bib files\n")
        exit(-1)
    for bibfile,entrylist in entrylists:
        sys.stderr.write(str(len(entrylist)) + " entries in file " + bibfile + '\n')
    entries = {} # store all entry IDs I've seen so far (entries[ID] = file I read it from)
    outlist = []
    f = open('merged.bib','w')
    for bibfile,entrylist in entrylists:
        for entry in entrylist:
            if entry['ID'] in entries:
                sys.stderr.write("DUPLICATE: " + entry['ID'] + ", using entry from " + entries[entry['ID']] + '\n')
            else:
                outlist.append(entry)
                entries[entry['ID']] = bibfile
    db = BibDatabase()
    db.entries = outlist
    writer = BibTexWriter()
    print(writer.write(db).encode('utf8'))
    sys.stderr.write(str(len(entries)) + " entries in output\n")
