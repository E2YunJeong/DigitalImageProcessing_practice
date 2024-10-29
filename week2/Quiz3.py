import numpy as np
import cv2

# 이미지 불러오기
image = cv2.imread('C:/Users/Administrator/Downloads/rgb.png', cv2.IMREAD_COLOR)
if image is None:
    raise Exception("영상 파일 읽기 에러")

# 채널 분리 : 컬러영상 -> 3채널 분리
split_rgb = cv2.split(image)
cv2.imshow("image", image) # 기본 이미지
cv2.imshow("Blue", split_rgb[0]) # Blue 채널
cv2.imshow("Green", split_rgb[1]) # Green 채널
cv2.imshow("Red", split_rgb[2]) # Red 채널
cv2.waitKey(0)