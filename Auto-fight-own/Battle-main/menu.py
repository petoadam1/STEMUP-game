import pygame
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
screen_width = 800
screen_height = 400

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Menu')

background_img = pygame.image.load('img/Background/background.png').convert_alpha()
play_button = pygame.image.load('img/Icons/play-button.png').convert_alpha()
settings_button = pygame.image.load('img/Icons/settings-button.png').convert_alpha()
inventory_button = pygame.image.load('img/Icons/inventory-button.png').convert_alpha()

def draw_bg_icons():
    screen.blit(background_img, (0, 0))
    screen.blit(play_button, (screen_width / 2 - 100, screen_height * 0.33))
    screen.blit(settings_button, (screen_width / 2 - 100, screen_height * 0.50))
    screen.blit(inventory_button, (730, 10))


run = True
while run:

    clock.tick(fps)

    draw_bg_icons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()