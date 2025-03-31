#!/usr/bin/env bash
# run/test 'deid' on generated dicom file
# 20250331WF - init

input=${1:-fake_phi.dcm} # default to output of fake.py
mkdir -p scrubbed/
uv run \
    deid --debug --overwrite --format dicom  --outfolder scrubbed/ \
      identifiers -a all --deid ./deid.yaml \
      --input  "$input"
