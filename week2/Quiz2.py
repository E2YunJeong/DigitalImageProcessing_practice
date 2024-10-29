import numpy as np
import cv2

# 메인 윈도우 사이즈 지정
cv2.namedWindow('image')
cv2.resizeWindow(winname='image', width=400, height=400)

# 이미지 불러오기
image = cv2.imread('C:/Users/Administrator/Downloads/fig.jpg', cv2.IMREAD_GRAYSCALE)
if image is None:
    raise Exception("영상 파일 읽기 에러")

# 관심영역 좌표 및 지정
x = 30
y = 50
w = 320
h = 300
roi = image[y:y + h, x:x + w]

# 관심영역 화소값 평균
print("관심영역 화소값 평균 : ", cv2.mean(roi))

# 영상 밝기 50만큼 높이기
dst = np.clip(roi + 50., 0, 255).astype(np.uint8)
cv2.imshow("image", image)
cv2.imshow("dst + 50", dst)
cv2.waitKey(0)
