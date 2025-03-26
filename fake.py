from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, SecondaryCaptureImageStorage, ExplicitVRLittleEndian
import datetime

# 1. Make an image with fake PHI burned in

img_size = (512, 512)  # Image size (width x height)
img = Image.new("L", img_size, color=0)  # New grayscale image with black background
draw = ImageDraw.Draw(img)  # Set up drawing context

# Fake PHI text to embed in the image
phi_text = [
    "FAKEMAN, JOHN",
    "COMPLETELYREALPERSON, JOHN",
    "111222333",
    "DOB: 12/34/5678"
]

# Load font (fallback to default if needed)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", size=20)
except IOError:
    font = ImageFont.load_default()

# Draw each line of PHI text on the image
for i, line in enumerate(phi_text):
    draw.text((10, 10 + i * 24), line, fill=255, font=font)  # White text

# Convert image to raw pixel bytes for DICOM
pixel_array = np.array(img, dtype=np.uint8)
pixel_bytes = pixel_array.tobytes()

# 2. Build the DICOM file

filename = "fake_phi.dcm"

# Set up DICOM file metadata
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
file_meta.MediaStorageSOPInstanceUID = generate_uid()
file_meta.ImplementationClassUID = generate_uid()
file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

# Create the DICOM dataset
ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

# Set basic DICOM fields
dt = datetime.datetime.now()
ds.PatientName = "FAKELAST^FAKEFIRST"
ds.PatientID = "FAKE123"
ds.StudyInstanceUID = generate_uid()
ds.SeriesInstanceUID = generate_uid()
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.Modality = "MR"
ds.SeriesDescription = "MR TEST"
ds.StudyDate = dt.strftime('%Y%m%d')
ds.StudyTime = dt.strftime('%H%M%S')

# Image data settings
ds.Rows, ds.Columns = pixel_array.shape
ds.BitsAllocated = 8
ds.BitsStored = 8
ds.HighBit = 7
ds.PixelRepresentation = 0
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.PixelData = pixel_bytes

# Save the final DICOM file
ds.save_as(filename)
print(f"Saved DICOM with burned-in PHI: {filename}")

