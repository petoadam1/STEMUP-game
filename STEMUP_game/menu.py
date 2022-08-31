import pygame
import button
import random
import mysql.connector

# Pygame basics
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Database connect
db = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="challenge_me")
mycursor = db.cursor()

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (245, 66, 66)
MAXRED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game window
battle_bottom_panel = 160
battle_question_panel = 50
battle_screen_width = 800
battle_screen_height = 400 + battle_bottom_panel
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode(
    (battle_screen_width, battle_screen_height))  # erre egy jobb megoldást kell találjak majd
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Menu')

# Fonts
battle_font = pygame.font.Font('font/8-BIT WONDER.ttf', 16)
font = pygame.font.Font('font/8-BIT WONDER.ttf', 26)
smallerFont = pygame.font.Font('font/8-BIT WONDER.ttf', 22)
tinyFont = pygame.font.Font('font/8-BIT WONDER.ttf', 10)
normalTypeFont = pygame.font.SysFont('Times New Roman', 26)
#statFont = pygame.font.SysFont('Times New Roman', 10)
statFont = pygame.font.Font('font/8-BIT WONDER.ttf', 12)

# Images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
play_img = pygame.image.load('img/Icons/play-button.png').convert_alpha()
settings_img = pygame.image.load('img/Icons/settings-button.png').convert_alpha()
inventory_img = pygame.image.load('img/Icons/inventory-button.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
bp_img = pygame.image.load('img/Icons/inventory4.png').convert_alpha()
login_img = pygame.image.load('img/Icons/login_button_2.png').convert_alpha()
theoretical_question_img = pygame.image.load('img/Icons/theoretical_question_icon.png').convert_alpha()
boss_question_img = pygame.image.load('img/Icons/boss_question_icon.png').convert_alpha()
practical_question_img = pygame.image.load('img/Icons/practical_question_icon.png').convert_alpha()
extra_loot_question_img = pygame.image.load('img/Icons/extra_loot_question_icon.png').convert_alpha()
completed_level_img = pygame.image.load('img/Icons/completed_level.png').convert_alpha()
# Images to battle
panel_img = pygame.image.load('img/Icons/new_panel.png').convert_alpha()
questionpanel_img = pygame.image.load('img/Icons/question_panel.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()
# ITEM IMAGES


# Booleans
inventory_click = False
open_inventory = False
is_inventory_open = False
logged = False
sign_up = False
inmap = False
start_game = False
theoretical_game = False
boss_game = False
practical_game = False
extra_loot_game = False
itemsrand = 0

# bpresult = 0
# Map floors, levels
icons_size_x = 40
icons_size_y = 40
starter_pixel = 40
floor_size = 5
row_size = 3
rand = random.randint(0, 2)
rand2 = random.randint(3, 5)
rand3 = random.randint(6, 8)
rand4 = random.randint(9, 11)
rand5 = random.randint(12, 14)

the_map = [[[starter_pixel, (screen_height / 3) - (screen_height / 3 / 2) - (icons_size_x / 2)],  # row1
            [starter_pixel, (screen_height / 3 * 2) - (screen_height / 3 / 2) - (icons_size_x / 2)],  # row2
            [starter_pixel, screen_height - (screen_height / 3 / 2) - (icons_size_x / 2)]],  # row3
           # floor2
           [[(starter_pixel + (screen_width / 5)), (screen_height / 3) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            # row1
            [(starter_pixel + (screen_width / 5)),
             (screen_height / 3 * 2) - (screen_height / 3 / 2) - (icons_size_x / 2)],  # row2
            [(starter_pixel + (screen_width / 5)), screen_height - (screen_height / 3 / 2) - (icons_size_x / 2)]],
           # row3
           # floor3
           [[(starter_pixel + (screen_width / 5 * 2)),
             (screen_height / 3) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 2)),
             (screen_height / 3 * 2) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 2)), screen_height - (screen_height / 3 / 2) - (icons_size_x / 2)]],
           # floor4
           [[(starter_pixel + (screen_width / 5 * 3)),
             (screen_height / 3) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 3)),
             (screen_height / 3 * 2) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 3)), screen_height - (screen_height / 3 / 2) - (icons_size_x / 2)]],
           # floor5
           [[(starter_pixel + (screen_width / 5 * 4)),
             (screen_height / 3) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 4)),
             (screen_height / 3 * 2) - (screen_height / 3 / 2) - (icons_size_x / 2)],
            [(starter_pixel + (screen_width / 5 * 4)), screen_height - (screen_height / 3 / 2) - (icons_size_x / 2)]],
           ]

