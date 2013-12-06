#!/usr/bin/env bash
#
# Script to extract aliases from Google/UMass wiki-link data

WIKILINK=/data/wiki-link/google

ALIASES=wiki-link-google.aliases
PRIORS=wiki-link-google.priors
python extract.py \
    $WIKILINK \
    $ALIASES \
    $PRIORS
gzip $ALIASES
gzip $PRIORS

AFOF=$ALIASES.fof.csv
gunzip -c $ALIASES.gz \
    | cut -f3 \
    | uniq -c \
    | sed 's/^[^0-9]*//' \
    | awk 'BEGIN{FS=" "; OFS=","} {print $2,$1}' \
    > $AFOF

PFOF=$PRIORS.fof.csv
gunzip -c $PRIORS.gz \
    | cut -f2 \
    | uniq -c \
    | sed 's/^[^0-9]*//' \
    | awk 'BEGIN{FS=" "; OFS=","} {print $2,$1}' \
    > $PFOF

AGT1=$ALIASES.gt1
gunzip -c $ALIASES.gz \
    | awk 'BEGIN{FS="\t"} {if ($3 > 1) print}' \
    > $AGT1
gzip $AGT1

PGT1=$PRIORS.gt1
gunzip -c $PRIORS.gz \
    | awk 'BEGIN{FS="\t"} {if ($2 > 1) print}' \
    > $PGT1
gzip $PGT1
