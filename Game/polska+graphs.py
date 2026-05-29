import pygame
import random
import math
from os import path
from pygame.locals import *
from pygame.math import Vector2
from pygame import mixer

WIDTH = 1080
HEIGHT = 700
FPS = 60

img_dir = path.join(path.dirname(__file__), 'img')
background1 = pygame.image.load(path.join(img_dir, 'lvl1_background.png'))
background_rect1 = background1.get_rect()
background2 = pygame.image.load(path.join(img_dir, 'lvl2_background.png'))
background_rect2 = background2.get_rect()
background3 = pygame.image.load(path.join(img_dir, 'lvl3_background.png'))
background_rect3 = background3.get_rect()
mob_img = pygame.image.load(path.join(img_dir, 'mob.png'))
background_rect = []
farm_img1 = pygame.image.load(path.join(img_dir, 'base1.png'))
farm_img_rect1 = farm_img1.get_rect()
farm_img2 = pygame.image.load(path.join(img_dir, 'base2.png'))
farm_img_rect2 = farm_img2.get_rect()
farm_img3 = pygame.image.load(path.join(img_dir, 'base3.png'))
farm_img_rect3 = farm_img3.get_rect()
special_effect = pygame.image.load(path.join(img_dir, 'special_effect.png'))
r_cow = pygame.image.load(path.join(img_dir, 'r_cow.png'))
polska_cow = pygame.image.load(path.join(img_dir, 'polska_cow.png'))

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

farm_imgs = [farm_img1, farm_img2, farm_img3]
farm_rects = [farm_img_rect1, farm_img_rect2, farm_img_rect3]
colors = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW]
#direction = ['w','s','a','d']
score = 0
img_number = 0
enemies = 0
location = 1
waves = 1
last_polska = 0
background = background1
background_rect = background_rect1
spawn = True
polska = False
enough = False
win = False

font_name = pygame.font.match_font('arial')  #text


def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct, color, n):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGHT * n
    outline_rect = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, color, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def newmob():
    if not win:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        global enemies
        enemies += 1


# defining what player is
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50, 40)) # setting a rectangle
        #self.image.fill(GREEN)
        self.image = r_cow
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2  # defining center
        self.rect.bottom = HEIGHT - 10
        self.shield = 100
        self.shoot_delay = 300
        self.velx = 5  # the initial speed on x and y
        self.vely = 5  # basically defining the vriables

        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0  # every iteration the speed is set to zero
        self.speedy = 0  # so that it moves only when buttoon is pressed
        if not polska:
            self.image = r_cow
            self.shoot_delay = 300
            self.velx = 5
            self.vely = 5
        else:
            self.image = polska_cow
            self.shoot_delay = 0
            self.velx = -6
            self.vely = -6
        keystate = pygame.key.get_pressed()  # setting of controls
        if keystate[pygame.K_a]:
            self.speedx = -self.velx
            self.speedy = 0
        if keystate[pygame.K_d]:
            self.speedx = self.velx
            self.speedy = 0
        if keystate[pygame.K_s]:
            self.speedy = self.vely
            self.speedx = 0
        if keystate[pygame.K_w]:
            self.speedy = -self.vely
            self.speedx = 0
        if keystate[pygame.K_SPACE] or polska:
            if not win:
                self.shoot()

        if self.rect.right > WIDTH:  # boundaries for the player
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        self.rect.x += self.speedx  # speed is coordinate + or - value per second
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            keystate = pygame.key.get_pressed()  # setting of controls
            if not polska:
              
                if keystate[pygame.K_a]:
                    bullet.image = pygame.Surface((10, 5))
                    bullet.image.fill(WHITE)
                    bullet.speedx = -6
                    bullet.speedy = 0
                if keystate[pygame.K_d]:
                    bullet.image = pygame.Surface((10, 5))
                    bullet.image.fill(WHITE)
                    bullet.speedx = 6
                    bullet.speedy = 0
                if keystate[pygame.K_s]:
                    bullet.image = pygame.Surface((5, 10))
                    bullet.image.fill(WHITE)
                    bullet.speedy = 6
                    bullet.speedx = 0
                if keystate[pygame.K_w]:
                    bullet.image = pygame.Surface((5, 10))
                    bullet.image.fill(WHITE)
                    bullet.speedy = -6
                    bullet.speedx = 0
            all_sprites.add(bullets)
            bullets.add(bullet)
            mixer.init()
            mixer.music.load('Tank_Shooting.wav')
            mixer.music.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        if not polska:
            self.image.fill(WHITE)
        else:
            self.image.fill(colors[random.randrange(0, 6)])
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 40
        self.rect.centerx = x
        self.speedy = -6
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.bottom < 0) or (self.rect.top > HEIGHT) or (
                self.rect.left > WIDTH) or (self.rect.right < 0):
            self.kill()


class Grass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = special_effect
        #self.image = pygame.Surface((30,30))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = 2
        self.speedy = 2
        if polska:
            self.image = pygame.transform.rotate(self.image, 180.0)
        """self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100 , -40)
        self.speedy = random.randrange(1 , 8)
        self.speedx = random.randrange(-3 , 3)"""

    def update(self):
        if polska:
            self.speedy = 4
            self.speedx = 4
        #self.rect.y += self.speedy
        #self.rect.x -= self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            #self.speedy = random.randrange(1 , 8)
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        fx, fy = WIDTH / 2 - self.rect.x, HEIGHT - 150 - self.rect.y
        dist = math.hypot(dx, dy)
        distf = math.hypot(fx, fy)
        if distf < dist:
            dx = fx
            dy = fy
            dist = distf
        if dist < 30:
            self.kill()
        dx, dy = dx / (dist + 0.000001), dy / (dist + 0.000001)
        self.rect.x += dx * self.speedx + random.randrange(-2, 2)
        self.rect.y += dy * self.speedy + random.randrange(-1, 2)


