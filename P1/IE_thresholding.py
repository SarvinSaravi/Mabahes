import gc
import matplotlib.pyplot as plt
from skimage import io, color
from skimage.filters import threshold_otsu


def main(img):
    image = img
    thresh = threshold_otsu(image)
    binary = image > thresh

    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.5))
    ax = axes.ravel()
    ax[0] = plt.subplot(1, 3, 1)
    ax[1] = plt.subplot(1, 3, 2)
    ax[2] = plt.subplot(1, 3, 3, sharex=ax[0], sharey=ax[0])

    ax[0].imshow(image, cmap=plt.cm.gray)
    ax[0].set_title('Original')
    ax[0].axis('off')

    ax[1].hist(image.ravel(), bins=256)
    ax[1].set_title('Histogram')
    ax[1].axvline(thresh, color='r')

    ax[2].imshow(binary, cmap=plt.cm.gray)
    ax[2].set_title('Thresholded')
    ax[2].axis('off')

    fig.tight_layout()

    return plt, binary, thresh


def save(plot, name):
    plot.savefig(r'thresholding/' + str(name) + '.png')


if __name__ == '__main__':
    num = 10
    tmp_img = io.imread(r'pictures/' + str(num) + '.png')
    tmp_img = color.rgb2gray(tmp_img)
    p, img_binary, img_thresh = main(tmp_img)
    # save(p, num)
    p.show()
