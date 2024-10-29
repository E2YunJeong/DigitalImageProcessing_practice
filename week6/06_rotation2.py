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

def calc_angle(pt):
    d1 = np.subtract(pts[1], pts[0]).astype(float)
    d2 = np.subtract(pts[2], pts[0]).astype(float)
    angle1 = cv2.fastAtan2(d1[1], d1[0])
    angle2 = cv2.fastAtan2(d2[1], d2[0])
    return (angle2 - angle1)

def draw_point(x, y):
    pts.append([x, y])
    print("좌표: ", len(pts), [x,y])
    cv2.circle(tmp, (x, y), 2, 255, 2)
    cv2.imshow("image", tmp)

def onMouse(event, x, y, flags, param):
    global tmp, pts
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 0): draw_point(x, y)
    if (event == cv2.EVENT_LBUTTONDOWN and len(pts) == 1): draw_point(x, y)
    if (event == cv2.EVENT_LBUTTONUP and len(pts) == 2): draw_point(x, y)
    if len(pts) == 3:
        angle = calc_angle(pts)
        print("회전각 : %3.2f" % angle)
        dst = rotate_pt(image, angle, pts[0])
        cv2.imshow("image", dst)
        tmp = np.copy(image)
        pts = []


image = cv2.imread("C:/Users/Administrator/Downloads/chap8_images/rotate.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 오류")

tmp = np.copy(image)
pts = []

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)