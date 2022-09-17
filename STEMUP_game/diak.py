import pygame
import button
import random
import numpy as np
import mysql.connector
from configparser import ConfigParser

pygame.init()
clock = pygame.time.Clock()
fps = 60

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

# Nones
floor_size = None
row_size = None
start = None
map_size = None
map_variables = None
max_floor = None
last_floor_count = None
container = None

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (60, 113, 159)
LIGHTGREEN = (37, 137, 26)
RED = (245, 66, 66)
MAXRED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen datas
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Diak')

# Fonts
battle_font = pygame.font.Font('font/8-BIT WONDER.ttf', 16)
fontType = pygame.font.Font('font/8-BIT WONDER.ttf', 20)
tinyType = pygame.font.Font('font/8-BIT WONDER.ttf', 10)
bigFont = pygame.font.Font('font/8-BIT WONDER.ttf', 46)
base_font = pygame.font.Font(None, 32)
answer_font = pygame.font.Font(None, 20)
question_font = pygame.font.Font(None, 26)

# Images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
login_img = pygame.image.load('img/Icons/login_button_2.png').convert_alpha()
theoretical_question_img = pygame.image.load('img/Icons/theoretical_question_icon.png').convert_alpha()
boss_question_img = pygame.image.load('img/Icons/boss_question_icon.png').convert_alpha()
practical_question_img = pygame.image.load('img/Icons/practical_question_icon.png').convert_alpha()
extra_loot_question_img = pygame.image.load('img/Icons/extra_loot_question_icon.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()

# Classes
# Fighter class
class Fighter:
    def __init__(self, x, y, name, max_hp, power, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = power
        self.defense = defense
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/warrior_death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), MAXRED)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        # self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

# Enemy class
class Bandit:
    def __init__(self, x, y, name, max_hp, power, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = power
        self.defense = defense
        # self.start_potions = potions
        # self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/warrior_hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/warrior_death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 200
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        # set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), MAXRED)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        # self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

# Health bar class
class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 20, 120))
        pygame.draw.rect(screen, MAXRED, (self.x, self.y, 20, 120 - (120 * ratio)))
    # pygame.draw.rect(screen, green, (self.x, self.y + (120 - (120 * ratio)), 20, 120 * ratio))

# Damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = battle_font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()
knighthp = 20
bandithp = 20
knight = Fighter(250, 315, 'Knight', knighthp, 30, 0)
bandit1 = Bandit(545, 315, 'Bandit', bandithp, 6, 0)

knight_health_bar = HealthBar(20, 10, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(750, 10, bandit1.hp, bandit1.max_hp)

# Booleans
no_map_added = False
login_screen = True
menu_screen = False
fight_screen = False
empty_neptuncode_text = False
wrong_neptuncode_text = False
used_neptuncode_text = False
neptuncode_active = False
attack = False
click_is_free = True
start_ticking = False
allow_timer = False
make_question = True

subtitle1 = 'Neptuncode'

# Input string
neptuncode_text = ''

# Input rectangles create, define colors of rectangle backgrounds
input_rect_neptuncode = pygame.Rect(300, 160, 200, 30)
color_active = pygame.Color(237, 176, 71)
color_passive = pygame.Color(150, 100, 32)
neptuncode_color = color_passive

# Define game variables
floor_completed = 0
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 75
game_over = 0
ticks = pygame.time.get_ticks()
floor_completed = 0
question_type = 0

# Buttons
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

# Functions
def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def print_line(result, i, x):
    mycursor.execute("select count(*) from map where floor = %s", (x,))
    asd = mycursor.fetchall()
    darab = asd[0][0]

    # print("darab")
    # print(darab)
    # print("i")
    # print(i)
    startX = result[i][0] + 8
    startY = result[i][1] + 4
    endX = result[i + darab][0] + 8
    endY = result[i + darab][1] + 4
    pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))


def draw_line_dashed(surface, color, start_pos, end_pos, width=1, dash_length=10, exclude_corners=True):
    # convert tuples to numpy arrays
    start_pos = np.array(start_pos)
    end_pos = np.array(end_pos)

    # get euclidian distance between start_pos and end_pos
    length = np.linalg.norm(end_pos - start_pos)

    # get amount of pieces that line will be split up in (half of it are amount of dashes)
    dash_amount = int(length / dash_length)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

    return [pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n + 1]), width)
            for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]


def draw_good_answer():
    img = battle_font.render('Good answer', True, GREEN)
    img_rect = img.get_rect().center
    screen.blit(img, (screen_width / 2 - img_rect[0], screen_height / 2))
    # draw_text(f'Good answer', battle_font, GREEN, (screen_width / 2 - 78),
    #           screen_height - 20)


