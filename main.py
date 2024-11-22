import pygame, sys
from pygame.locals import *
import random, time

# initiate game engine
pygame.init()

# set game fps
FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5.0
SCORE = 0

# Set up fonts
'''
set up 2 fonts, with font and size
use render() to create the surface to be passed into blit() later
'''
font = pygame.font.SysFont('Verdana', 60)
font_small = pygame.font.SysFont('Verdana', 20)
# the game over surface doesnt't change, so we render it outside of the game loop
game_over = font.render('Game over!', True, BLACK)


# Make display and fill with white background
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load('assets/AnimatedStreet.png')
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")  # what does this do?

class Enemy(pygame.sprite.Sprite):  # enemy class extends from sprite
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load('assets/Enemy.png')
    self.rect = self.image.get_rect()
    self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

  def move(self):
    global SCORE
    self.rect.move_ip(0, SPEED)
    if (self.rect.top > SCREEN_HEIGHT):
      SCORE += 1
      self.rect.top = 0
      self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)


class Player(pygame.sprite.Sprite):
  def __init__(self):
    # init the sprite things
    super().__init__()
    # get the image
    self.image = pygame.image.load("assets/Player.png")
    # create a rect for the object
    self.rect = self.image.get_rect()
    # define starting position
    self.rect.center = (160, 520)

  def move(self):
    pressed_keys = pygame.key.get_pressed()
    # if pressed_keys[K_UP]:
    #   self.rect.move_ip(0, -5)
    # if pressed_keys[K_DOWN]:
    #   self.rect.move_ip(0, 5)
    # when press left, move left 5 units (pixels?)
    if pressed_keys[K_LEFT]:
      self.rect.move_ip(-5, 0)
    if pressed_keys[K_RIGHT]:
      self.rect.move_ip(5, 0)


# set up sprites
P1 = Player()
E1 = Enemy()

# create sprite groups
'''
sprite groups - for us to group sprites(entities) together
one group for enemies, one group for all sprites
'''
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new user event
'''
we create a user event, and increment by 1 to give it a unique ID
then, we use pygame.time.set_timer to invoke this event every 1000ms, or 1 second
'''
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#game loop
while True:

  # cycle through all events
  for event in pygame.event.get():
    '''
    When the event type is INC_SPEED, we increment the speed by 2 (used by enemies)
    '''
    if event.type == INC_SPEED:
      SPEED += 0.5

    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # blit the background first, so we can blit over it with other entities like player and enemy
  DISPLAYSURF.blit(background, (0,0))
  # this score changes, so we need to render it within the game loop
  scores = font_small.render(str(SCORE), True, BLACK)
  # use blit() to actually draw it onto the screen
  DISPLAYSURF.blit(scores, (10, 10))

  # move and redraw all sprites
  for entity in all_sprites:
    DISPLAYSURF.blit(entity.image, entity.rect)
    entity.move()

  # handle collision between player and enemy
  '''
  pygame.sprite.spritecollideany:
    takes 2 args - a sprite, and a sprite group
    returns true / truthy if the first sprite touches any sprite in the group
    this is why grouping sprites is good - so we can use spritecollideany to
      check whether any of those sprites in the group have collided with player

  if collision occurs, we:
  1. fill the display red
  2. go through all_sprites and kill each sprite
    this removes the sprite from the group, which means they wont be drawn
  3. wait 2 seconds
  4. quit pygame and sys
  '''
  if pygame.sprite.spritecollideany(P1, enemies):
    # use pygame mixer library to load the (short) sound, then play() it
    # for longer music tracks, we need to use a separate function in pygame mixer
    pygame.mixer.Sound('assets/crash.wav').play()
    time.sleep(0.5)

    DISPLAYSURF.fill(RED)
    DISPLAYSURF.blit(game_over, (30,250))

    pygame.display.update()
    for entity in all_sprites:
      entity.kill()
    time.sleep(2)
    pygame.quit()
    sys.exit()

  pygame.display.update()
  FramePerSec.tick(FPS)