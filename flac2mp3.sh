#!/usr/bin/env bash
# Convert a FLAC to a 320 kbps MP3
if [ "$#" -ne 2 ] ; then
    echo "USAGE: $0 <in_flac> <out_mp3>"; exit 1
fi
ffmpeg -i "$1" -ab 320k -map_metadata 0 -id3v2_version 3 "$2"
