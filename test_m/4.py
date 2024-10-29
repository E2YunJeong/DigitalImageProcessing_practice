import numpy as np, cv2

def contain(p, shape):                              # 좌표(y,x)가 범위내 인지 검사
    return 0<= p[0] < shape[0] and 0<= p[1] < shape[1]

def translate(img, pt):
    dst = np.zeros(img.shape, img.dtype)            # 목적 영상 생성
    for i in range(img.shape[0]):                           # 목적 영상 순회 - 역방향 사상
        for j in range(img.shape[1]):
            x, y = np.subtract((j, i) , pt)
            if contain((y, x), img.shape):
                dst[i, j] = img[y, x]
    return dst

def onMouse(event, x, y, flags, param):
    global image, h, w
    # 콜백 함수 – 이벤트 내용 출력
    if event == cv2.EVENT_LBUTTONDOWN:
        print("중심 좌표 값 : ",x,y)
        tran_x = int(w/2 - x)
        tran_y = int(h/2 - y)
        dst = translate(image, (tran_x, tran_y))
        cv2.imshow("image", dst)


image = cv2.imread('mid_fig4.jpg', cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상 파일을 읽기 에러")

#중앙 좌표를 얻기 위한 영상 크기 획득
h, w = image.shape

print("영상 기존 중심 좌표 :", w/2, h/2)

cv2.imshow("image", image)
cv2.setMouseCallback("image", onMouse, 0)
cv2.waitKey(0)