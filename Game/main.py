import pygame #ANTON TI NE TAM SMOTRISH
import random
import math

WIDTH = 1080
HEIGHT = 700
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# defining what player is
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40)) # setting a rectangle
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 # defining center
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 # the initial speed on x and y
        self.speedy = 0 # basically defining the vriables
    def update(self):
        self.speedx = 0 # every iteration the speed is set to zero
        self.speedy = 0 # so that it moves only when buttoon is pressed
        keystate = pygame.key.get_pressed() # setting of controls
        if keystate[pygame.K_a]:
            self.image = pygame.Surface((40, 50))
            self.image.fill(GREEN)
            self.speedx = -3
            self.speedy = 0
        elif keystate[pygame.K_d]:
            self.image = pygame.Surface((40, 50))
            self.image.fill(GREEN)
            self.speedx = 3
            self.speedy = 0
        elif keystate[pygame.K_s]:
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)
            self.speedy = 3
            self.speedx = 0
        elif keystate[pygame.K_w]:
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)
            self.speedy = -3
            self.speedx = 0
        else:
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)

        self.rect.x += self.speedx # speed is coordinate + or - value per second
        self.rect.y += self.speedy
        if self.rect.right > WIDTH: # boundaries for the player
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        keystate = pygame.key.get_pressed()  # setting of controls
        if keystate[pygame.K_a]:
            bullet.image = pygame.Surface((10, 5))
            bullet.image.fill(WHITE)
            bullet.speedx = -4
            bullet.speedy = 0
        if keystate[pygame.K_d]:
            bullet.image = pygame.Surface((10, 5))
            bullet.image.fill(WHITE)
            bullet.speedx = 4
            bullet.speedy = 0
        if keystate[pygame.K_s]:
            bullet.image = pygame.Surface((5,10))
            bullet.image.fill(WHITE)
            bullet.speedy = 4
            bullet.speedx = 0
        if keystate[pygame.K_w]:
            bullet.image = pygame.Surface((5,10))
            bullet.image.fill(WHITE)
            bullet.speedy = -4
            bullet.speedx = 0

        all_sprites.add(bullets)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 40
        self.rect.centerx = x
        self.speedy = 4
        self.speedx = 0
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.bottom < 0) or (self.rect.top > HEIGHT) or (self.rect.left > WIDTH) or (self.rect.right < 0):
            self.kill()

# making game and window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lachase")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group() # we need to say that player is a class and a sprite
player = Player()
all_sprites.add(player) # adding a player to the group of sprites
bullets = pygame.sprite.Group()
# game cycle
running = True
while running:
    # maintaining game speed
    clock.tick(FPS)
    # input of the process
    for event in pygame.event.get():
        # if the game is closed
        if event.type == pygame.QUIT:
            running = False
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_ESCAPE]:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # updating
    all_sprites.update()

    # rendering
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing everything turn the screen
    pygame.display.flip()

pygame.quit()