def draw_wrong_answer():
    img = battle_font.render('Wrong answer', True, MAXRED)
    img_rect = img.get_rect().center
    screen.blit(img, (screen_width / 2 - img_rect[0], screen_height / 2))
    # draw_text(f'Wrong answer', battle_font, MAXRED, (screen_width / 2 - 92),
    #           screen_height - 20)


def draw_question_answers(variable, x, y, font):
    img = font.render(variable, True, WHITE)
    img_rect = img.get_rect().center
    screen.blit(img, (x - img_rect[0], y))


def draw_line_c1(a):
    startX = map_variables[a][1] + 7
    startY = map_variables[a][2] + 7
    c1 = (map_variables[a][5])
    # c1 helyen lévő id-nak az x értéke
    if c1 != -1:
        endX = map_variables[c1][1] + 7
        # c1 helyen lévő id-nak az y értéke
        endY = map_variables[c1][2] + 7
        draw_line_dashed(screen, LIGHTGREEN, (startX, startY), (endX, endY))
    # pygame.draw.line(screen, LIGHTGREEN, (startX, startY), (endX, endY))

    # c2 = map_variables[map_variables[a][0]][6]
    # if c2 != -1:
    #     endX = map_variables[map_variables[a][6]][1] + 7
    #     endY = map_variables[map_variables[a][6]][2] + 7
    #     draw_line_dashed(screen, LIGHTGREEN, (startX, startY), (endX, endY))
    #     # pygame.draw.line(screen, LIGHTGREEN, (startX, startY), (endX, endY))


def draw_line_c2(a):
    c2 = map_variables[map_variables[a][0]][6]
    if c2 != -1:
        startX = map_variables[a][1] + 7
        startY = map_variables[a][2] + 7
        endX = map_variables[map_variables[a][6]][1] + 7
        endY = map_variables[map_variables[a][6]][2] + 7
        draw_line_dashed(screen, LIGHTGREEN, (startX, startY), (endX, endY))
        # pygame.draw.line(screen, LIGHTGREEN, (startX, startY), (endX, endY))


def floor_indicator(a):
    img = base_font.render("A", True, WHITE)
    screen.blit(img, (map_variables[i][1], screen_height - 30))


def draw_congratulations():
    img = bigFont.render('Congratulations', True, WHITE)
    img_rect = img.get_rect().center
    screen.blit(img, (screen_width / 2 - img_rect[0], screen_height / 2))