# Map csomópontok(the_map változó) feltöltése
question_button = [None] * (floor_size * row_size)
count = 0
for i in range(floor_size):
    for j in range(row_size):
        # print(i, j)
        random_icon = random.randint(0, 3)
        if random_icon == 0:
            question_button[count] = button.Button(screen, the_map[i][j][0], the_map[i][j][1],
                                                   theoretical_question_img, 40, 40)
        elif random_icon == 1:
            question_button[count] = button.Button(screen, the_map[i][j][0], the_map[i][j][1],
                                                   boss_question_img, 40, 40)
        elif random_icon == 2:
            question_button[count] = button.Button(screen, the_map[i][j][0], the_map[i][j][1],
                                                   practical_question_img, 40, 40)
        elif random_icon == 3:
            question_button[count] = button.Button(screen, the_map[i][j][0], the_map[i][j][1],
                                                   extra_loot_question_img, 40, 40)
        # question_button[count] = button.Button(screen, the_map[i][j][0], the_map[i][j][1], theoretical_question_img, 40, 40)
        count += 1

# Buttons
inventory_button = button.Button(screen, 10, 10, inventory_img, 60, 60)
play_button = button.Button(screen, screen_width / 2 - 100, screen_height * 0.33, play_img, 200, 50)


# Functions
def draw_bg():
    screen.blit(background_img, (0, 0))


def draw_bg_icons():
    # screen.blit(play_img, (screen_width / 2 - 100, screen_height * 0.33))
    screen.blit(settings_img, (screen_width / 2 - 100, screen_height * 0.50))


# Classes
class Account():
    def __init__(self, id, name, hp, power, defense):
        self.id = id
        self.name = name
        self.hp = hp
        self.power = power
        self.defense = defense


class User():
    def __init__(self, id, username, pswd):
        self.id = id
        self.username = username
        self.pswd = pswd


fighter = [None]
user = [None]


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_item(itemimg, itemx, itemy):
    asd1 = 'img/Items/'
    asd2 = asd1 + itemimg
    item = pygame.image.load(asd2).convert_alpha()
    screen.blit(item, (itemx, itemy))


bp_x = 20
bp_y = 30
bp_hero_part_x = 275
bp_height = 300
bp_inventory_slot_size_x = 48
bp_inventory_slot_size_y = 48
bp_inventory_start_x = 293
bp_inventory_start_y = bp_y + 26
bp_weapon_slot_x = bp_x + 18
bp_weapon_slot_y = bp_y + 37
bp_armor_slot_x = bp_x + 201
bp_armor_slot_y = bp_y + 92
bp_helmet_slot_x = bp_x + 201
bp_helmet_slot_y = bp_y + 37


