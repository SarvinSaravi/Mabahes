import os
from skimage import io, color
import matplotlib.pyplot as plt
from skimage.transform import rescale

filename_list = os.listdir('pictures')
list_of_images = []

for item in filename_list:
    img = io.imread('pictures\\' + item)
    list_of_images.append(img)

for pic in list_of_images:
    img1 = pic

    img1 = color.rgb2gray(img1)
    image_rescaled = rescale(img1, 0.7, anti_aliasing=False)

    plt.imshow(img1)
    plt.show()

    plt.imshow(image_rescaled)
    plt.show()