# Game loop
run = True
while run:

    clock.tick(fps)

    # Login screen
    if login_screen:
        draw_bg()
        draw_text(subtitle1, fontType, WHITE, screen_width / 2 - 100, screen_height / 2 - 70)
        pygame.draw.rect(screen, neptuncode_color, input_rect_neptuncode)
        login_button = button.Button(screen, 420, 200, login_img, 80, 20)

        if neptuncode_active:
            neptuncode_color = color_active
        else:
            neptuncode_color = color_passive

        text_surface_neptuncode = base_font.render(neptuncode_text, True, (0, 0, 0))
        screen.blit(text_surface_neptuncode, (input_rect_neptuncode.x + 5, input_rect_neptuncode.y + 5))

        if login_button.draw():
            if len(neptuncode_text) == 6:
                mycursor.execute("SELECT neptuncode FROM students WHERE neptuncode = %s", (neptuncode_text,))
                result = mycursor.fetchall()
                if not result:

                    mycursor.execute("SELECT * FROM map")
                    map_variables = mycursor.fetchall()
                    if not map_variables:
                        no_map_added = True
                    else:
                        no_map_added = False
                        mycursor.execute("SELECT * FROM floor_row_size")
                        result = mycursor.fetchall()
                        floor_size = result[0][0]
                        row_size = result[0][1]
                        start = result[0][2]
                        mycursor.execute("SELECT count(*) FROM map")
                        result = mycursor.fetchall()
                        map_size = result[0][0]
                        mycursor.execute("SELECT MAX(floor) FROM map")
                        max_floor = mycursor.fetchall()
                        mycursor.execute("SELECT count(*) FROM map WHERE floor = %s", (max_floor[0][0],))
                        last_floor_count = mycursor.fetchall()
                        print('Logged')
                        login_screen = False
                        menu_screen = True
                        allow_timer = True
                        mycursor.execute("INSERT INTO students(neptuncode) VALUES (%s)", (neptuncode_text,))
                        db.commit()
                else:
                    used_neptuncode_text = True

            elif len(neptuncode_text) == 0:
                empty_neptuncode_text = True
            else:
                wrong_neptuncode_text = True

        if no_map_added:
            img = fontType.render('No map added', True, WHITE)
            img_rect = img.get_rect().center
            screen.blit(img, (screen_width / 2 - img_rect[0], screen_height / 2 + 160))

        if empty_neptuncode_text:
            draw_text('Pls enter your neptuncode', tinyType, WHITE, 10, 10)
        if wrong_neptuncode_text:
            draw_text('Pls enter right neptuncode ( 6 characters )', tinyType, WHITE, 10, 10)
        if used_neptuncode_text:
            draw_text('This neptuncode is already taken', tinyType, WHITE, 10, 10)

    # Menu screen
    if menu_screen:

        mycursor.execute("SELECT * FROM map")
        map_variables = mycursor.fetchall()
        if not map_variables:
            login_screen = True
            menu_screen = False
            fight_screen = False
        else:
            draw_bg()
            question_button = [None] * map_size

            # floor1_size = 0
            for i in range(map_size):
                # Question_button array fill, with datas
                if map_variables[i][3] == 1:
                    question_button[i] = button.Button(screen, map_variables[i][1], map_variables[i][2],
                                                       theoretical_question_img, 40, 40)
                elif map_variables[i][3] == 2:
                    question_button[i] = button.Button(screen, map_variables[i][1], map_variables[i][2],
                                                       practical_question_img, 40, 40)
                elif map_variables[i][3] == 3:
                    question_button[i] = button.Button(screen, map_variables[i][1], map_variables[i][2],
                                                       boss_question_img, 40, 40)
                elif map_variables[i][3] == 4:
                    question_button[i] = button.Button(screen, map_variables[i][1], map_variables[i][2],
                                                       extra_loot_question_img, 40, 40)
                if floor_completed == 0:
                    if i < map_size - last_floor_count[0][0]:
                        draw_line_c1(i)
                        draw_line_c2(i)
                    else:
                        draw_line_c2(i)
                    if map_variables[i][4] == floor_completed:
                        floor_indicator(i)
                        if question_button[i].draw():
                            question_type = int(map_variables[i][3])
                            fight_screen = True
                            login_screen = False
                            menu_screen = False
                            make_question = True
                            container = map_variables[i]
                    # elif map_variables[i][4] == (floor_completed - 1):
                    #     if question_button[i].draw():
                    #         nothing = True
                    else:
                        if question_button[i].draw():
                            nothing = True

                if floor_size > floor_completed > 0:
                    if floor_completed == 3:
                        print("itt")
                    if map_variables[i][4] > floor_completed:
                        if i < map_size - last_floor_count[0][0]:
                            draw_line_c1(i)
                        # else:
                        elif map_variables[i][4] > floor_completed + 1:
                            draw_line_c2(i)
                        if question_button[i].draw():
                            nothing = True
                    elif map_variables[i][4] == floor_completed:
                        if container[5] == map_variables[i][0] or map_variables[i][6] == container[0]:
                            draw_line_c1(i)
                            if map_variables[i][4] == floor_completed:
                                floor_indicator(i)
                                if question_button[i].draw():
                                    question_type = int(map_variables[i][3])
                                    fight_screen = True
                                    login_screen = False
                                    menu_screen = False
                                    make_question = True
                                    container = map_variables[i]
                            # elif map_variables[i][4] == (floor_completed - 1):
                            #     if question_button[i].draw():
                            #         nothing = True
                            else:
                                if question_button[i].draw():
                                    nothing = True

                if floor_completed == floor_size:
                    draw_congratulations()
                    if restart_button.draw():
                        mycursor.execute("SELECT score FROM students WHERE neptuncode = %s", (neptuncode_text,))
                        oldscore = mycursor.fetchall()
                        mycursor.execute("SELECT timer FROM floor_row_size WHERE start_time = %s", (start,))
                        timer = mycursor.fetchall()
                        newscore = ((1 - ((timer[0][0] / start) / 2)) * 1000) + oldscore[0][0]
                        mycursor.execute("UPDATE students SET score = %s WHERE neptuncode = %s",
                                         (int(newscore), neptuncode_text,))
                        db.commit()
                        login_screen = False
                        menu_screen = True
                        fight_screen = False
                        floor_completed = 0

    # Fight screen
    if fight_screen:
        draw_bg()
        pygame.display.set_caption('Battle')
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(bandit1.hp)
        if start_ticking:
            if pygame.time.get_ticks() - ticks > 1000:
                click_is_free = True
                ticks = pygame.time.get_ticks()
                print("ticks")
                if knight.hp > 0 and bandit1.hp > 0:
                    make_question = True
                start_ticking = False

        # select databases datas

        if make_question:
            mycursor.execute("SELECT question_type, question, answer1, answer2, answer3, answer4, good_answer_number "
                             "FROM Questions WHERE question_type = %s", (question_type,))
            questions = mycursor.fetchall()
            number_of_questions = 0
            for i in questions:
                # print(i)
                number_of_questions += 1

            rand_of_questions = random.randint(0, (number_of_questions - 1))

            result1 = False
            result2 = False
            result3 = False
            result4 = False
            question_type = questions[rand_of_questions][0]
            question = questions[rand_of_questions][1]
            answer1 = questions[rand_of_questions][2]
            answer2 = questions[rand_of_questions][3]
            answer3 = questions[rand_of_questions][4]
            answer4 = questions[rand_of_questions][5]
            good_answer_number = questions[rand_of_questions][6]
            if good_answer_number == 1:
                result1 = True
            elif good_answer_number == 2:
                result2 = True
            elif good_answer_number == 3:
                result3 = True
            elif good_answer_number == 4:
                result4 = True

            make_question = False

        # draw question
        draw_question_answers(question, screen_width / 2, 10, question_font)

        # draw answers
        draw_question_answers(answer1, screen_width * 0.150, screen_height - 30, answer_font)
        draw_question_answers(answer2, screen_width * 0.383, screen_height - 30, answer_font)
        draw_question_answers(answer3, screen_width * 0.616, screen_height - 30, answer_font)
        draw_question_answers(answer4, screen_width * 0.850, screen_height - 30, answer_font)

        # draw fighters
        knight.update()
        knight.draw()
        bandit1.update()
        bandit1.draw()

        # draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        # control player actions
        # reset action variables
        attack = False
        wrong_answer_attack = False
        target = None
        # make sure mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        posx, posy = pygame.mouse.get_pos()

        if click_is_free:
            # first answer
            if (screen_height - 45) < posy < (screen_height - 15) and 0 < posx < (
                    screen_width * 0.2665):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if clicked and result1 and bandit1.alive:
                    attack = True
                    target = bandit1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if clicked and result1 == False and bandit1.alive:
                    wrong_answer_attack = True
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
            # second answer
            if (screen_height - 45) < posy < (screen_height - 15) and (screen_width * 0.2665) < posx < (
                    screen_width * 0.4995):
                pygame.mouse.set_visible(False)
                screen.blit(sword_img, pos)
                if clicked and result2 and bandit1.alive:
                    attack = True
                    target = bandit1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if clicked and result2 == False and bandit1.alive:
                    wrong_answer_attack = True
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
            # third answer
            if (screen_height - 45) < posy < (screen_height - 15) and (screen_width * 0.4995) < posx < (
                    screen_width * 0.733):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if clicked and result3 and bandit1.alive:
                    attack = True
                    target = bandit1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if clicked and result3 == False and bandit1.alive:
                    wrong_answer_attack = True
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False

            # right bottom corner
            if (screen_height - 45) < posy < (screen_height - 15) and (screen_width * 0.733) < posx < screen_width:
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if clicked and result4 and bandit1.alive:
                    attack = True
                    target = bandit1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if clicked and result4 == False and bandit1.alive:
                    wrong_answer_attack = True
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False

        if game_over == 0:
            # player action
            if knight.alive:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        click_is_free = True
                        # look for player action
                        # attack
                        if attack and target != None:
                            print("attack is true and fight")
                            knight.attack(target)
                            # current_fighter += 1
                            action_cooldown = 0
                            click_is_free = False
                        if wrong_answer_attack:
                            current_fighter += 1
                            action_cooldown = 50
                            click_is_free = False
            else:
                game_over = -1

            # enemy action
            if current_fighter == 2:
                if bandit1.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        bandit1.attack(knight)
                        current_fighter += 1
                        action_cooldown = 0
                else:
                    current_fighter += 1

            # if all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        if knight.action == 1:
            draw_good_answer()
        elif bandit1.action == 1:
            draw_wrong_answer()
        # check if all bandits are dead
        alive_bandits = 0
        if bandit1.alive:
            alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1

        # check if game is over
        if game_over != 0:
            # if you won
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
                if restart_button.draw():
                    login_screen = False
                    menu_screen = True
                    fight_screen = False
                    floor_completed += 1
                    knight.reset()
                    bandit1.reset()
                    current_fighter = 1
                    action_cooldown = 0
                    game_over = 0
            # if you defeated
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
                if restart_button.draw():
                    knight.reset()
                    bandit1.reset()
                    current_fighter = 1
                    action_cooldown = 0
                    game_over = 0

    # Events (click, keydowns, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            if input_rect_neptuncode.collidepoint(event.pos):
                empty_neptuncode_text = False
                wrong_neptuncode_text = False
                used_neptuncode_text = False
                neptuncode_active = True
                no_map_added = False
            else:
                neptuncode_active = False
        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if neptuncode_active == True:
                if event.key == pygame.K_BACKSPACE:
                    neptuncode_text = neptuncode_text[0:-1]
                else:
                    if input_rect_neptuncode.w > (text_surface_neptuncode.get_width() + 16):
                        neptuncode_text += event.unicode

    pygame.display.update()

pygame.quit()