# Inventory
def draw_bp():
    screen.blit(bp_img, (bp_x, bp_y))

    img = tinyFont.render(f'{fighter.name}', True, WHITE)
    imgrect = img.get_rect().center
    screen.blit(img, (bp_x + 133 - imgrect[0], bp_y + 195))

    draw_text(f'{fighter.power}', statFont, WHITE, bp_x + 44, bp_y + bp_height - 35)
    draw_text(f'{fighter.defense}', statFont, WHITE, bp_x + 124, bp_y + bp_height - 35)
    draw_text(f'{fighter.hp}', statFont, WHITE, bp_x + 206, bp_y + bp_height - 35)
    mycursor.execute(
        "select * from accounts inner join fighters on accounts.id = fighters.accountId inner join inventories on accountId = fighterId inner join Items on item = Items.id")
    bpresult = mycursor.fetchall()
    # counter1 = 0
    # hanyadik = 0
    itemx = bp_inventory_start_x
    itemy = bp_inventory_start_y
    asd = False
    inventory_counter = 0
    for k in bpresult:
        # print(k)
        # a selectből a user-nek az id-jáz jelöli
        if k[0] == user.id:
            itemimg = k[16]
            # print(itemx)
            # print(itemy)
            equipped = False
            inventory_counter += 1
            pygame.mouse.set_visible(True)
            posx, posy = pygame.mouse.get_pos()
            # k[10] a selectből az equipped sor ahol 1/0 lehet az érték
            if k[10] == 1:
                equipped = True
                # k[17] azt jelöli, hogy milyen típus, fegyver, páncél, fejfedő, stb
                if k[17] == "weapon":
                    draw_item(itemimg, bp_weapon_slot_x, bp_weapon_slot_y)
                    if posx > bp_weapon_slot_x and posx < (bp_weapon_slot_x+48) and posy > bp_weapon_slot_y and posy < (bp_weapon_slot_y+48):
                        if clicked:
                            # k[8] fighterId-t jelöl, a k[9] pedig az item-nek az id-t
                            mycursor.execute("UPDATE Inventories SET equipped = 0 WHERE fighterId = %s AND item = %s", (k[8], k[9]))
                            db.commit()
                            #name, hp, power, defense
                            fighter.hp -= k[15]
                            fighter.power -= k[13]
                            fighter.defense -= k[14]

                # k[17] azt jelöli, hogy milyen típus, fegyver, páncél, fejfedő, stb
                if k[17] == "armor":
                    draw_item(itemimg, bp_armor_slot_x, bp_armor_slot_y)
                    if posx > bp_armor_slot_x and posx < (
                            bp_armor_slot_x + 48) and posy > bp_armor_slot_y and posy < (bp_armor_slot_y + 48):
                        if clicked:
                            #k[8] fighterId-t jelöl, a k[9] pedig az item-nek az id-t
                            mycursor.execute("UPDATE Inventories SET equipped = 0 WHERE fighterId = %s AND item = %s", (k[8], k[9]))
                            db.commit()
                            fighter.hp -= k[15]
                            fighter.power -= k[13]
                            fighter.defense -= k[14]
                if k[17] == "helmet":
                    draw_item(itemimg, bp_helmet_slot_x, bp_helmet_slot_y)
                    if posx > bp_helmet_slot_x and posx < (
                            bp_helmet_slot_x + 48) and posy > bp_helmet_slot_y and posy < (bp_helmet_slot_y + 48):
                        if clicked:
                            #k[8] fighterId-t jelöl, a k[9] pedig az item-nek az id-t
                            mycursor.execute("UPDATE Inventories SET equipped = 0 WHERE fighterId = %s AND item = %s", (k[8], k[9]))
                            db.commit()
                            fighter.hp -= k[15]
                            fighter.power -= k[13]
                            fighter.defense -= k[14]
            else:
                if posx > itemx and posx < (itemx + 48) and posy > itemy and posy < (itemy + 48):
                    if clicked:
                        # print(k[8])
                        # k[8] fighterId-t jelöl, a k[9] pedig az item-nek az id-t
                        mycursor.execute("SELECT * FROM Inventories INNER JOIN Items ON item = Items.id WHERE fighterId = %s", (k[8],))
                        equippedresult = mycursor.fetchall()
                        there_is_equipped = False
                        for l in equippedresult:
                            # print(l)
                            # print(l[9])
                            #l[2] az equippedet jelöli, az l[9] pedig azt, hogy weapon, armor, vagy micsoda
                            if l[2] == 1 and l[9] == k[17]:
                                there_is_equipped = True
                                mycursor.execute(
                                    #az l[0] azt jelöli, hogy melyik fighterid, az l[1] pedig, hogy melyik item id
                                    "UPDATE Inventories SET equipped = 0 WHERE fighterId = %s AND item = %s",
                                    (l[0], l[1]))
                                db.commit()
                                fighter.hp -= l[7]
                                fighter.power -= l[5]
                                fighter.defense -= l[6]
                                print(l[7], l[5], l[6])
                                mycursor.execute(
                                    "UPDATE Inventories SET equipped = 1 WHERE fighterId = %s AND item = %s",
                                    (k[8], k[9]))
                                db.commit()
                                fighter.hp += k[15]
                                fighter.power += k[13]
                                fighter.defense += k[14]

                        if there_is_equipped == False:
                            mycursor.execute("UPDATE Inventories SET equipped = 1 WHERE fighterId = %s AND item = %s",(k[8], k[9]))
                            db.commit()
                        # print("equipped false rész lefut")
                            fighter.hp += k[15]
                            fighter.power += k[13]
                            fighter.defense += k[14]
                        # itemx -= bp_inventory_slot_size_x
                        # inventory_counter -= 1
                draw_item(itemimg, itemx, itemy)

            # itemx += bp_inventory_slot_size_x

            if inventory_counter == 10 and equipped == False:
                itemx = bp_inventory_start_x
                itemy = bp_inventory_start_y + bp_inventory_slot_size_y
            elif inventory_counter == 20 and equipped == False:
                itemx = bp_inventory_start_x
                itemy = bp_inventory_start_y + bp_inventory_slot_size_y*2
            elif inventory_counter == 30 and equipped == False:
                itemx = bp_inventory_start_x
                itemy = bp_inventory_start_y + bp_inventory_slot_size_y*3
            elif equipped == True:
                nothing = True
                inventory_counter -= 1
            else:
                itemx += bp_inventory_slot_size_x

            # itemy += 40
        # counter1 += 1


# LOGIN PART
# Booleans
username_active = False
pswd_active = False
wrong_un_pswd_text = False

base_font = pygame.font.Font(None, 32)
username_text = ''
pswd_text = ''
title = 'Login'
subtitle1 = 'Username'
subtitle2 = 'Password'
# too_many_character = 'Too many character'

# x, y = 200 helyen fogkirajzolódni, a 140 széles, 32 magas téglalap
# Rectangles, Colors
input_rect_username = pygame.Rect(300, 170, 200, 30)
input_rect_pswd = pygame.Rect(300, 220, 200, 30)
color_active = pygame.Color(237, 176, 71)
color_passive = pygame.Color(150, 100, 32)
username_color = color_passive
pswd_color = color_passive

# BATTLE

# questions
# question1 = 'Magyarul igent jelent'

# answers
# answer1 = 'Yes'
# answer2 = 'No'

# define game variables
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 75
attack = False
battle_clicked = False
game_over = 0
question_counter = 0
click_is_free = True
click_is_free_for_login = True
start_ticking = False
start_ticking_for_login = False
cooldown = 100
ticks = pygame.time.get_ticks()
floor_completed = 0


