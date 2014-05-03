#!/usr/bin/env bash
#
# Script to extract sparse term-article matrix for Wikipedia

# Download KOPI plain text from http://kopiwiki.dsd.sztaki.hu/

# Set KOPI variables
KOPI_ROOT=/Users/benhachey/Desktop/kopiwiki
#KOPI_ROOT=/data/wikipedia/kopiwiki
KOPI_DATE=20131203
KOPI_LANG=en
MAX_DF=0.5
MIN_DF=5

# Aggregate term-article frequencies
TERM_ARTS=kopi-wiki.contexts
python extract.py \
    $KOPI_ROOT \
    $KOPI_DATE \
    $KOPI_LANG \
    --max_df=$MAX_DF \
    --min_df=$MIN_DF \
#    > $TERM_ARTS
#gzip $TERM_ARTS


