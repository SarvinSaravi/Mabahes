import os
from skimage import io, color
import matplotlib.pyplot as plt
import numpy as np

from skimage import data, img_as_float
from skimage import exposure

filename_list = os.listdir('pictures')
list_of_images = []

for item in filename_list:
    img = io.imread('pictures\\' + item)
    list_of_images.append(img)

name = 1

# for img in list_of_images:

