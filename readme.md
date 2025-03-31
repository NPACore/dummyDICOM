# Dummy DICOM

Creates a "dummy" dicom with fake PHI pixel burn in for testing

## Reproduce

See [`Makefile`](Makefile).

  * Use `uv sync` to create `.venv/`. (Created with `uv init`)
  * `uv run fake.py` creates `fake_phi.dcm`