def do_click_free():
    click_is_free = True


# function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


# function for drawing panel
def draw_panel():
    # draw panel rectangle
    screen.blit(panel_img, (0, battle_screen_height - battle_bottom_panel))
    screen.blit(questionpanel_img, (0, battle_screen_height - 210))


# #show knight stats
# draw_text(f'{knight.name} HP: {knight.hp}', battle_font, red, 100, screen_height - bottom_panel + 10)
# #show name and health
# draw_text(f'{bandit1.name} HP: {bandit1.hp}', battle_font, red, 550, (screen_height - bottom_panel + 10) + 60)

def draw_good_answer():
    draw_text(f'Good answer', battle_font, GREEN, (battle_screen_width / 2 - 78),
              battle_screen_height - battle_bottom_panel - battle_question_panel - 20)


def draw_wrong_answer():
    draw_text(f'Wrong answer', battle_font, MAXRED, (battle_screen_width / 2 - 92),
              battle_screen_height - battle_bottom_panel - battle_question_panel - 20)

def add_random_item(question_type):
    print("add item")
    mycursor.execute("select count(*) from items")
    itemscount = mycursor.fetchall()
    itemscount_in_normal_int = itemscount[0][0]
    # print(itemscount[0][0])
    # print(question_type)
    if question_type == 1:
        itemsrand = random.randint(1, itemscount_in_normal_int)
        mycursor.execute("INSERT INTO Inventories (fighterId, item) VALUES (%s, %s)", (fighter.id, itemsrand,))
        db.commit()
    if question_type == 2:
        itemsrand = random.randint(1, itemscount_in_normal_int)
        mycursor.execute("INSERT INTO Inventories (fighterId, item) VALUES (%s, %s)", (fighter.id, itemsrand,))
        db.commit()
    if question_type == 3:
        itemsrand = random.randint(1, itemscount_in_normal_int)
        mycursor.execute("INSERT INTO Inventories (fighterId, item) VALUES (%s, %s)", (fighter.id, itemsrand,))
        db.commit()
            # itemsrand = random.randint(1, itemscount_in_normal_int)
            # mycursor.execute("INSERT INTO Inventories (fighterId, item) VALUES (%s, %s)", (fighter.id, itemsrand,))
            # db.commit()
    if question_type == 4:
        itemsrand = random.randint(1, itemscount_in_normal_int)
        mycursor.execute("INSERT INTO Inventories (fighterId, item) VALUES (%s, %s)", (fighter.id, itemsrand,))
        db.commit()

        # mycursor.execute("SELECT img FROM Items WHERE id = %s", (itemsrand,))
        # itemimg = mycursor.fetchall()
        # draw_item(itemimg[0][0], 150, 150)



# fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, power, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = power
        self.defense = defense
        #self.start_potions = potions
        #self.potions = potions
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


class HealthBar():
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
knight = Fighter(250, 315, 'Knight', knighthp, 10, 0)
bandit1 = Fighter(545, 315, 'Bandit', bandithp, 6, 0)

