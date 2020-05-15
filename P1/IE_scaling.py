from skimage import color, io
import matplotlib.pyplot as plt
from skimage.transform import rescale


def main(image, ratio):
    img1 = color.rgb2gray(image)
    image_rescaled = rescale(img1, ratio, anti_aliasing=False)

    fig, axes = plt.subplots(nrows=1, ncols=2)

    ax = axes.ravel()

    ax[0].imshow(img1, cmap='gray')
    ax[0].set_title("Original image")

    ax[1].imshow(image_rescaled, cmap='gray')
    ax[1].set_title("Rescaled image (aliasing)")

    # plt.show()

    return plt, image_rescaled


def save(plot, name):
    plot.savefig(r'scaling2/' + str(name) + '.png')


if __name__ == '__main__':
    num = 10
    tmp_img = io.imread(r'pictures/' + str(num) + '.png')
    p, img_rescale = main(tmp_img, 0.7)
    save(p, num)
