import numpy as np, cv2

image = cv2.imread("C:/Users/user/pythonProject_test/images/chap7_images/dog_test.jpg", cv2.IMREAD_COLOR)
if image is None:
    raise Exception("영상 파일 읽기 오류")

title = "canny edge"

def bar(value) :

    # 낮은 임계값 th1과 높은 임계값 th2 구하기
    th1 = cv2.getTrackbarPos('th1', title)
    th2 = cv2.getTrackbarPos('th2', title)

    # 구한 임계값으로 캐네 에지 검출하기
    result = cv2.Canny(image, th1, th2)

    cv2.imshow(title, result)

# 캐니 에지 검출하기 (낮은 임계값은 100, 높은 임계값은 150을 디폴트로 검출)
result = cv2.Canny(image, 100, 150)

cv2.namedWindow(title)

cv2.createTrackbar('th1', title, 0, 255, bar)
cv2.createTrackbar('th2', title, 0, 255, bar)

cv2.setTrackbarPos('th1', title, 50)
cv2.setTrackbarPos('th2', title, 150)

cv2.waitKey(0)