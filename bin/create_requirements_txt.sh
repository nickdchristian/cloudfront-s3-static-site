#!/bin/bash

for d in ../* ; do
  find "$d" -name "index.py" -type f -execdir pipreqs --force \;
  echo "$d"
done