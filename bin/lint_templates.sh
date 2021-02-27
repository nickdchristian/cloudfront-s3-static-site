#!/bin/bash

for d in ../* ; do
  find "$d" -name "*.template.yaml"  -exec cfn-lint {} \;
done
for d in ../* ; do
  find "$d" -name "*.template.yaml"  -exec cfn_nag_scan -i {} \;
done