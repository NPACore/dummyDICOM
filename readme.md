# Dummy DICOM

Creates a "dummy" dicom with fake PHI pixel burn in and then demonstrate removing it.

## Intention

[`clean.py`](clean.py) demonstrates pixel censoring by modifying the image to include a solid rectangle over sensitive burnt in data using the python package [deid](https://pydicom.github.io/deid/). When and how censoring is preformed is configured by [`deid-py.cfg`](deid-py.cfg).

### Config
Within [`deid-py.cfg`](deid-py.cfg), `contains` matches a dicom header (here any file assuming UID always includes a `.` character). and `coordinates` specifies a rectangle to censor ( `0,0` is the top left corner). For more see [deid's dicom pixels documentation](https://pydicom.github.io/deid/getting-started/dicom-pixels/)
```
contains SOPInstanceUID .
  coordinates 0,0,512,110
```

## Flywheel
[`deid-py.cfg`](deid-py.cfg) is manually translated to [`deid.yaml`](deid.yaml) for use with [deid-export](https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export/). As of 20250402, this is either an incomplete translation or otherwise not interpreted correctly by the flywheel gear -- no pixel censoring is preformed.

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

## 
```
git clone https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export
```
