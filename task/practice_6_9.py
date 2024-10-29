import numpy as np, cv2

# image1, image2에 대한 트랙바 콜백 함수
def bar(value):
    global alpha, beta, title, image1, image2, add_result

    alpha = cv2.getTrackbarPos('image1', title) / 100
    beta = cv2.getTrackbarPos('image2', title) / 100

    # 두 영상 비율에 따른 더하기
    add_result = cv2.addWeighted(image1, alpha, image2, beta, 0)

    # 이미지 가로로 붙이기
    numpy_horizontal = np.hstack((image1, add_result, image2))

    cv2.imshow(title, numpy_horizontal)


image1 = cv2.imread('C:/Users/user/pythonProject_test/images/chap6_images/add1.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('C:/Users/user/pythonProject_test/images/chap6_images/add2.jpg', cv2.IMREAD_GRAYSCALE)
if image1 is None or image2 is None:
    raise Exception("영상 파일 읽기 에러")

title = "dst"

cv2.namedWindow(title)

# image1 트랙바
cv2.createTrackbar('image1', title, 0, 100, bar)
# image2 트랙바
cv2.createTrackbar('image2', title, 0, 100, bar)

# 초기 트랙바 설정
cv2.setTrackbarPos('image1', title, 50)
cv2.setTrackbarPos('image2', title, 50)

cv2.waitKey(0)