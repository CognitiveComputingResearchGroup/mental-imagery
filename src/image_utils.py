import numpy as np
import cv2


def display(img):
    cv2.imshow("Image", img)
    cv2.waitKey(0)


def select_pixels(img, area):
    return cv2.bitwise_and(img, area)


def get_image_segments(img):
    shifted = cv2.pyrMeanShiftFiltering(img, 20, 50)
    gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)[1]

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    return cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]


def get_pixels_for_segment(img, segment):
    cimg = np.zeros_like(img)
    cv2.drawContours(cimg, [segment], -1, color=(255, 255, 255), thickness=-1)
    return select_pixels(img, cimg)


def crop_to_segment(img, segment):
    x, y, w, h = cv2.boundingRect(segment)
    return img[y: y + h, x: x + w]


img = cv2.imread('../resources/pixel_layer.png')

segments = get_image_segments(img)

for segment in segments:
    masked_img = get_pixels_for_segment(img, segment)
    display(masked_img)
    cropped_image = crop_to_segment(masked_img, segment)
    display(cropped_image)
