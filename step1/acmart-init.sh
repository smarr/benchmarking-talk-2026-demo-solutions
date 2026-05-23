#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# ACMART=$DIR/acmart
ACMART="~/Projects/misc/acmart"

echo Copying ACM ART template to current directory
echo Copying collab.sty for collaborative macros
echo Copying empty paper.tex

cp $ACMART/acmart.cls $ACMART/ACM-Reference-Format.bst $ACMART/../collab.sty/collab.sty $ACMART/../collab.sty/.gitignore .
touch references.bib
cp $DIR/paper.tex paper.tex
