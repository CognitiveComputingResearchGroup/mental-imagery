#! /usr/bin/env python

import numpy as np
import cv2

import lidapy
from lidapy import LIDAThread
from sensor_msgs.msg import CompressedImage

import image_utils as img_utils

image_topic = lidapy.Topic('images', msg_type=CompressedImage, queue_size=1)
score_topic = lidapy.Topic('score', queue_size=1)

pixel_layer = None
segmented_layer = None


def receive_image():
    msg = image_topic.receive()  # type: CompressedImage
    if msg:
        pixel_matrix = np.fromstring(msg.data, np.uint8)
        open_cv_image = cv2.imdecode(pixel_matrix, flags=cv2.IMREAD_COLOR)
        build_segmented_layer(open_cv_image)


def build_segmented_layer(img):
    segments = img_utils.get_image_segments(img)

    for segment in segments:
        masked_img = img_utils.get_pixels_for_segment(img, segment)
        img_utils.display(masked_img, wait_for_keypress=True)


def receive_score():
    msg = score_topic.receive()
    if msg:
        pass
        # print msg


# Initialize the lidapy framework
lidapy.init(process_name='sensory_memory')

# Launch environment listeners
LIDAThread(name='image receiver', callback=receive_image).start()
LIDAThread(name='score receiver', callback=receive_score).start()
