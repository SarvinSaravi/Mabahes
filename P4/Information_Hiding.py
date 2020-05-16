import matplotlib.pyplot as plt
from skimage import io, color, img_as_float


def data_detection(image):
    image_bw = img_as_float(image)
    image_bw = color.rgb2gray(image_bw)

    rows = []
    cols = []

    x, y = image_bw.shape

    for r in range(x):
        for c in range(y):
            if image_bw[r][c] < 1:
                if r not in rows:
                    rows.append(r)
                if c not in cols:
                    cols.append(c)

    row_x1 = min(rows) - 5
    row_x2 = max(rows) + 5
    col_y1 = min(cols) - 5
    col_y2 = max(cols) + 5

    return row_x1, row_x2, col_y1, col_y2, image_bw


def encoding(rx1, rx2, cy1, cy2, img1):
    for r in range(rx1, rx2):
        for c in range(cy1, cy2, 2):
            tmp = 0.5 + (0.5 - img1[r][c])
            img1[r][c] = tmp

    for r in range(rx1, rx2, 2):
        for c in range(cy1, cy2):
            tmp = 0.5 + (0.5 - img1[r][c])
            img1[r][c] = tmp

    plt.imshow(img1, cmap=plt.cm.gray)
    plt.show()

    return img1


if __name__ == '__main__':
    filepath = 'picture\\Q5.png'
    image = io.imread(filepath)

    x1, x2, y1, y2, img = data_detection(image)
    img = encoding(x1, x2, y1, y2, img)
    s = encoding(x1, x2, y1, y2, img)
