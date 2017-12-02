#! /usr/bin/env python

from PIL import Image
from StringIO import StringIO

import lidapy
from lidapy import LIDAThread
from sensor_msgs.msg import CompressedImage

image_topic = lidapy.Topic('images', msg_type=CompressedImage, queue_size=1)
score_topic = lidapy.Topic('score', queue_size=1)


def receive_image():
    msg = image_topic.receive()  # type: CompressedImage
    if msg:
        # TODO: Create the pixel layer from this image's data
        image = Image.open(StringIO(msg.data))


def receive_score():
    msg = score_topic.receive()
    if msg:
        print msg


# Initialize the lidapy framework
lidapy.init(process_name='sensory_memory')

# Launch environment listeners
LIDAThread(name='image receiver', callback=receive_image).start()
LIDAThread(name='score receiver', callback=receive_score).start()
