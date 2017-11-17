import sys, pygame, math


class GameObject:
    def __init__(self, image, pos):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos

    def move(self, offset):
        self.rect = self.rect.move(offset)

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

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


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)
gray = (50, 50, 50)

width = 470
height = 300

piece_move_delta = 1

score = 0

pygame.init()

screen = pygame.display.set_mode((width, height))
background = pygame.image.load('../resources/wood_background.jpg').convert()
piece = GameObject(pygame.image.load('../resources/wooden_circle.png').convert_alpha(), [0, 0])
hole = GameObject(pygame.image.load('../resources/hole.png').convert_alpha(), [0, 0])

hole.move([(width - hole.width) / 2, (height - hole.height) / 2])


def display_score():
    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render("Score: {}".format(score), True, (255, 0, 0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = 24
    screen.blit(text, textrect)


def draw_background(background):
    screen.blit(background, background.get_rect())
    screen.blit(hole.image, hole.rect)

    display_score()


def draw_object(object):
    screen.blit(object.image, object.rect)


def process_game_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def process_key_event():
    offset = [0, 0]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        offset = [0, -piece_move_delta]
    if keys[pygame.K_DOWN]:
        offset = [0, piece_move_delta]
    if keys[pygame.K_LEFT]:
        offset = [-piece_move_delta, 0]
    if keys[pygame.K_RIGHT]:
        offset = [piece_move_delta, 0]

    piece.move(offset)


def is_in_hole(piece):
    p0 = hole.center
    p1 = piece.center

    distance = math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)
    if distance < 2.0:
        return True


while True:
    process_game_event()
    process_key_event()

    if is_in_hole(piece):
        score = score + 10

        # while piece.width > 0 or piece.height > 0:
        #     piece.width = int(piece.width * 0.9)
        #     piece.height = int(piece.height * 0.9)
        #
        #     draw_background(background)
        #     image = pygame.transform.smoothscale(piece.image, (piece.width, piece.height))
        #     screen.blit(image, image.get_rect())
        #
        #     pygame.display.update()
        #     pygame.time.delay(100)

        # reset piece
        piece.move([-piece.left, -piece.height])

    draw_background(background)
    draw_object(piece)

    pygame.display.update()
    pygame.time.delay(10)
