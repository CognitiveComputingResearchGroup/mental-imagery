import numpy as np
import cv2

def display(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)

from matplotlib import pyplot as plt
img = cv2.imread('../resources/pixel_layer.png')
shifted = cv2.pyrMeanShiftFiltering(img, 21, 51)
gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)[1]

# noise removal
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
contours = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

# For each list of contour points...
for i in range(len(contours)):
    # Create a mask image that contains the contour filled in
    cimg = np.zeros_like(img)
    cv2.drawContours(cimg, contours, i, color=(255,255,255), thickness=-1)
    display(cimg)
    maskedImg = cv2.bitwise_and(img, cimg)
    display(maskedImg)

for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    cimg = np.zeros_like(img)
    cv2.rectangle(cimg,(x,y),(x+w,y+h),(255,255,255),-1)
    maskedImg = cv2.bitwise_and(img, cimg)
    display(maskedImg)