class Farm(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = farm_imgs[img_number]
        self.rect = farm_rects[img_number]
        self.rect.centerx = WIDTH / 2 - 80  # defining center
        self.rect.bottom = HEIGHT - 150
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.bottom
        self.shield = 1000

    def update(self):
        self.image = farm_imgs[img_number]
        self.rect = farm_rects[img_number]
        self.rect.centerx = WIDTH / 2 - 80  # defining center
        self.rect.bottom = HEIGHT - 150
        self.rect.x = self.rect.centerx
        self.rect.y = self.rect.bottom


# making game and window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lachase")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group(
)  # we need to say that player is a class and a sprite
player = Player()
all_sprites.add(player)  # adding a player to the group of sprites
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
farm = Farm()
all_sprites.add(farm)
grasses = pygame.sprite.Group()

for i in range(5):
    newmob()

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

    if enemies < 1:
        waves += 1
        if polska:
            n = 3
        else:
            n = 1
        a = 4 * waves * location * int(not win) * n
        for i in range(a):
            if not win:
                newmob()

    if waves > 5:
        location += 1
        waves = 1

    if location == 2:
        background = background2
        background_rect = background_rect2
        img_number = 1
    elif location == 3:
        background = background3
        background_rect = background_rect3
        img_number = 2
    elif location > 3 or location == 0:
        win = True
        background = background3
        background_rect = background_rect3
        img_number = 2

    # updating
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 1
        enemies -= 1
        if random.random() > 0.9 and not polska and pygame.time.get_ticks(
        ) - last_polska > 1200:
            gr = Grass()
            grasses.add(gr)
            all_sprites.add(grasses)

    hits = pygame.sprite.spritecollide(
        player, mobs, True,
        pygame.sprite.collide_circle)  # change on False to get pizdec mode
    for hit in hits:
        player.shield -= 10
        enemies -= 1
        if player.shield <= 0:
            running = False

    hits = pygame.sprite.spritecollide(farm, mobs, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        farm.shield -= 10
        enemies -= 1
        if farm.shield <= 0:
            running = False

    hits = pygame.sprite.spritecollide(
        player, grasses, True,
        pygame.sprite.collide_circle)  # the beggining of POLSKA mode
    for hit in hits:
        polska = True
        now = pygame.time.get_ticks()

    healing = False
    if player.rect.centerx > WIDTH / 2 - 150 and player.rect.centerx < WIDTH / 2 + 150 and player.rect.centery > HEIGHT - 180:
        if player.shield < 100:
            player.shield += 0.05
        if player.shield < 100:
            healing = True
        else:
            healing = False

    dying = False
    if player.shield < 45:
        dying = True
        mixer.init()
        mixer.music.load('Explode_Tank.wav')
        mixer.music.play()

    polska_healing = False

    if polska:
        if not enough:
            if player.shield < 1000:
                polska_healing = True
            else:
                enough = True
        polska_timer = int(31 - (pygame.time.get_ticks() - now) / 1000)
        if polska_timer == 0:
            last_polska = pygame.time.get_ticks()
            polska = False
            enemies = 0
            all_sprites.remove(mobs)
            for i in range(5):
                newmob()

    # rapid increase of health in polska mode
    if polska_healing:
        player.shield += 0.5
    # rapid decrease of hp after polska mode
    if not polska:
        if player.shield > 100:
            player.shield -= 5

    # rendering
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    #all text
    draw_text(screen, str(score), 18, WIDTH / 2, 10, WHITE)
    if not win:
        draw_text(screen, 'wave: ' + str(waves), 18, 30, 30, WHITE)
        draw_text(screen, 'enemies left: ' + str(enemies), 18, 50, 45, WHITE)
    else:
        draw_text(screen, 'YOU WIN', 40, WIDTH / 2, HEIGHT / 2, WHITE)

    if healing and not polska:
        draw_text(screen, 'state: healing', 18, 47.2, 60, GREEN)
    if dying:
        draw_text(screen, 'attention: healing required', 18, 85, 78, RED)
    if polska:
        draw_text(screen, 'state: ', 18, 20.2, 60, WHITE)
        draw_text(screen, 'polska ', 18, 70.2 + random.randrange(-2, 2), 60,
                  RED)
        if polska_timer > 20:
            draw_text(screen, str(polska_timer), 18, 101.2, 60, GREEN)
        elif polska_timer > 10:
            draw_text(screen, str(polska_timer), 18,
                      101.2 + random.randrange(-1, 1), 60, YELLOW)
        else:
            draw_text(screen, str(polska_timer), 18,
                      101.2 + random.randrange(-2, 2), 60, RED)

    # hp bars
    if not polska:
        draw_shield_bar(screen, 5, 5, player.shield, RED, 1)
    else:
        draw_shield_bar(screen, 5, 5, player.shield,
                        colors[random.randrange(0, 6)], 1)
    draw_shield_bar(screen, 5, 20, farm.shield, WHITE, 0.1)

    # after drawing everything turn the screen
    pygame.display.flip()


pygame.quit()
