.PHONY: all

all: nii/fake_phi.nii.gz

fake_phi.dcm: fake.py
	uv run fake.py

nii/fake_phi.nii.gz: fake_phi.dcm
	mkdir -p nii
	dcm2niix -o nii/ -f fake_phi -z y $<
