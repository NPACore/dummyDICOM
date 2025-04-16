.PHONY: all

all: nii/fake_phi.nii.gz nii/cleaned-gray.nii.gz scrubbed/cleaned-gray.jpg scrubbed/fake_phi.jpg

.flywheel-upload: deid.yaml
	fw upload deid.yaml  "fw://flywheel/test/"
	date > $@

.launched: .flywheel-upload
	# from copy-gear, launch job on flywheel
	uv run ./deid-export_launchtest.py

fake_phi.dcm: fake.py
	uv run fake.py

gray.dcm: ./gen_greydcm.py
	./gen_greydcm.py

scrubbed/cleaned-gray.dcm: gray.dcm
	./clean.py

scrubbed/fake_phi.dcm: gray.dcm
	./01_test_deid.bash

# for nii/fake_phi.nii.gz and nii/cleaned-gray.nii.gz
nii/%.nii.gz: scrubbed/%.dcm
	mkdir -p nii
	dcm2niix -o nii/ -f $(notdir $(@:.nii.gz=)) -z y -s y $<

scrubbed/%.jpg: scrubbed/%.dcm
	# uv tool install git+https://github.com/WillForan/med2image
	# # and remove cgi from pfmisc?
	# # $HOME/.local/share/uv/tools/med2image/lib/python3.13/site-packages/pfmisc/C_stringCore.py
	# # https://github.com/FNNDSC/pfmisc/issues/3
	med2image  --convertOnlySingleDICOM -s m -i $< -o $@
