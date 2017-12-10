#! /usr/bin/env python

import numpy as np
import cv2

import lidapy
from lidapy import LIDAThread
from sensor_msgs.msg import CompressedImage

image_topic = lidapy.Topic('images', msg_type=CompressedImage, queue_size=1)
score_topic = lidapy.Topic('score', queue_size=1)


def receive_image():
    msg = image_topic.receive()  # type: CompressedImage
    if msg:
        pixel_matrix = np.fromstring(msg.data, np.uint8)
        open_cv_image = cv2.imdecode(pixel_matrix, flags=cv2.IMREAD_COLOR)


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
