#! /usr/bin/env python

from random import choice

import lidapy
from lidapy import LIDAThread

action_topic = lidapy.Topic('actions')

actions = ['LEFT', 'RIGHT', 'UP', 'DOWN']


def send_action():
    action = choice(actions)
    action_topic.send(action)


# Initialize the lidapy framework
lidapy.init(process_name='sensory_motor_memory')
LIDAThread(name='sensory_motor_memory', callback=send_action).start()
