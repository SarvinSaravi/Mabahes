import matplotlib.pyplot as plt
from skimage import io, img_as_float, color
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.util import random_noise
import gc
import numpy as np
from skimage.util.dtype import dtype_range
from skimage._shared.utils import warn, check_shape_equality

# import sys
# sys.path.insert(1, "IE_scaling")
# import IE_scaling as my_module

__all__ = ['mean_squared_error',
           'normalized_root_mse',
           'peak_signal_noise_ratio',
           ]


def _as_floats(image0, image1):
    float_type = np.result_type(image0.dtype, image1.dtype, np.float32)
    image0 = np.asarray(image0, dtype=float_type)
    image1 = np.asarray(image1, dtype=float_type)
    return image0, image1


def mean_squared_error(image0, image1):
    check_shape_equality(image0, image1)
    image0, image1 = _as_floats(image0, image1)
    return np.mean((image0 - image1) ** 2, dtype=np.float64)


def normalized_root_mse(image_true, image_test, *, normalization='euclidean'):
    check_shape_equality(image_true, image_test)
    image_true, image_test = _as_floats(image_true, image_test)

    # Ensure that both 'Euclidean' and 'euclidean' match
    normalization = normalization.lower()
    if normalization == 'euclidean':
        denom = np.sqrt(np.mean((image_true * image_true), dtype=np.float64))
    elif normalization == 'min-max':
        denom = image_true.max() - image_true.min()
    elif normalization == 'mean':
        denom = image_true.mean()
    else:
        raise ValueError("Unsupported norm_type")
    return np.sqrt(mean_squared_error(image_true, image_test)) / denom


def peak_signal_noise_ratio(image_true, image_test, *, data_range=None):
    check_shape_equality(image_true, image_test)

    if data_range is None:
        if image_true.dtype != image_test.dtype:
            warn("Inputs have mismatched dtype.  Setting data_range based on "
                 "im_true.", stacklevel=2)
        dmin, dmax = dtype_range[image_true.dtype.type]
        true_min, true_max = np.min(image_true), np.max(image_true)
        if true_max > dmax or true_min < dmin:
            raise ValueError(
                "im_true has intensity values outside the range expected for "
                "its data type.  Please manually specify the data_range")
        if true_min >= 0:
            # most common case (255 for uint8, 1 for float)
            data_range = dmax
        else:
            data_range = dmax - dmin

    image_true, image_test = _as_floats(image_true, image_test)

    err = mean_squared_error(image_true, image_test)
    return 10 * np.log10((data_range ** 2) / err)


def main(image, noise):
    my_picture = image

    sigma = noise
    noisy = random_noise(my_picture, var=sigma ** 2)

    # estimate the noise standard deviation from the noisy image
    sigma_est = np.mean(estimate_sigma(noisy, multichannel=True))
    print(f"estimated noise standard deviation = {sigma_est}")

    patch_kw = dict(patch_size=5,  # 5x5 patches
                    patch_distance=6,  # 13x13 search area
                    multichannel=True)

    # slow algorithm
    denoise = denoise_nl_means(noisy, h=1.15 * sigma_est, fast_mode=False,
                               **patch_kw)

    # slow algorithm, sigma provided
    denoise2 = denoise_nl_means(noisy, h=0.8 * sigma_est, sigma=sigma_est,
                                fast_mode=False, **patch_kw)

    # fast algorithm
    denoise_fast = denoise_nl_means(noisy, h=0.8 * sigma_est, fast_mode=True,
                                    **patch_kw)

    # fast algorithm, sigma provided
    denoise2_fast = denoise_nl_means(noisy, h=0.6 * sigma_est, sigma=sigma_est,
                                     fast_mode=True, **patch_kw)

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(8, 6),
                           sharex=True, sharey=True)

    ax[0, 0].imshow(noisy, cmap=plt.cm.gray)
    ax[0, 0].axis('off')
    ax[0, 0].set_title('noisy')
    ax[0, 1].imshow(denoise, cmap=plt.cm.gray)
    ax[0, 1].axis('off')
    ax[0, 1].set_title('non-local means\n(slow)')
    ax[0, 2].imshow(denoise2, cmap=plt.cm.gray)
    ax[0, 2].axis('off')
    ax[0, 2].set_title('non-local means\n(slow, using $\\sigma_{est}$)')
    ax[1, 0].imshow(my_picture, cmap=plt.cm.gray)
    ax[1, 0].axis('off')
    ax[1, 0].set_title('original\n(noise free)')
    ax[1, 1].imshow(denoise_fast, cmap=plt.cm.gray)
    ax[1, 1].axis('off')
    ax[1, 1].set_title('non-local means\n(fast)')
    ax[1, 2].imshow(denoise2_fast, cmap=plt.cm.gray)
    ax[1, 2].axis('off')
    ax[1, 2].set_title('non-local means\n(fast, using $\\sigma_{est}$)')

    fig.tight_layout()

    # print PSNR metric for each case
    psnr_noisy = peak_signal_noise_ratio(my_picture, noisy)
    psnr = peak_signal_noise_ratio(my_picture, denoise)
    psnr2 = peak_signal_noise_ratio(my_picture, denoise2)
    psnr_fast = peak_signal_noise_ratio(my_picture, denoise_fast)
    psnr2_fast = peak_signal_noise_ratio(my_picture, denoise2_fast)

    print(f"PSNR (noisy) = {psnr_noisy:0.2f}")
    print(f"PSNR (slow) = {psnr:0.2f}")
    print(f"PSNR (slow, using sigma) = {psnr2:0.2f}")
    print(f"PSNR (fast) = {psnr_fast:0.2f}")
    print(f"PSNR (fast, using sigma) = {psnr2_fast:0.2f}")

    return plt, denoise, denoise2, denoise_fast, denoise2_fast, noisy


def save(plot, name):
    plot.savefig(r'denoising/' + str(name) + '.png')
    gc.collect()


if __name__ == '__main__':
    # change this number to access different pictures
    num = 10

    # Load an example image
    img = io.imread('pictures\\' + str(num) + '.png')

    # process on image
    img = img_as_float(img)
    img = color.rgb2gray(img)
    print(img.shape)
    # plt_v, img = my_module.main(img, 0.2)
    img = img[2000:2500, 1500:2000]
    print(img.shape)

    p, dn, dn2, dn_f, dn_f2, nsy = main(img, 0.05)
    save(p, num)
