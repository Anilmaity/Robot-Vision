import cv2
import numpy as np


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def adaptive_gausssian_threshold(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                 cv2.THRESH_BINARY, 11, 2)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 1)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 100, 200, cv2.THRESH_BINARY)


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


img = cv2.imread('../object_detection_model/yolov5/img1.jpg')
img = cv2.resize(img, (500, 500))
temp = cv2.imread('images/img2.jpg')

cv2.imshow('img', get_grayscale(img))
cv2.waitKey(0)

cv2.imshow('img', canny(img))
cv2.waitKey(0)

cv2.imshow('img', erode(img))
cv2.waitKey(0)

cv2.imshow('img', dilate(img))
cv2.waitKey(0)
