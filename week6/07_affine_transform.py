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

def affine_transform(img, mat):
    rows, cols = img.shape[:2]
    inv_mat = cv2.invertAffineTransform(mat)
    pts = [np.dot(inv_mat, (j, i, 1)) for i in range(rows) for j in range(cols)]
    dst = [bilinear_value(img, p) if contain(p, size) else 0 for p in pts]
    dst = np.reshape(dst, (rows, cols)).astype('uint8')

    return dst

image = cv2.imread("C:/Users/Administrator/Downloads/chap8_images/affine.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 오류")

center = (200, 200)
angle, scale = 30, 1
size = image.shape[::-1]

pt1 = np.array([(30, 70), (20, 240), (300, 110)], np.float32)
pt2 = np.array([(120, 20), (10, 180), (280, 260)], np.float32)
aff_mat = cv2.getAffineTransform(pt1, pt2)
rot_mat = cv2.getRotationMatrix2D(center, angle, scale)

dst1 = affine_transform(image, aff_mat)
dst2 = affine_transform(image, rot_mat)
dst3 = cv2.warpAffine(image, aff_mat, size, cv2.INTER_LINEAR)
dst4 = cv2.warpAffine(image, rot_mat, size, cv2.INTER_LINEAR)

image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
dst1 = cv2.cvtColor(dst1, cv2.COLOR_GRAY2BGR)
dst3 = cv2.cvtColor(dst3, cv2.COLOR_GRAY2BGR)

for i in range(len(pt1)):
    cv2.circle(image, tuple(pt1[i].astype(int)), 3, (0, 0, 255), 2)
    cv2.circle(dst1, tuple(pt2[i].astype(int)), 3, (0, 0, 255), 2)
    cv2.circle(dst3, tuple(pt2[i].astype(int)), 3, (0, 0, 255), 2)

cv2.imshow("image", image)
cv2.imshow("dst1_affine", dst1)
cv2.imshow("dst2_affine_rotate", dst2)
cv2.imshow("dst3_OpenCV_affine", dst3)
cv2.imshow("dst4_OpenCV_affine_rotate", dst4)
cv2.waitKey(0)