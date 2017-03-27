#! /usr/bin/env python
'''
Niema Moshiri 2017

Merge multiple bib files into a single file: merged.bib
'''
import sys
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
from os.path import isfile

if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in {'h','-h','--h','help','-help','--help'}):
        print("USAGE: python printbib.py <file1.bib> <file2.bib> ...")
        exit(0)
    if len(sys.argv) == 2:
        print("ERROR: Only 1 file specified")
        print("USAGE: python printbib.py <file1.bib> <file2.bib> ...")
        exit(-1)
    if isfile('merged.bib'):
        print("ERROR: merged.bib file already exists!")
        exit(-1)
    try:
        entrylists = [(f,BibTexParser(open(f).read()).get_entry_list()) for f in sys.argv[1:]] # (file,entrylist) tuples
    except:
        print("ERROR: Failed to read bib files")
        exit(-1)
    for bibfile,entrylist in entrylists:
        print(str(len(entrylist)) + " entries in file " + bibfile)
    entries = {} # store all entry IDs I've seen so far (entries[ID] = file I read it from)
    outlist = []
    f = open('merged.bib','w')
    for bibfile,entrylist in entrylists:
        for entry in entrylist:
            if entry['ID'] in entries:
                print("DUPLICATE: " + entry['ID'] + ", using entry from " + entries[entry['ID']])
            else:
                outlist.append(entry)
                entries[entry['ID']] = bibfile
    db = BibDatabase()
    db.entries = outlist
    writer = BibTexWriter()
    f = open('merged.bib','w')
    f.write(writer.write(db).encode('utf8'))
    f.close()
    print(str(len(entries)) + " entries written to file merged.bib")
