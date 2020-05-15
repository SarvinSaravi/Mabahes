import gc
import matplotlib.pyplot as plt
from skimage import io, color, img_as_float

filepath = 'picture\\Q3.png'
image = io.imread(filepath)

image_bw = img_as_float(image)
image_bw = color.rgb2gray(image)

rows = []
cols = []

for r in range(100):
    for c in range(100):
        if image_bw[r][c] == 0:
            if r not in rows:
                rows.append(r)
            if c not in cols:
                cols.append(c)

row_x1 = min(rows) - 5
row_x2 = max(rows) + 5
col_y1 = min(cols) - 5
col_y2 = max(cols) + 5

image_bw[row_x1, col_y1:col_y2] = 0
image_bw[row_x2, col_y1:col_y2] = 0
image_bw[row_x1:row_x2, col_y1] = 0
image_bw[row_x1:row_x2, col_y2] = 0

plt.imshow(image_bw, cmap=plt.cm.gray)
plt.savefig(r'picture/result2.png')
gc.collect()
