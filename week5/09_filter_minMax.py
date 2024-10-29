import numpy as np, cv2


def minmax_filter(image, ksize, mode):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.uint8)
    center = ksize // 2

    for i in range(center, rows - center):
        for j in range(center, cols - center):
            y1, y2 = i - center, i + center + 1
            x1, x2 = j - center, j + center + 1
            mask = image[y1:y2, x1:x2]
            dst[i, j] = cv2.minMaxLoc(mask)[mode]

    return dst


image = cv2.imread("C:/Users/Administrator/Downloads/chap7_images/min_max.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영사 파일 읽기 오류")

minFilter_img = minmax_filter(image, 3, 0)
maxFilter_img = minmax_filter(image, 3, 1)

cv2.imshow("image", image)
cv2.imshow("minFilter_img", minFilter_img)
cv2.imshow("maxFilter_img", maxFilter_img)
cv2.waitKey(0)
