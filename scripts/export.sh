#!/usr/bin/env bash

OUTDIR=$1

do_export() {
    filename="$1$2_$3_$4.csv"
    echo "writing... $filename"
  
    echo "--codescheme $5 $2 $4_$3 > $OUTDIR/$filename" 
    python manage.py export --codescheme $5 $2 $2_$3 > $OUTDIR/$filename
}

if [$# -ne 1]
then
    echo "usage: `basename $0` <outdir>"
    exit 1
fi



for dataset in 1 2
do
    do_export mt_ andu $dataset and AND
    do_export mt_ andu $dataset u Uncertainty
    do_export mt_ and $dataset and AND
    do_export mt_ u $dataset u Uncertainty 
done


