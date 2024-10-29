import cv2
import numpy as np


def calc_histo(image, histSize, ranges=[0, 256]):
    hist = np.zeros((histSize, 1), np.float32)
    gap = ranges[1] / histSize

    for i in (image / gap).flat:
        hist[int(i)] += 1
    return hist


image = cv2.imread('C:/Users/Administrator/Downloads/chap6_images/color_model.jpg/pixel.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 에러")

histSize, ranges = [32], [0, 256]
gap = ranges[1] / histSize[0]
ranges_gap = np.arange(0, ranges[1] + 1, gap)
hist1 = calc_histo(image, histSize[0], ranges)
hist2 = cv2.calcHist([image], [0], None, histSize, ranges)
hist3, bins = np.histogram(image, ranges_gap)

print("User 함수 : \n", hist1.flatten())
print("OpenCV 함수 : \n", hist2.flatten())
print("numpy 함수 : \n", hist3)
