import pygame
import array as arr
import button
import random
import numpy as np
import mysql.connector
from configparser import ConfigParser

pygame.init()
clock = pygame.time.Clock()
fps = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Predefined values
screen_width = 800
screen_height = 400
start = 600  # 60 = 1 second, 600 = 10 seconds, 3600 = 1 minute, 108000 = 30 minutes
timer = 0
gmsp = 15  # generate map starter pixel
ns = 40  # node_size / csomópont x és y koordináta

# Fonts
fontType = pygame.font.Font('font/8-BIT WONDER.ttf', 16)
tinyType = pygame.font.Font('font/8-BIT WONDER.ttf', 10)
base_font = pygame.font.Font(None, 32)
smaller_font = pygame.font.Font(None, 16)

# Database connection
file = 'config.ini'
config = ConfigParser()
config.read(file)
host = config['database']['host']
user = config['database']['user']
passwd = config['database']['passwd']
database = config['database']['database']
db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
mycursor = db.cursor()

# Screen display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tanar')

# Images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
theoretical_question_img = pygame.image.load('img/Icons/theoretical_question_icon.png').convert_alpha()
boss_question_img = pygame.image.load('img/Icons/boss_question_icon.png').convert_alpha()
practical_question_img = pygame.image.load('img/Icons/practical_question_icon.png').convert_alpha()
extra_loot_question_img = pygame.image.load('img/Icons/extra_loot_question_icon.png').convert_alpha()

# Booleans
menu = True
generate_map = False
clicked = False
click_is_free = True
start_ticking = False
able_to_countdown = False
empty_time_text = False
wrong_time_text = False
empty_floor_text = False
wrong_floor_text = False
empty_row_text = False
wrong_row_text = False
time_active = False
floor_active = False
row_active = False
ticks = pygame.time.get_ticks()
floor_size = None
row_size = None


# Functions
def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def get_scores():
    scores = 'scores.ini'
    score_config = ConfigParser()
    score_config.read(scores)

    mycursor.execute("SELECT * FROM students")
    result = mycursor.fetchall()
    # print(len(result))
    length = len(result)
    for f in range(length):
        neptunc = result[f][0]
        score = result[f][1]
        print(neptunc)
        print(score)
        score_config.add_section(str(neptunc))
        score_config.set(str(neptunc), 'score', str(score))
        with open(scores, 'w') as configfile:
            score_config.write(configfile)


def delete_map_infos():
    mycursor.execute("TRUNCATE TABLE map")
    db.commit()
    mycursor.execute("TRUNCATE TABLE floor_row_size")
    db.commit()
    mycursor.execute("TRUNCATE TABLE students")
    db.commit()


def select_floor_size(floor):
    mycursor.execute("SELECT count(*) FROM map WHERE floor = %s", (floor,))
    current_size = mycursor.fetchall()
    return current_size[0][0]


def update_c1(c1, k):
    mycursor.execute("UPDATE map SET c1 = %s WHERE id = %s", (c1, k,))
    db.commit()


subtitle1 = 'Time'
subtitle2 = 'Floor'
subtitle3 = 'Row'

# Input strings
time_text = ''
floor_text = ''
row_text = ''

# Input rectangles create, define colors of rectangle backgrounds
input_rect_time = pygame.Rect(350, 142, 100, 30)
input_rect_floor = pygame.Rect(350, 192, 100, 30)
input_rect_row = pygame.Rect(350, 242, 100, 30)
color_active = pygame.Color(237, 176, 71)
color_passive = pygame.Color(150, 100, 32)
time_color = color_passive
floor_color = color_passive
row_color = color_passive