knight_health_bar = HealthBar(26, battle_screen_height - 142, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(754, battle_screen_height - 142, bandit1.hp, bandit1.max_hp)

# create buttons
# potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)
# start_game = True
make_question = True
question_type = 1
able_to_give_item = False

# # answer_img1 = Answer
# answer_text1 = battle_font.render(answer1, True, WHITE)
# answer_text2 = battle_font.render(answer2, True, WHITE)
# answer1_button = button.Button(screen, battle_screen_width * 0.25, battle_screen_height - 100, answer_text1, 40, 30)
# answer2_button = button.Button(screen, battle_screen_width * 0.7, battle_screen_height - 100, answer_text2, 40, 30)
# inmap = True

run = True
while run:

    clock.tick(fps)

    # Login interface
    if logged == False:
        if start_game == False and inmap == False and sign_up == False:
            draw_bg()
            draw_text(title, font, WHITE, 342, screen_height / 4)
            draw_text(subtitle1, tinyFont, WHITE, 302, 158)
            draw_text(subtitle2, tinyFont, WHITE, 302, 208)
            draw_text('Sign up', tinyFont, WHITE, 302, 270)
            pygame.mouse.set_visible(True)
            posx, posy = pygame.mouse.get_pos()
            pygame.draw.rect(screen, username_color,
                             input_rect_username)  # , 2) vel hozzá lehet adni, hogy csak egy x vastagságú kerete legyen
            pygame.draw.rect(screen, pswd_color, input_rect_pswd)
            login_button = button.Button(screen, 420, 270, login_img, 80, 20)

            if start_ticking_for_login == True:
                if pygame.time.get_ticks() - ticks > 70:
                    click_is_free_for_login = True
                    ticks = pygame.time.get_ticks()
                    # print("ticks")
                    start_ticking_for_login = False

            if click_is_free_for_login:
                if posx > 302 and posx < 340 and posy > 270 and posy < 290:
                    if clicked:
                        click_is_free_for_login = False
                        start_ticking_for_login = True
                        ticks = pygame.time.get_ticks()
                        sign_up = True


            if login_button.draw():

                # un_pswd_databaseformat = (username_text, pswd_text)

                mycursor.execute("SELECT id, username, pswd FROM Accounts")
                result = mycursor.fetchall()
                for i in result:
                    # print(i[1])
                    if i[1] == username_text and i[2] == pswd_text:
                        # if i == un_pswd_databaseformat:
                        # for k in resultid:
                        user = User(i[0], i[1], i[2])
                        mycursor.execute("SELECT * FROM Accounts INNER JOIN Fighters ON Accounts.id = Fighters.accountId WHERE Accounts.id = %s", (i[0],))
                        result2 = mycursor.fetchall()
                        mycursor.execute(
                            "select Items.power, Items.defense, Items.hp from accounts inner join fighters on accounts.id = fighters.accountId inner join inventories on accountId = fighterId inner join Items on item = Items.id WHERE Accounts.id = %s AND equipped = 1;",
                            (i[0],))
                        itemStats = mycursor.fetchall()
                        hp = 0
                        power = 0
                        defense = 0
                        for j in itemStats:
                            print()
                            hp += j[2]
                            power += j[0]
                            defense += j[1]

                        fighter = Account(result2[0][0], result2[0][4], result2[0][5]+hp, result2[0][6]+power, result2[0][7]+defense)
                        knight = Fighter(250, 315, 'Knight', result2[0][5]+hp, result2[0][6]+power, result2[0][7]+defense)
                        logged = True
                        # print(user.id)
                        # print(user.username)
                        # print(user.pswd)
                if logged == False:
                    wrong_un_pswd_text = True

            if username_active == False and pswd_active == False:
                if wrong_un_pswd_text == True:
                    draw_text('Wrong username or password', tinyFont, RED, 270, 255)

            if username_active:
                username_color = color_active
            else:
                username_color = color_passive

            if pswd_active:
                pswd_color = color_active
            else:
                pswd_color = color_passive

            text_surface_username = base_font.render(username_text, True, (0, 0, 0))
            screen.blit(text_surface_username, (input_rect_username.x + 5, input_rect_username.y + 5))
            text_surface_pswd = base_font.render(pswd_text, True, (0, 0, 0))
            screen.blit(text_surface_pswd, (input_rect_pswd.x + 5, input_rect_pswd.y + 5))

            # ez felelős azért, hogy akkora legyen a téglalap szélessége, mint a szöveg
            # input_rect_username.w = max(200, text_surface.get_width() + 10)

    #Sign up interface
    if sign_up == True:
        if inmap == False and start_game == False and logged == False:
            draw_bg()
            draw_text('Sign up', font, WHITE, 325, screen_height / 4)
            draw_text(subtitle1, tinyFont, WHITE, 302, 158)
            draw_text(subtitle2, tinyFont, WHITE, 302, 208)
            draw_text('Sign in', tinyFont, WHITE, 302, 270)
            pygame.mouse.set_visible(True)
            posx, posy = pygame.mouse.get_pos()
            pygame.draw.rect(screen, username_color,
                             input_rect_username)  # , 2) vel hozzá lehet adni, hogy csak egy x vastagságú kerete legyen
            pygame.draw.rect(screen, pswd_color, input_rect_pswd)
            login_button = button.Button(screen, 420, 270, login_img, 80, 20)

            if start_ticking_for_login == True:
                if pygame.time.get_ticks() - ticks > 70:
                    click_is_free_for_login = True
                    ticks = pygame.time.get_ticks()
                    # print("ticks")
                    start_ticking_for_login = False

            if click_is_free_for_login == True:
                if posx > 302 and posx < 340 and posy > 270 and posy < 290:
                    if clicked:
                        click_is_free_for_login = False
                        start_ticking_for_login = True
                        ticks = pygame.time.get_ticks()
                        sign_up = False

            if login_button.draw():
                nothing = True

    # Menu interface
    if inmap == False and start_game == False:
        if logged == True:
            # print("menu")
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.mouse.set_visible(True)
            posx, posy = pygame.mouse.get_pos()
            draw_bg()
            # x = 20
            # y = 30
            # screen.fill(WHITE)
            draw_bg_icons()
            draw_text('Sign out', tinyFont, WHITE, screen_width - 80, screen_height - 20)

            if click_is_free:
                if posx > screen_width - 83 and posx < screen_width - 5 and posy > screen_height - 23 and posy < screen_height - 5:
                    if clicked:
                        logged = False
                        username_text = ''
                        pswd_text = ''
                        open_inventory = False

            if start_ticking == True:
                if pygame.time.get_ticks() - ticks > 50:
                    click_is_free = True
                    ticks = pygame.time.get_ticks()
                    # print("ticks")
                    start_ticking = False

            if play_button.draw() and open_inventory == False:
                # ide bekell rakni, majd a random számokat, hogy újragenerálja
                # print("ez nem jo1")
                knight = Fighter(250, 315, 'Knight', fighter.hp, fighter.power, fighter.defense)
                inmap = True
                start_ticking = False
                click_is_free = False

            if inventory_button.draw():
                if click_is_free:
                    if open_inventory == False:
                        ticks = pygame.time.get_ticks()
                        start_ticking = True
                        click_is_free = False
                        open_inventory = True
                        # is_inventory_open = True

            if open_inventory == True:
                # print("open")
                draw_bp()
                # draw_text(fighter.name, font, WHITE, 228, 135)
                # draw_text(f'{fighter.hp}', smallerFont, BLACK, 170, 190)
                # draw_text(f'{fighter.power}', smallerFont, BLACK, 170, 210)
                # draw_text(f'{fighter.defense}', smallerFont, BLACK, 170, 230)

            if click_is_free:
                if open_inventory == True:
                    if posx > 10 and posx < 72 and posy > 10 and posy < 72:
                        if clicked:
                            # print("close")
                            # is_inventory_open = False
                            open_inventory = False

    # Map interface
    if inmap == True and start_game == False:
        screen = pygame.display.set_mode((screen_width, screen_height))
        draw_bg()
        draw_text('Back to menu', tinyFont, WHITE, screen_width - 125, screen_height - 20)

        able_to_give_item = True

        pygame.mouse.set_visible(True)
        posx, posy = pygame.mouse.get_pos()

        if posx > screen_width - 130 and posx < screen_width - 5 and posy > screen_height - 23 and posy < screen_height - 5:
            if clicked:
                print("asd")
                inmap = False
                logged = True


        for h in range(floor_size * row_size):

            if h != rand and h != rand2 and h != rand3 and h != rand4 and h != rand5:

                startX = question_button[h].x + 8
                startY = question_button[h].y + 8
                egesz = h // 3
                # print(egesz)
                maradek = h % 3
                # print(maradek)
                if h < ((floor_size * row_size) - 3):
                    if maradek == 2:
                        if h + 1 != rand and h + 1 != rand2 and h + 1 != rand3 and h + 1 != rand4 and h + 1 != rand5:
                            endX = question_button[h + 1].x + 8
                            endY = question_button[h + 1].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 2 != rand and h + 2 != rand2 and h + 2 != rand3 and h + 2 != rand4 and h + 2 != rand5:
                            endX = question_button[h + 2].x + 8
                            endY = question_button[h + 2].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 3 != rand and h + 3 != rand2 and h + 3 != rand3 and h + 3 != rand4 and h + 3 != rand5:
                            endX = question_button[h + 3].x + 8
                            endY = question_button[h + 3].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                    if maradek == 1:
                        if h + 2 != rand and h + 2 != rand2 and h + 2 != rand3 and h + 2 != rand4 and h + 2 != rand5:
                            endX = question_button[h + 2].x + 8
                            endY = question_button[h + 2].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 3 != rand and h + 3 != rand2 and h + 3 != rand3 and h + 3 != rand4 and h + 3 != rand5:
                            endX = question_button[h + 3].x + 8
                            endY = question_button[h + 3].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 4 != rand and h + 4 != rand2 and h + 4 != rand3 and h + 4 != rand4 and h + 4 != rand5:
                            endX = question_button[h + 4].x + 8
                            endY = question_button[h + 4].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                    if maradek == 0:
                        if h + 3 != rand and h + 3 != rand2 and h + 3 != rand3 and h + 3 != rand4 and h + 3 != rand5:
                            endX = question_button[h + 3].x + 8
                            endY = question_button[h + 3].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 4 != rand and h + 4 != rand2 and h + 4 != rand3 and h + 4 != rand4 and h + 4 != rand5:
                            endX = question_button[h + 4].x + 8
                            endY = question_button[h + 4].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                        if h + 5 != rand and h + 5 != rand2 and h + 5 != rand3 and h + 5 != rand4 and h + 5 != rand5:
                            endX = question_button[h + 5].x + 8
                            endY = question_button[h + 5].y + 8
                            pygame.draw.line(screen, WHITE, (startX, startY), (endX, endY))
                if floor_completed == 0:
                    if h < 3:
                        if question_button[h].draw():
                            make_question = True
                            if question_button[h].pureimage == theoretical_question_img:
                                question_type = 1
                                theoretical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == boss_question_img:
                                question_type = 3
                                boss_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == practical_question_img:
                                question_type = 2
                                practical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == extra_loot_question_img:
                                question_type = 4
                                extra_loot_game = True
                                start_game = True
                                inmap = False
                    if h >= 3:
                        if question_button[h].draw():
                            nothing = True
                if floor_completed == 1:
                    if h < 3:
                        x = question_button[h].x
                        y = question_button[h].y
                        screen.blit(completed_level_img, (x, y))
                    if h >= 3 and h < 6:
                        if question_button[h].draw():
                            make_question = True
                            if question_button[h].pureimage == theoretical_question_img:
                                question_type = 1
                                theoretical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == boss_question_img:
                                question_type = 3
                                boss_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == practical_question_img:
                                question_type = 2
                                practical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == extra_loot_question_img:
                                question_type = 4
                                extra_loot_game = True
                                start_game = True
                                inmap = False
                    if h >= 6:
                        if question_button[h].draw():
                            nothing = True
                if floor_completed == 2:
                    if h < 6:
                        x = question_button[h].x
                        y = question_button[h].y
                        screen.blit(completed_level_img, (x, y))
                    if h >= 6 and h < 9:
                        if question_button[h].draw():
                            make_question = True
                            if question_button[h].pureimage == theoretical_question_img:
                                question_type = 1
                                theoretical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == boss_question_img:
                                question_type = 3
                                boss_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == practical_question_img:
                                question_type = 2
                                practical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == extra_loot_question_img:
                                question_type = 4
                                extra_loot_game = True
                                start_game = True
                                inmap = False
                    if h >= 9:
                        if question_button[h].draw():
                            nothing = True
                if floor_completed == 3:
                    if h < 9:
                        x = question_button[h].x
                        y = question_button[h].y
                        screen.blit(completed_level_img, (x, y))
                    if h >= 9 and h < 12:
                        if question_button[h].draw():
                            make_question = True
                            if question_button[h].pureimage == theoretical_question_img:
                                question_type = 1
                                theoretical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == boss_question_img:
                                question_type = 3
                                boss_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == practical_question_img:
                                question_type = 2
                                practical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == extra_loot_question_img:
                                question_type = 14
                                extra_loot_game = True
                                start_game = True
                                inmap = False
                    if h >= 12:
                        if question_button[h].draw():
                            nothing = True
                if floor_completed == 4:
                    if h < 12:
                        x = question_button[h].x
                        y = question_button[h].y
                        screen.blit(completed_level_img, (x, y))
                    if h >= 12 and h < 15:
                        if question_button[h].draw():
                            make_question = True
                            if question_button[h].pureimage == theoretical_question_img:
                                question_type = 1
                                theoretical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == boss_question_img:
                                question_type = 3
                                boss_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == practical_question_img:
                                question_type = 2
                                practical_game = True
                                start_game = True
                                inmap = False
                            if question_button[h].pureimage == extra_loot_question_img:
                                question_type = 4
                                extra_loot_game = True
                                start_game = True
                                inmap = False
                        # if h >= 12:
                        #     if question_button[h].draw():
                        #         nothing = True
                    # if h >= 6:
                    #     if question_button[h].draw():
                    #         nothing = True



    # Fight interface
    if start_game == True:

        screen = pygame.display.set_mode((battle_screen_width, battle_screen_height))
        draw_bg()
        pygame.display.set_caption('Battle')
        # clock.tick(fps)
        # draw panel
        draw_panel()
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(bandit1.hp)
        # question_type = [None]

        if start_ticking == True:
            if pygame.time.get_ticks() - ticks > 1000:
                click_is_free = True
                ticks = pygame.time.get_ticks()
                print("ticks")
                if knight.hp > 0 and bandit1.hp > 0:
                    make_question = True
                start_ticking = False

        # select databases datas

        # print(result[0][0])
        if make_question == True:
            mycursor.execute(
                "SELECT question_type, question, answer1, answer2, answer3, answer4, good_answer_number FROM Questions WHERE question_type = %s", (question_type,))
            questions = mycursor.fetchall()
            # print(questions)
            count = 0
            # print(questions)
            for i in questions:
                # print(i)
                count += 1
            questionrand = random.randint(0, (count-1))
            # print(count)
            # print(questionrand)
            # mycursor.execute(
            #     "SELECT question_type, question, answer1, answer2, answer3, answer4, good_answer_number FROM Questions WHERE id = %s", (questionrand,))
            # filteredquestions = mycursor.fetchall()
            # print(filteredquestions)

            result1 = False
            result2 = False
            result3 = False
            result4 = False
            question_type = questions[questionrand][0]
            question = questions[questionrand][1]
            answer1 = questions[questionrand][2]
            answer2 = questions[questionrand][3]
            answer3 = questions[questionrand][4]
            answer4 = questions[questionrand][5]
            good_answer_number = questions[questionrand][6]
            if good_answer_number == 1:
                result1 = True
            elif good_answer_number == 2:
                result2 = True
            elif good_answer_number == 3:
                result3 = True
            elif good_answer_number == 4:
                result4 = True

            make_question = False

        # print(count)

        # draw question, answers
        draw_text(question, normalTypeFont, BLACK, 10, (battle_screen_height - 200))
        draw_text(answer1, normalTypeFont, WHITE, battle_screen_width * 0.25, battle_screen_height - 135)
        draw_text(answer2, normalTypeFont, WHITE, battle_screen_width * 0.7, battle_screen_height - 135)
        draw_text(answer3, normalTypeFont, WHITE, battle_screen_width * 0.25, battle_screen_height - 50)
        draw_text(answer4, normalTypeFont, WHITE, battle_screen_width * 0.7, battle_screen_height - 50)

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
            # left top corner
            if posy > (battle_screen_height - battle_bottom_panel) and \
                    posy < (battle_screen_height - (battle_bottom_panel / 2) - 10) and posx > 80 and posx < (
                    battle_screen_width / 2 - 10):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if battle_clicked == True and result1 == True and bandit1.alive == True:
                    attack = True
                    target = bandit1
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                    print("attack")
                if battle_clicked == True and result1 == False and bandit1.alive == True:
                    wrong_answer_attack = True
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
            # right top corner
            if posy > (battle_screen_height - battle_bottom_panel) and \
                    posy < (battle_screen_height - (battle_bottom_panel / 2) - 10) and posx > (
                    battle_screen_width / 2 + 10) and posx < (battle_screen_width - 80):
                pygame.mouse.set_visible(False)
                screen.blit(sword_img, pos)
                if battle_clicked == True and result2 == True and bandit1.alive == True:
                    attack = True
                    target = bandit1
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if battle_clicked == True and result2 == False and bandit1.alive == True:
                    wrong_answer_attack = True
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
            # left bottom corner
            if posy > (battle_screen_height - (battle_bottom_panel / 2) + 10) and posy < (
                    battle_screen_height - 10) and posx > 80 and posx < (battle_screen_width / 2 - 10):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if battle_clicked == True and result3 == True and bandit1.alive == True:
                    attack = True
                    target = bandit1
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if battle_clicked == True and result3 == False and bandit1.alive == True:
                    wrong_answer_attack = True
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False

            # right bottom corner
            if posy > (battle_screen_height - (battle_bottom_panel / 2) + 10) and posy < (battle_screen_height - 10) \
                    and posx > (battle_screen_width / 2 + 10) and posx < (battle_screen_width - 80):
                # hide mouse
                pygame.mouse.set_visible(False)
                # show sword in place of mouse cursor
                screen.blit(sword_img, pos)
                if battle_clicked == True and result4 == True and bandit1.alive == True:
                    attack = True
                    target = bandit1
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False
                if battle_clicked == True and result4 == False and bandit1.alive == True:
                    wrong_answer_attack = True
                    # question_counter = question_counter + 1
                    ticks = pygame.time.get_ticks()
                    start_ticking = True
                    click_is_free = False

        if game_over == 0:
            # player action
            if knight.alive == True:

                if current_fighter == 1:

                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        click_is_free = True
                        # look for player action
                        # attack
                        if attack == True and target != None:
                            print("attack is true and fight")
                            knight.attack(target)
                            # current_fighter += 1
                            action_cooldown = 0
                            click_is_free = False
                        if wrong_answer_attack == True:
                            current_fighter += 1
                            action_cooldown = 50
                            click_is_free = False
            else:
                game_over = -1

            # enemy action
            if current_fighter == 2:
                if bandit1.alive == True:
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
        if bandit1.alive == True:
            alive_bandits += 1
        if alive_bandits == 0:
            game_over = 1

        # check if game is over
        if game_over != 0:
            #if you won
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
                if able_to_give_item == True:
                    add_random_item(question_type)
                    able_to_give_item = False
                # if able_to_give_item == False:
                #     add_random_item(question_type, 0)
                if restart_button.draw():
                    start_game = False
                    inmap = True
                    logged = True
                    play_button.action = False
                    floor_completed += 1
                    knight.reset()
                    bandit1.reset()
                    current_fighter = 1
                    action_cooldown = 0
                    game_over = 0
                    question_counter = 0
            # if you defeated
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
                if restart_button.draw():
                    knight.reset()
                    bandit1.reset()
                    current_fighter = 1
                    action_cooldown = 0
                    game_over = 0
                    question_counter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                battle_clicked = True
            else:
                battle_clicked = False

        pygame.display.update()

        if theoretical_game == True:
            nothing = True
        if boss_game == True:
            nothing = True
        if practical_game == True:
            nothing = True

    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
            # Login part
            if input_rect_username.collidepoint(event.pos):
                username_active = True
            else:
                wrong_un_pswd_text = False
                username_active = False
            if input_rect_pswd.collidepoint(event.pos):
                pswd_active = True
            else:
                wrong_un_pswd_text = False
                pswd_active = False
        else:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if username_active == True:
                if event.key == pygame.K_BACKSPACE:
                    username_text = username_text[0:-1]
                else:
                    if input_rect_username.w > (text_surface_username.get_width() + 16):
                        username_text += event.unicode

            if pswd_active == True:
                if event.key == pygame.K_BACKSPACE:
                    pswd_text = pswd_text[0:-1]
                else:
                    if input_rect_pswd.w > (text_surface_pswd.get_width() + 16):
                        pswd_text += event.unicode

    pygame.display.update()

pygame.quit()
