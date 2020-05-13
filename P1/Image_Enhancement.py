import os
from skimage import io
import matplotlib.pyplot as plt
from skimage.transform import rescale, resize, downscale_local_mean

filename_list = os.listdir('pictures')
print(filename_list)
list_of_images = []

for item in filename_list:
    img = io.imread('pictures\\' + item)
    list_of_images.append(img)

print(len(list_of_images))

img1 = list_of_images[0]

print(type(img1))
print(img1.shape)

print('****************************')

image_rescaled = rescale(img1, 0.7, anti_aliasing=False)

# print(image_rescaled)