# Game loop
run = True
while run:
    clock.tick(fps)

    # Menu
    if menu:
        draw_bg()
        draw_text(subtitle1, tinyType, WHITE, screen_width / 2 - 50, screen_height / 2 - 70)
        draw_text(subtitle2, tinyType, WHITE, screen_width / 2 - 50, screen_height / 2 - 20)
        draw_text(subtitle3, tinyType, WHITE, screen_width / 2 - 50, screen_height / 2 + 30)
        pygame.draw.rect(screen, time_color, input_rect_time)
        pygame.draw.rect(screen, floor_color, input_rect_floor)
        pygame.draw.rect(screen, row_color, input_rect_row)
        pygame.mouse.set_visible(True)
        posx, posy = pygame.mouse.get_pos()

        # Map generate button
        gm_x = screen_width / 2 - 50
        gm_y = screen_height / 2 + 80
        draw_text('Generate', tinyType, WHITE, gm_x, gm_y)
        draw_text('Map details', fontType, WHITE, screen_width / 2 - 49, screen_height / 2 - 100)
        draw_text('Minutes', smaller_font, WHITE, 455, 152)
        draw_text('4-15', smaller_font, WHITE, 455, 202)
        draw_text('3-7', smaller_font, WHITE, 455, 252)
        draw_text(str(start // 3600) + ' mins', fontType, WHITE, screen_width - 130, screen_height - 50)

        if time_active:
            time_color = color_active
        else:
            time_color = color_passive

        if floor_active:
            floor_color = color_active
        else:
            floor_color = color_passive

        if row_active:
            row_color = color_active
        else:
            row_color = color_passive

        text_surface_time = base_font.render(time_text, True, (0, 0, 0))
        screen.blit(text_surface_time, (input_rect_time.x + 5, input_rect_time.y + 5))
        text_surface_floor = base_font.render(floor_text, True, (0, 0, 0))
        screen.blit(text_surface_floor, (input_rect_floor.x + 5, input_rect_floor.y + 5))
        text_surface_row = base_font.render(row_text, True, (0, 0, 0))
        screen.blit(text_surface_row, (input_rect_row.x + 5, input_rect_row.y + 5))

        # generate map click
        if click_is_free:
            if gm_x < posx < gm_x + 240 and gm_y < posy < gm_y + 200:
                if clicked:
                    print(floor_text.isdigit())
                    if time_text.isdigit() and floor_text.isdigit() and row_text.isdigit():
                        start = (int(time_text) * 3600)
                        able_to_countdown = True
                        # print(start)
                        floor_size = int(floor_text)
                        row_size = int(row_text)
                        mycursor.execute("TRUNCATE TABLE students")
                        db.commit()
                        mycursor.execute("TRUNCATE TABLE floor_row_size")
                        db.commit()
                        mycursor.execute("INSERT INTO floor_row_size (floor_size, row_size, start_time, timer) VALUES (%s, %s, %s, %s)",
                                         (floor_size, row_size, start, timer))
                        db.commit()
                        generate_map = True
                    elif len(time_text) == 0:
                        empty_time_text = True
                    elif len(floor_text) == 0:
                        empty_floor_text = True
                    elif len(row_text) == 0:
                        empty_row_text = True
                    else:
                        wrong_time_text = True
                        wrong_floor_text = True
                        wrong_row_text = True

                    click_is_free = False
                    start_ticking = True

        if empty_time_text:
            draw_text('Pls enter time', tinyType, WHITE, 10, 10)
        elif wrong_time_text:
            draw_text('Pls enter int', tinyType, WHITE, 10, 10)
        if empty_floor_text:
            draw_text('Pls enter floor size', tinyType, WHITE, 10, 10)
        elif wrong_floor_text:
            draw_text('Pls enter int', tinyType, WHITE, 10, 10)
        if empty_row_text:
            draw_text('Pls enter row size', tinyType, WHITE, 10, 10)
        elif wrong_row_text:
            draw_text('Pls enter int', tinyType, WHITE, 10, 10)

        if start_ticking:
            if pygame.time.get_ticks() - ticks > 100 and event.type == pygame.MOUSEBUTTONUP:
                click_is_free = True
                start_ticking = False
                ticks = pygame.time.get_ticks()

    # Generate Map
    if generate_map:
        mycursor.execute("TRUNCATE TABLE map")
        db.commit()
        question_button = np.zeros((floor_size * row_size, 4))

        # all possible nodes
        count = 0
        # all created nodes
        count2 = 0
        asd = True
        rand = -1
        rand2 = -1
        rand3 = -1
        # fill question_button[]
        for i in range(floor_size):
            for j in range(row_size):

                # minden új oszlopnál randomizáljon
                if count % row_size == 0:
                    if row_size <= 3:
                        rand = random.randint(0, (row_size - 1))
                    if 3 < row_size <= 5:
                        rand = random.randint(0, (row_size - 1))
                        rand2 = random.randint(0, (row_size - 1))
                    if 5 < row_size <= 8:
                        rand = random.randint(0, (row_size - 1))
                        rand2 = random.randint(0, (row_size - 1))
                        rand3 = random.randint(0, (row_size - 1))
                if rand != j and rand2 != j and rand3 != j:

                    if i == 0:
                        x = gmsp
                    else:
                        x = gmsp + (screen_width / floor_size * i)

                    y = (screen_height / row_size * (j + 1)) - (screen_height / row_size / 2) - (ns / 2)

                    question_button[count][0] = x
                    question_button[count][1] = y
                    question_button[count][3] = i

                    r = random.randint(0, 99)
                    # theoretical question
                    if 0 <= r < 30:
                        question_button[count][2] = 1
                        # question_button[count] = button.Button(screen, x, y, theoretical_question_img, 40, 40)
                    # practical question
                    elif 30 <= r < 60:
                        question_button[count][2] = 2
                        # question_button[count] = button.Button(screen, x, y, practical_question_img, 40, 40)
                    # boss question
                    elif 60 <= r < 80:
                        question_button[count][2] = 3
                        # question_button[count] = button.Button(screen, x, y, boss_question_img, 40, 40)
                    # extra loot question
                    else:
                        question_button[count][2] = 4
                        # question_button[count] = button.Button(screen, x, y, extra_loot_question_img, 40, 40)
                    # print('count')
                    # print(count)
                    # print('rand')
                    # print(rand)
                    # print('j')
                    # print(j)
                    mycursor.execute("INSERT INTO map (id, x, y, question_type, floor) VALUES (%s, %s, %s, %s, %s)",
                                     (count2,
                                      float(question_button[count][0]), float(question_button[count][1]),
                                      float(question_button[count][2]), float(question_button[count][3]),))
                    db.commit()
                    count2 += 1
                count += 1

        mycursor.execute("SELECT MAX(floor) FROM map")
        max = mycursor.fetchall()
        floor_sizes = np.zeros(16)

        for i in range(max[0][0] + 2):
            floor_sizes[i] = select_floor_size(i)

        variable = np.zeros(16)
        amount = 0

        for i in range(max[0][0] + 2):
            variable[i] = amount
            amount = amount + floor_sizes[i]

        #floor left and right side
        for x in range(14):
            #floor counter
            for k in range(count2):
                asd = True
                if variable[x] <= k < variable[x + 1] and (max[0][0]) > x:
                    c1 = random.randint(variable[x + 1], (variable[x + 2] - 1))
                    update_c1(c1, k)
                if variable[x + 2] > k >= variable[x + 1] and (max[0][0]) > x:
                    for a in range(int(variable[x]), int(variable[x + 1])):
                        mycursor.execute("SELECT c1 FROM map WHERE id = %s", (a,))
                        result = mycursor.fetchall()
                        if k == result[0][0]:
                            asd = False
                    if asd:
                        c2 = random.randint(variable[x], (variable[x + 1] - 1))
                        mycursor.execute("UPDATE map SET c2 = %s WHERE id = %s", (c2, k,))
                        db.commit()

        generate_map = False

    # Timer
    if able_to_countdown:
        # start -= 1
        timer += 1
        mycursor.execute("UPDATE floor_row_size SET timer = %s WHERE start_time = %s", (timer, start))
        db.commit()
        if timer >= start:
            run = False
        # if start <= 0:
        #     run = False

    # Events (clicks, keydowns, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            if input_rect_time.collidepoint(event.pos):
                empty_time_text = False
                wrong_time_text = False
                time_active = True
            else:
                time_active = False

            if input_rect_floor.collidepoint(event.pos):
                empty_floor_text = False
                wrong_floor_text = False
                floor_active = True
            else:
                floor_active = False

            if input_rect_row.collidepoint(event.pos):
                empty_row_text = False
                wrong_row_size_text = False
                row_active = True
            else:
                row_active = False

        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if time_active:
                if event.key == pygame.K_BACKSPACE:
                    time_text = time_text[0:-1]
                else:
                    if input_rect_time.w > (text_surface_time.get_width() + 15):
                        time_text += event.unicode
            if floor_active:
                if event.key == pygame.K_BACKSPACE:
                    floor_text = floor_text[0:-1]
                else:
                    if input_rect_floor.w > (text_surface_floor.get_width() + 15):
                        floor_text += event.unicode
            if row_active:
                if event.key == pygame.K_BACKSPACE:
                    row_text = row_text[0:-1]
                else:
                    if input_rect_row.w > (text_surface_row.get_width() + 15):
                        row_text += event.unicode

    pygame.display.update()

# When the game ends, write out points and emptying tables
get_scores()
delete_map_infos()
pygame.quit()
