#!/usr/bin/env bash
tmp='DUMMYCONTENT'
for f in *; do
    tmp2=$(cat $f | sort)
    if [ "$tmp" == "$tmp2" ]; then
        rm $f
    else
        tmp=$tmp2
    fi
done
