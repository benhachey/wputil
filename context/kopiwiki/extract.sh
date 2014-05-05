#!/usr/bin/env bash
#
# Script to extract sparse term-article matrix for Wikipedia

# Download KOPI plain text from http://kopiwiki.dsd.sztaki.hu/
: ${KOPI_ROOT?"Set KOPI_ROOT, e.g., ~/data/kopiwiki"}

# Set KOPI variables
KOPI_DATE=20131203
KOPI_LANG=en
MAX_DF=0.5

# Aggregate term-article frequencies
OUT=kopiwiki.contexts.txt
LOG=kopiwiki.contexts.log
python extract.py \
    $KOPI_ROOT \
    $KOPI_DATE \
    $KOPI_LANG \
    --max_df=$MAX_DF \
    > $OUT \
		2> $LOG
#gzip $OUT


