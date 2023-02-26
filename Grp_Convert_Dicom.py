import numpy as np
import pydicom
from PIL import Image
import os
from datetime import datetime
import shutil

timestamp = datetime.now()

#Grabbing the files and creating new filenames
def get_names(path):
    names = []
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in ['.dcm']:
                names.append(filename)
    
    return names

#Converting/resizing DICOM images from file path
def convert_dcm_jpg(name):
    
    im = pydicom.dcmread('C:/Dicom/Images/'+name)

    im = im.pixel_array.astype(float)

    rescaled_image = (np.maximum(im,0)/im.max())*255 # float pixels
    final_image = np.uint8(rescaled_image) # integers pixels

    final_image = Image.fromarray(final_image)

    return final_image


#Calling the two functions and saving images as jpg files
names = get_names('C:/Dicom/Images/')

log_file = open('C:/Dicom/DCM_Convert_Log.txt', 'a')
for name in names:
    try:
        image = convert_dcm_jpg(name)
        image.save('C:/Dicom/jpg/'+name+'.jpg')
    except:
        log_file.write(f"{timestamp} - {name} - File did not convert\n\n")

log_file.close()

#Moving .dcm files to archive folder
source = 'C:/Dicom/Images/'
destination = 'C:/Dicom/Images_archive/'
files = os.listdir(source)
for file in files:
    if file.endswith(".dcm"):
        shutil.move(source + file, destination + file)
        log_file = open('C:/Dicom/DCM_Convert_Log.txt', 'a')
        log_file.write(f"{timestamp}: Moved {file} to archive folder\n")

log_file.close()