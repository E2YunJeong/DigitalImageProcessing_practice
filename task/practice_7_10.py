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
            tmp = cv2.multiply(roi, mask, dtype=cv2.CV_32F)
            dst[i, j] = cv2.sumElems(tmp)[0]

    dst = np.clip(dst, 0, 255)
    return dst

image = cv2.imread("C:/Users/user/pythonProject_test/images/chap7_images/filter_sharpen.jpg", cv2.IMREAD_COLOR)
if image is None:
    raise Exception("영상 파일 읽기 오류")

sharpen_data = [ 0, -1, 0,
                -1, 5, -1,
                0, -1, 0]
blur_data = [1 / 9, 1 / 9, 1 / 9,
            1 / 9, 1 / 9, 1 / 9,
            1 / 9, 1 / 9, 1 / 9]

sharpen_mask = np.array(sharpen_data, np.float32).reshape(3, 3)
blur_mask = np.array(blur_data, np.float32).reshape(3,3)

# 채널 분리 : 컬러영상 -> 3채널 분리
b, g, r = cv2.split(image)

b_blur_user = filter(b, blur_mask)
g_blur_user = filter(g, blur_mask)
r_blur_user = filter(r, blur_mask)

b_sharpen_user = filter(b, sharpen_mask)
g_sharpen_user = filter(g, sharpen_mask)
r_sharpen_user = filter(r, sharpen_mask)

bluring_user = cv2.merge([b_blur_user, g_blur_user, r_blur_user]).astype(np.uint8)
sharpen_user = cv2.merge([b_sharpen_user, g_sharpen_user, r_sharpen_user]).astype(np.uint8)

bluring_opencv = cv2.filter2D(image, -1, blur_mask)
sharpen_opencv = cv2.filter2D(image, -1, sharpen_mask)


cv2.imshow("image", image)
cv2.imshow("sharpen User", sharpen_user)
cv2.imshow("sharpen OpenCV", sharpen_opencv)
cv2.imshow("bluring User", bluring_user)
cv2.imshow("bluring OpenCV", bluring_opencv)
cv2.waitKey(0)