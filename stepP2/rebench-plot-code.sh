#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Create folder: experiments"
mkdir experiments
FILES=(
  "$DIR/diagram.py"
  "$DIR/download.py"
  "$DIR/process-benchmark.py"
  "$DIR/latex.py"
)

for f in "${FILES[@]}"; do
  echo "Copy $f to experiments"
  cp "$f" experiments/
done
