# 히스토그램 스트레칭 : 명암 분포가 좁은 히스토그램을 좌우로 잡아 당겨(스트레칭) 고른 명암 분포를 가지도록 하는 것
# 히스토그램 평활화 : 한 쪽으로 치우친 명암 분포를 가지는 영상에 대해 재분배 과정을 거쳐 균등한 히스토그램을 가지도록 하는 것

import numpy as np, cv2

def calc_histo(image, hsize, ranges=[0, 256]):  # 행렬 원소의 1차원 히스토그램 계산
    hist = np.zeros((hsize, 1), np.float32)  # 히스토그램 누적 행렬
    gap = ranges[1]/hsize  # 계급 간격
    print(hist)
    for i in (image/gap).flat:
        hist[int(i)] += 1
    return hist

def draw_histo(hist, shape=(200, 256)):
    hist_img = np.full( shape, 255, np.uint8)
    cv2.normalize(hist, hist, 0, shape[0], cv2.NORM_MINMAX)
    gap = hist_img.shape[1]/hist.shape[0]             # 한 계급 너비

    for i, h in enumerate(hist):
        x = int(round(i * gap))                         # 막대 사각형 시작 x 좌표
        w = int(round(gap))
        roi = (x, 0, w, int(h))
        cv2.rectangle(hist_img, roi, 150, -1)
        cv2.rectangle(hist_img, roi, 0, 1)

    return   cv2.flip(hist_img, 0)                        # 영상 상하 뒤집기 후 반환


image = cv2.imread("mid_fig3.jpg", cv2.IMREAD_GRAYSCALE)  # 영상 읽기
if image is None: raise Exception("영상 파일 읽기 오류")

bins, ranges = [256], [0, 256]
hist = cv2.calcHist([image], [0], None, bins, ranges)    # 히스토그램 계산

# 히스토그램 누적합 계산
accum_hist = np.zeros(hist.shape[:2], np.float32)
accum_hist[0] = hist[0]
for i in range(1, hist.shape[0]):
    accum_hist[i] = accum_hist[i - 1] + hist[i]

accum_hist = (accum_hist / sum(hist)) * 255                 # 누적합의 정규화
dst1 = [[accum_hist[val] for val in row] for row in image] # 화소값 할당
dst1 = np.array(dst1, np.uint8)

# #numpy 함수 및 룩업 테이블 사용
accum_hist = np.cumsum(hist)                      # 누적합 계산
cv2.normalize(accum_hist, accum_hist, 0, 255, cv2.NORM_MINMAX)  # 정규화
dst2 = cv2.equalizeHist(image)                # OpenCV 히스토그램 평활화

hist2 = cv2.calcHist([dst2], [0], None, bins, ranges)   # 히스토그램 계산
hist_img = draw_histo(hist)
hist_img2 = draw_histo(hist2)

cv2.imshow("image", image);             cv2.imshow("hist_img", hist_img)
cv2.imshow("dst2_OpenCV", dst2);        cv2.imshow("OpenCV_hist", hist_img2)
cv2.waitKey(0)