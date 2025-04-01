#!/usr/bin/env -S uv run --script
#/// script
# dependencies = ["deid"]
#///
# https://pydicom.github.io/deid/getting-started/dicom-pixels/

from deid.dicom.pixels import DicomCleaner
client=DicomCleaner(deid='deid-py.cfg')
client.detect('gray.dcm')
client.clean()
# NB. always appends cleaned- to output name: cleaned-gray.dcm
client.save_dicom(output_folder="scrubbed/")
