#!/bin/sh

if [ "$MORBIDMETERHOME" = "" ]
then
    MORBIDMETERHOME=$(dirname $(readlink -f "$0"))
fi

if [ "$MORBIDMETERBIN" = "" ]
then
    MORBIDMETERBIN=$MORBIDMETERHOME
fi

export MORBIDMETERHOME
export MORBIDMETERBIN

export PYTHONBIN=/usr/bin/python

cd $MORBIDMETERHOME

"$PYTHONBIN" mm.py "$@"
