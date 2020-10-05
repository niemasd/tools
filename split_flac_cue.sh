#!/usr/bin/env bash
# Split a single flac + cue into multiple flac files
if [ "$#" -ne 2 ] ; then
    echo "USAGE: $0 <flac> <cue>"; exit 1
fi
shnsplit -f "$2" -t %n-%t -o flac "$1"
