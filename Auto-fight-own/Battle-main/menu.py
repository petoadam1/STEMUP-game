import pygame
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#game window
screen_width = 800
screen_height = 400

font = pygame.font.SysFont('Times New Roman', 26)
smallerFont = pygame.font.SysFont('Times New Roman', 22)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Menu')


background_img = pygame.image.load('img/Background/background.png').convert_alpha()
play_button = pygame.image.load('img/Icons/play-button.png').convert_alpha()
settings_button = pygame.image.load('img/Icons/settings-button.png').convert_alpha()
inventory_img = pygame.image.load('img/Icons/inventory-button.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
#bagpack image
bp_img = pygame.image.load('img/Icons/inventory_with_x.png').convert_alpha()

# inventory_image = inventory_img.get_rect()
# inventory_image.center = (760, 40)

inventory_click = False
# inventory_click2 = False
# did_click = False
inventory_button = button.Button(screen, 10, 10, inventory_img, 60, 60)

def draw_bg_icons():
    screen.blit(background_img, (0, 0))
    screen.blit(play_button, (screen_width / 2 - 100, screen_height * 0.33))
    screen.blit(settings_button, (screen_width / 2 - 100, screen_height * 0.50))
    # screen.blit(inventory_button, (730, 10))

open_inventory = False
is_inventory_open = True

def draw_bp(x, y):
    screen.blit(bp_img, (x, y))

class Account():
    def __init__(self, name, hp, power, defense):
        self.name = name
        self.hp = hp
        self.power = power
        self.defense = defense

fighter = Account('Adam', 50, 15, 5)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

run = True
while run:

    clock.tick(fps)
    x = 60
    y = 60
    screen.fill(WHITE)
    draw_bg_icons()

    if inventory_button.draw():
        open_inventory = True
        is_inventory_open = True

    if open_inventory == True:
        draw_bp(x, y)
        draw_text(fighter.name, font, WHITE, 228, 135)
        draw_text(f'{fighter.hp}', smallerFont, BLACK, 170, 190)
        draw_text(f'{fighter.power}', smallerFont, BLACK, 170, 210)
        draw_text(f'{fighter.defense}', smallerFont, BLACK, 170, 230)

    pygame.mouse.set_visible(True)
    posx, posy = pygame.mouse.get_pos()

    if posx > 436 and posx < 460 and posy > 60 and posy < 84 and open_inventory == True and is_inventory_open == True:
        if clicked:
            is_inventory_open = False
            open_inventory = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()