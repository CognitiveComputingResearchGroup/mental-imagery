from StringIO import StringIO

import lidapy
import pygame, math

from random import choice
from pygame import image
from pygame import font
from pygame import display
from pygame.time import Clock
from datetime import timedelta
from PIL import Image

from sensor_msgs.msg import CompressedImage

# Initializing Python Libraries
pygame.init()
lidapy.init(process_name='Environment')

# Color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
GRAY = (50, 50, 50)

# Screen dimensions
WIDTH = 470
HEIGHT = 300

# Frames Per Second
FPS = 30

# Game Constants
SCORE_INCREMENT = 10
PIECE_MIN_DELTA = 5
SCORE_DISTANCE_IN_PIXELS = 5.0
START_STATES = [(15, 60), (15, 210), (330, 210), (385, 20)]

# ROS message topics
image_topic = lidapy.Topic('images', msg_type=CompressedImage, queue_size=1)
score_topic = lidapy.Topic('score', queue_size=1)
action_topic = lidapy.Topic('actions', queue_size=1)


class GameObject:
    def __init__(self, image, pos):
        self.image = image
        self.rect = image.get_rect()
        self.rect.left, self.rect.top = pos

    def move(self, offset):
        self.rect = self.rect.move(offset)

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, value):
        self.rect.left = value

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, value):
        self.rect.top = value

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, value):
        self.rect.width = value

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, value):
        self.rect.height = value

    @property
    def center(self):
        return self.rect.center


# Current Game State
score = 0
elapsed_time = 0
next_action = ''

# Initialize Game Objects
clock = Clock()
screen = display.set_mode((WIDTH, HEIGHT))

background = image.load('../resources/wood_background.jpg').convert()
hole = GameObject(image.load('../resources/hole.png').convert_alpha(), [0, 0])
hole.move([(WIDTH - hole.width) / 2, (HEIGHT - hole.height) / 2])
piece = GameObject(image.load('../resources/wooden_circle.png').convert_alpha(), list(choice(START_STATES)))


def display_score():
    text = font.SysFont(None, 28).render("Score: {}".format(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.left = int(screen.get_rect().left + 20)
    text_rect.centery = 40
    screen.blit(text, text_rect)


def display_elapsed_time():
    global elapsed_time
    d = timedelta(milliseconds=elapsed_time)

    frac_seconds = d.total_seconds()
    seconds = int(frac_seconds)
    millis = int((frac_seconds - seconds) * 1000)

    text = font.SysFont(None, 28).render("Elapsed Time: {}.{}".format(seconds, millis), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.left = int(screen.get_rect().left + 20)
    text_rect.centery = 20

    screen.blit(text, text_rect)


def draw_background():
    global background
    screen.blit(background, background.get_rect())
    screen.blit(hole.image, hole.rect)


def draw_always_visible():
    display_elapsed_time()
    display_score()


def draw_object(object):
    screen.blit(object.image, object.rect)


def screenshot(screen):
    screenshot = Image.frombytes('RGB', screen.get_size(), pygame.image.tostring(screen, 'RGB'))

    img_buffer = StringIO()
    screenshot.save(img_buffer, 'JPEG')

    msg = CompressedImage()
    msg.format = 'jpeg'
    msg.data = img_buffer.getvalue()

    return msg


def process_agent_action(action):
    offset = [0, 0]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or action == 'UP':
        offset = [0, -PIECE_MIN_DELTA]
    if keys[pygame.K_DOWN] or action == 'DOWN':
        offset = [0, PIECE_MIN_DELTA]
    if keys[pygame.K_LEFT] or action == 'LEFT':
        offset = [-PIECE_MIN_DELTA, 0]
    if keys[pygame.K_RIGHT] or action == 'RIGHT':
        offset = [PIECE_MIN_DELTA, 0]

    piece.move(offset)


def is_in_hole(piece):
    p0 = hole.center
    p1 = piece.center

    distance = math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)
    if distance <= SCORE_DISTANCE_IN_PIXELS:
        return True


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    process_agent_action(next_action)

    if is_in_hole(piece):
        score = score + SCORE_INCREMENT

        # choose random start loc for respawn
        piece.rect.left, piece.rect.top = choice(START_STATES)

    draw_background()
    draw_object(piece)
    draw_always_visible()

    display.update()

    clock.tick(FPS)
    elapsed_time = elapsed_time + clock.get_time()

    image_topic.send(screenshot(screen))
    score_topic.send(score)
    next_action = action_topic.receive(timeout=.001)
