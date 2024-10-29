import numpy as np, cv2

def filter(image, mask):
    rows, cols = image.shape[:2]
    dst = np.zeros((rows, cols), np.float32)                 # 회선 결과 저장 행렬
    xcenter, ycenter = mask.shape[1]//2, mask.shape[0]//2  # 마스크 중심 좌표

    for i in range(ycenter, rows - ycenter):                  # 입력 행렬 반복 순회
        for j in range(xcenter, cols - xcenter):
            y1, y2 = i - ycenter, i + ycenter + 1               # 관심영역 높이 범위
            x1, x2 = j - xcenter, j + xcenter + 1               # 관심영역 너비 범위
            roi = image[y1:y2, x1:x2].astype("float32")         # 관심영역 형변환

            tmp = cv2.multiply(roi, mask)                       # 회선 적용 - OpenCV 곱셈
            dst[i, j] = cv2.sumElems(tmp)[0]                    # 출력화소 저장
    return dst

image = cv2.imread("mid_fig3.jpg", cv2.IMREAD_GRAYSCALE)  # 영상 읽기
if image is None: raise Exception("영상파일 읽기 오류")

# 블러링 마스크 원소 지정
data = [[-1,0,0],
        [0,0,0],
        [0,0,1]]
mask = np.array(data, np.float32).reshape(3, 3)

embossing = filter(image, mask)

cv2.imshow("image", image)
cv2.imshow("embossing", embossing)
cv2.waitKey(0)