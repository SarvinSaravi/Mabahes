import gc
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
            if image_bw[r][c] == 0:
                if r not in rows:
                    rows.append(r)
                if c not in cols:
                    cols.append(c)

    row_x1 = min(rows) - 5
    row_x2 = max(rows) + 5
    col_y1 = min(cols) - 5
    col_y2 = max(cols) + 5

    return row_x1, row_x2, col_y1, col_y2


filepath = 'picture\\Q3.png'
image = io.imread(filepath)

image = img_as_float(image)
data_detection(image)

print('end')
