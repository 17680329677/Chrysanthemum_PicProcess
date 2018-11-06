import cv2
import numpy as np
import os


def crop_mum(file, name):
    # 1.加载图片转成灰度图
    img = cv2.imread(file)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gradX = cv2.Sobel(gray_img, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray_img, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 85, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    image, cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    # cv2.drawContours(img, [box], -1, (0, 255, 0), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = min(Xs)
    x2 = max(Xs)
    y1 = min(Ys)
    y2 = max(Ys)
    hight = y2 - y1
    width = x2 - x1
    length = max(hight, width)

    cropImg = img[y1:y1 + length, x1:x1 + length]

    #win = cv2.namedWindow('win', flags=0)
    cv2.imwrite('G:/result/' + name.split('.')[0] + '.jpg', cropImg)
    # cv2.imshow('win', cropImg)
    # cv2.waitKey()


if __name__ == '__main__':
    L = []
    # root为文件根路径，dirs为该路径下子文件夹， files为该目录下所有文件的文件名
    for root, dirs, files in os.walk('G:\\origin'):
        for file in files:
            crop_mum(os.path.join(root, file), file)


    # crop_mum('G:/origin/42-1_20171124_15.png', '42-1_20171124_15.png')