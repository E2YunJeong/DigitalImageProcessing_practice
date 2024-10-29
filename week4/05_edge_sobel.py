import numpy as np, cv2


def filter(image, mask):
    rows, cols = image.shape[:2]

    dst = np.zeros((rows, cols), np.float32)
    ycenter, xcenter = mask.shape[0] // 2, mask.shape[1] // 2

    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1
            roi = image[y1:y2, x1:x2].astype('float32')
            tmp = cv2.multiply(roi, mask)
            dst[i, j] = cv2.sumElems(tmp)[0]

    return dst

def differential(image, data1, data2):
    mask1 = np.array(data1, np.float32).reshape(3, 3)
    mask2 = np.array(data2, np.float32).reshape(3, 3)

    dst1 = filter(image, mask1)
    dst2 = filter(image, mask2)
    dst = cv2.magnitude(dst1, dst2)

    dst = cv2.convertScaleAbs(dst)
    dst1 = cv2.convertScaleAbs(dst1)
    dst2 = cv2.convertScaleAbs(dst2)

    return dst, dst1, dst2


image = cv2.imread('C:/Users/Administrator/Downloads/edge.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 에러")

data1 = [-1, 0, 1,
         -2, 0, 2,
         -1, 0, 1]
data2 = [-1, - 2, -1,
         0, 0, 0,
         1, 2, 1]

dst, dst1, dst2 = differential(image, data1, data2)

dst3 = cv2.Sobel(np.float32(image), cv2.CV_32F, 1, 0, 3)
dst4 = cv2.Sobel(np.float32(image), cv2.CV_32F, 0, 1, 3)
dst3 = cv2.convertScaleAbs(dst3)
dst4 = cv2.convertScaleAbs(dst4)

cv2.imshow("dst1- vertical_mask", dst1)
cv2.imshow("dst2- horizontal_mask", dst1)
cv2.imshow("dst3- vertical_OpenCV", dst1)
cv2.imshow("dst4- vertical_OpenCV", dst1)
cv2.waitKey(0)
