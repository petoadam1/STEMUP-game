import pygame, sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600,600])
base_font = pygame.font.Font(None, 32)
user_text = ''

# x, y = 200 helyen fogkirajzolódni, a 140 széles, 32 magas téglalap
input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')
color = color_passive

active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

        if event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode

    screen.fill((0,0,0,))

    pygame.draw.rect(screen, color, input_rect, 2)

    if active:
        color = color_active
    else:
        color = color_passive


    text_surface = base_font.render(user_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y +5))

    #ez felelős azért, hogy akkora legyen a téglalap szélessége, mint a szöveg
    input_rect.w = max(100, text_surface.get_width() + 10)

    pygame.display.flip()
    clock.tick(60)