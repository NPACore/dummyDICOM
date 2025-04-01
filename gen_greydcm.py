#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pydicom", "deid", "deid-data"]
# ///

import numpy as np
from deid.data import get_dataset
from deid.dicom import get_files
from pydicom import dcmread, encaps
from pydicom.dataset import FileDataset  # type


def read_example() -> FileDataset:
    """Read an example dicom fom deid-data"""
    dataset = get_dataset("humans")
    example = list(get_files(dataset))[0]
    dcm = dcmread(example)
    return dcm


def make_gray(dcm) -> FileDataset:
    """Change all values to middle color: gray.
    Ideally this will make cropping/pixel censoring very obvious"""
    gray = 256 // 2 * np.ones(dcm.pixel_array.shape, dtype=dcm.pixel_array.dtype)
    dcm.PhotometricInterpretation = "YBR_FULL" # here b/c med2image complains
    # ValueError: The number of bytes of pixel data is a third larger than expected (697680 vs 465120 bytes) which indicates the set (0028,0004) 'Photometric Interpretation' value of 'YBR_FULL_422' is incorrect and may need to be changed to either 'RGB' or 'YBR_FULL'
    # BUT now black censor bar is green in output image? not a problem for testing
    dcm.set_pixel_data(gray,
                       dcm.PhotometricInterpretation,
                       dcm.BitsStored)
    return dcm


if __name__ == "__main__":
    output_name = "gray.dcm"
    dcm = read_example()
    graydcm = make_gray(dcm)
    graydcm.save_as(output_name)
