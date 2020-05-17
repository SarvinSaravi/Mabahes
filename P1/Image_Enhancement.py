import sys

sys.path.insert(1, "IE_scaling")
import IE_scaling as scaling

sys.path.insert(1, "IE_contrast")
import IE_contrast as contrast

sys.path.insert(1, "IE_contrast2")
import IE_contrast2 as contrast2

sys.path.insert(1, "IE_denoising")
import IE_denoising as denoising

sys.path.insert(1, "IE_thresholding")
import IE_thresholding as thresholding

sys.path.insert(1, "IE_thresholding2")
import IE_thresholding2 as thresholding2

from skimage import color, io, img_as_float
import matplotlib.pyplot as plt


def main(num):
    initial_img = io.imread(r'pictures/' + str(num) + '.png')

    p, img_rescale = scaling.main(initial_img, 0.7)
    p.show()

    # process on image
    # img_float = img_as_float(img_rescale)
    # img_gray = color.rgb2gray(img_float)
    # print(img_rescale.shape)
    img_cropped = img_rescale[1000:1500, 500:1000]
    p, dn, dn2, dn_f, dn_f2, nsy = denoising.main(img_cropped, 0.01)
    p.show()

    p, gamma, logarithmic = contrast.main(dn)
    p.show()

    p, contrast_stretching, equalization, adaptive_equalization = contrast2.main(dn)
    p.show()

    p, img_binary, img_thresh = thresholding.main(logarithmic)
    p.show()

    p, b_global, b_niblack, b_sauvola = thresholding2.main(logarithmic, 7)
    p.show()


if __name__ == '__main__':
    No = 1
    main(No)
