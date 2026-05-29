import pygame
import sys
from os import path

pygame.init()

WIDTH = 1080
HEIGHT = 700
spawn = True
img_dir = path.join(path.dirname(__file__), 'img')
Play_Button = pygame.image.load(path.join(img_dir,"Start.png"))
Settings_Button = pygame.image.load(path.join(img_dir,"Settings.png"))
Exit_Button = pygame.image.load(path.join(img_dir,"Exit.png"))

i = [Play_Button, Settings_Button, Exit_Button]

pygame.display.set_caption('LACHASE')
icon = pygame.image.load(path.join(img_dir,'cow.png'))
pygame.display.set_icon(icon)
Screen = pygame.display.set_mode((1080, 700), pygame.RESIZABLE, 64)
BG = pygame.image.load(path.join(img_dir,"Group16.png"))
BG_rect = BG.get_rect()
all_sprites = pygame.sprite.Group()


class Buttons(pygame.sprite.Sprite):
    def __init__(self, y, z):
        pygame.sprite.Sprite.__init__(self)
        k = z
        self.image = i[k]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.y = y


buts = pygame.sprite.Group()

start_game = False
running = True

while running:
    Screen.blit(BG, BG_rect)
    A = Buttons(345, 0)
    all_sprites.add(A)
    buts.add(A)

    B = Buttons(450, 1)
    all_sprites.add(B)
    buts.add(B)

    C = Buttons(550, 2)
    all_sprites.add(C)
    buts.add(C)


    all_sprites.update()
    all_sprites.draw(Screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH / 2 - 120 <= mouse[0] <= WIDTH / 2 + 115 and HEIGHT / 2 + 197 <= mouse[1] <= HEIGHT / 2 + 280:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH / 2 - 120 <= mouse[0] <= WIDTH / 2 + 115 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 80:
                import game #The name of the file in which the game code

    pygame.display.update()

pygame.quit()