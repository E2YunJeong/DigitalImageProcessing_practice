import numpy as np, cv2

def contain(p, shape):
    return 0 <= p[0] < shape[0] and 0 <= p[1] < shape[1]

def bilinear_value(img, pt):
    x, y = np.int32(pt)
    if x >= img.shape[1]-1: x=x-1
    if y >= img.shape[0]-1: y=y-1

    p1, p2, p3, p4 = np.float32(img[y:y+2, x:x+2].flatten())

    alpha, beta = pt[1] - y, pt[0] - x
    m1 = p1 + alpha * (p3-p1)
    m2 = p2 + alpha * (p4-p2)
    p = m1 + beta * (m2 - m1)
    return np.clip(p, 0, 255)

def rotate(img, degree):
    dst = np.zeros(img.shape[:2], img.dtype)
    radian = (degree/180) * np.pi
    sin, cos = np.sin(radian), np.cos(radian)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            y = -j * sin + i * cos
            x = j * cos + i * sin
            if contain((y, x), img.shape):
                dst[i, j] = bilinear_value(img, (x, y))
    return dst


def rotate_pt(img, degree, pt):
    dst = np.zeros(img.shape[:2], img.dtype)
    radian = (degree / 180) * np.pi
    sin, cos = np.sin(radian), np.cos(radian)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            jj, ii = np.subtract((j, i), pt)

            y = -jj * sin + ii * cos
            x = jj * cos + ii * sin
            x, y = np.add((x, y), pt)
            if contain((y, x), img.shape):
                dst[i, j] = bilinear_value(img, (x, y))
    return dst


image = cv2.imread("C:/Users/Administrator/Downloads/chap8_images/rotate.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 오류")

center = np.divmod(image.shape[::-1], 2)[0]
dst1 = rotate(image, 20)
dst2 = rotate_pt(image, 20, center)

cv2.imshow("image", image)
cv2.imshow("dst1: rotated on (0, 0)", dst1)
cv2.imshow("dst2: rotated on center point", dst2)
cv2.waitKey(0)

# 회전 중심값 (x, y), 회전각 제공
# 1. 그대로 출력
# 2. 중심값 그대로, 회전각 변경하여 출력
# 3. 회전각 그대로, 중심값 변경하여 출력
#
# 이거 시험문제 나올 듯
# 심화문제는 마우스로 클릭하는 거
# 생각해보는 건 값을 입력받았을 때 회전되는거