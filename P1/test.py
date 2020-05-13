# plt.show()

# my_path = os.path.abspath(__file__)
# my_file = str(name) + '.png'
# plt.savefig(os.path.join(my_path, my_file))

# plt.imshow(image_rescaled)





import os
from skimage import io, color
import matplotlib.pyplot as plt
from skimage.transform import rescale

filename_list = os.listdir('pictures')
list_of_images = []

for item in filename_list:
    img = io.imread('pictures\\' + item)
    list_of_images.append(img)

name = 1

for pic in list_of_images:
    img1 = pic

    img1 = color.rgb2gray(img1)
    image_rescaled = rescale(img1, 0.7, anti_aliasing=False)

    fig, axes = plt.subplots(nrows=1, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(img1, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled, cmap='gray')
    ax[1].set_title("Rescaled image (aliasing)")

    plt.savefig(r'scaling2/' + str(name) + '.png')
    name = name + 1



#############################################

from skimage import exposure


img = list_of_images[0]
# Gamma
gamma_corrected = exposure.adjust_gamma(img, 2)
# Logarithmic
logarithmic_corrected = exposure.adjust_log(img, 1)


plt.imshow(img)
plt.show()

plt.imshow(gamma_corrected)
plt.show()

plt.imshow(logarithmic_corrected)
plt.show()

