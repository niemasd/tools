#!/usr/bin/env bash
# Recursively convert all HTML files in this folder (and sub-folders) to PDF
ARGS=''
if [ "$#" -ne 0 ] ; then
    if [ "$1" == "-l" ] ; then
        ARGS="$ARGS -O landscape"
    fi
fi


for f in $(find . -name *.html) ; do wkhtmltopdf $ARGS $f $(echo $f | rev | cut -d'.' -f2- | rev).pdf ; done
