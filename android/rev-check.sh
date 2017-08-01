#!/data/data/com.termux/files/usr/bin/env bash

EXTRACTS_PATH="/storage/emulated/0/Android/data/com.she.eReader/.hamibookEx/extracts/"

for D in $(ls $EXTRACTS_PATH); do
    NUMPDFS=$(ls -l $EXTRACTS_PATH/$D/*.pdf | wc -l)
    if [ $NUMPDFS -ne 2 ]; then
        ls -l $EXTRACTS_PATH/$D/*.pdf
    else
        SIZE=0
        ls -l $EXTRACTS_PATH/$D/*.pdf | awk '{ print $5 }' | while read -r PDFSZ
        do
            [ $SIZE -eq 0 ] && SIZE=$PDFSZ
            [ $SIZE -ne $PDFSZ ] && ls -l $EXTRACTS_PATH/$D/*.pdf
        done
    fi
done
