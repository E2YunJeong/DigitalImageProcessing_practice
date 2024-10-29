import numpy as np, cv2

def onChange1(value):												# 트랙바 콜백 함수
    global image1, image2, image, alpha, beta                        	# 전역 변수 참조

    alpha = value/100

    image = cv2.addWeighted(image1 , alpha, image2 , beta, 0)
    image = cv2.hconcat([image1, image, image2])
    cv2.imshow(title, image)

def onChange2(value):												# 트랙바 콜백 함수
    global image1, image2, image, alpha, beta                        	# 전역 변수 참조

    beta = value/100

    image = cv2.addWeighted(image1 , alpha, image2 , beta, 0)
    image = cv2.hconcat([image1, image, image2])
    cv2.imshow(title, image)

def scaling_bilinear(img, size):                   	# 양선형 보간
    ratioY, ratioX = np.divide(size[::-1], img.shape[:2])  # 변경 크기 비율

    dst = [[ bilinear_value(img, (j/ratioX, i/ratioY))  # for문 이용한 리스트 생성
             for j in range(size[0])]
           for i in range(size[1])]
    return np.array(dst, img.dtype)

def bilinear_value(img, pt):
    x, y = np.int32(pt)
    if x >= img.shape[1]-1: x = x -1
    if y >= img.shape[0]-1: y = y - 1

    P1, P2, P3, P4 = np.float32(img[y:y+2,x:x+2].flatten())

    alpha, beta = pt[1] - y,  pt[0] - x                   # 거리 비율
    M1 = P1 + alpha * (P3 - P1)                      # 1차 보간
    M2 = P2 + alpha * (P4 - P2)
    P  = M1 + beta  * (M2 - M1)                     # 2차 보간
    return  np.clip(P, 0, 255)                       # 화소값 saturation후 반환

image1 = cv2.imread("mid_fig1.jpg", cv2.IMREAD_GRAYSCALE)   # 영상 읽기
image2 = cv2.imread("mid_fig2.jpg", cv2.IMREAD_GRAYSCALE)
if image1 is None or image2 is None: raise Exception("영상 파일 읽기 오류 발생")

h1 = image1.shape[0]
h2 = image1.shape[1]
w1 = image2.shape[0]
w2 = image2.shape[1]
h = max(h1, h2)
w = max(w1, w2)
#각 이미지별 최대 크기에 맞게 스케일링 (양선형 보간)

alpha = beta = 0

size = (w, h)
image1 = scaling_bilinear(image1, size)
image2 = scaling_bilinear(image2, size)
image = np.zeros((h, w), np.uint8)

title = "dst"

image = cv2.hconcat([image1, image, image2])
cv2.imshow(title, image)

cv2.createTrackbar("image1", title, 0, 100, onChange1)	# 트랙바 콜백 함수 등록
cv2.createTrackbar("image2", title, 0, 100, onChange2)	# 트랙바 콜백 함수 등록
cv2.waitKey(0)
