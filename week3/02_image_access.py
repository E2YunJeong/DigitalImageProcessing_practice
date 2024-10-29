import cv2
import numpy as np
import time


def pixel_access1(img):
    image_1 = np.zeros(img.shape[:2], img.dtype)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel = img[i, j]
            image_1[i, j] = 255 - pixel
    return image_1


def pixel_access2(img):
    image_2 = np.zeros(img.shape[:2], img.dtype)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            pixel = img.item(i, j)
            image_2[i, j] = 255 - pixel
    return image_2


def pixel_access3(img):
    lut = [255 - i for i in range(256)]
    lut = np.array(lut, np.uint8)
    image_3 = lut[img]
    return image_3


def pixel_access4(img):
    image_4 = cv2.subtract(255, img)
    return image_4


def pixel_access5(img):
    image_5 = 255 - img
    return image_5


image = cv2.imread("C:/Users/Administrator/Downloads/chap6_images/color_model.jpg/bright.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 오류")


def time_check(func, msg):
    start_time = time.perf_counter()
    ret_img = func(image)
    elapsed = (time.perf_counter() - start_time) * 1000
    print(msg, "수행 시간 : %0.2f ms" % elapsed)
    return ret_img


image1 = time_check(pixel_access1, "[방법1] 직접 접근 방식")
image2 = time_check(pixel_access2, "[방법2] item() 함수 방식")
image3 = time_check(pixel_access3, "[방법3] 룩업 테이블 방식")
image4 = time_check(pixel_access4, "[방법4] OpenCV 함수 방식")
image5 = time_check(pixel_access5, "[방법5] ndarray 연산 방식")
