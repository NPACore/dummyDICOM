# Dummy DICOM

Creates a "dummy" dicom with fake PHI pixel burn in for testing

## Reproduce

See [`Makefile`](Makefile).

  * Use `uv sync` to create `.venv/`. (Created with `uv init`)
  * `uv run fake.py` creates `fake_phi.dcm`

## TODO:

`make -B nii/fake_phi.nii.gz` shows fake dicom problems

```
DICOM appears corrupt: first group:element should be 0x0002:0x0000 '/home/foranw/src/work/dummyDICOM/fake_phi.dcm'
Warning: Instance number (0020,0013) not found: /home/foranw/src/work/dummyDICOM/fake_phi.dcm
Warning: PatientOrient (0018,5100) not specified (issue 642).
Warning: Unable to determine manufacturer (0008,0070), so conversion is not tuned for vendor.
```

maybe contributing to deid failing?

```
./01_test_deid.bash

WARNING dicom: not recognized to be in valid format, skipping.
```

## Notes

quick image from dicom
```
uv tool install git+https://github.com/WillForan/med2image

med2image  --convertOnlySingleDICOM -s m \
   -o scrubbed/fake_phi.jpg \
   -i scrubbed/fake_phi.dcm
```
