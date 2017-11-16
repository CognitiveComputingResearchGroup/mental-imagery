import sys, pygame

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

piece_move_delta = 5

score = 0

pygame.init()

screen = pygame.display.set_mode((width, height))
background = pygame.image.load('../resources/wood_background.jpg').convert()
piece_left = 100
piece_height = 100

def display_score():
    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render("Score: {}".format(score), True, (255, 0, 0))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = 24
    screen.blit(text, textrect)

def draw_background(background):
    screen.blit(background, background.get_rect())
    pygame.draw.circle(screen, black, (background.get_rect().width / 2, background.get_rect().height / 2), 30, 0)
    pygame.draw.circle(screen, gray, (background.get_rect().width / 2, background.get_rect().height / 2), 29, 5)
    display_score()

def process_event():
    global score, piece_height, piece_left
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            piece_height = piece_height - piece_move_delta
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            piece_height = piece_height + piece_move_delta
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            piece_left = piece_left - piece_move_delta
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            piece_left = piece_left + piece_move_delta
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return
        elif event.type == pygame.MOUSEBUTTONUP:
            score = score + 10

# def detect_collision():
#     offset_x, offset_y = (myOtherImage_rect.left - myImage_rect.left), (myOtherImage_rect.top - myImage_rect.top)
#     if (myImage_mask.overlap(myOtherImage_mask, (offset_x, offset_y)) != None):
#         print 'Collision Detected!'
#     else:
#         print 'None'


class GameObject:
    def __init__(self, image, pos):
        self.image = pygame.image.load(image).convert()
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


while True:
    process_event()

    draw_background(background)

    pygame.draw.circle(screen, blue, (piece_left, piece_height), 28, 0)

    pygame.display.update()
    pygame.time.delay(10)
