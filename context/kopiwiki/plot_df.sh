#!/usr/bin/env bash
#
# Script to extract sparse term-article matrix for Wikipedia

# Download KOPI plain text from http://kopiwiki.dsd.sztaki.hu/
: ${KOPI_ROOT?"Set KOPI_ROOT, e.g., ~/data/kopiwiki"}

# Set KOPI variables
KOPI_DATE=20131203
KOPI_LANG=en

# Aggregate term-article frequencies
TERM_ARTS=kopi-wiki.contexts
python plot_df.py \
    $KOPI_ROOT \
    $KOPI_DATE \
    $KOPI_LANG


