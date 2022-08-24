import pygame
import random
import button
import time

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 160
question_panel = 50
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')

#questions
question1 = 'Magyarul igent jelent'

#answers
answer1 = 'Yes'
answer2 = 'No'

#define game variables
current_fighter = 1
total_fighters = 2
action_cooldown = 0
action_wait_time = 75
attack = False
potion = False
potion_effect = 15
battle_clicked = False
game_over = 0


#define fonts
font = pygame.font.Font('font/8-BIT WONDER.ttf', 16)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

#load images
#background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
panel_img = pygame.image.load('img/Icons/new_panel.png').convert_alpha()
questionpanel_img = pygame.image.load('img/Icons/question_panel.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# #jó és rossz válasz
# good_answer = (f'Jó válasz', font, green, 100, 100)
# wrong_answer = (f'Rossz válasz', font, green, 100, 100)

#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))

#function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	screen.blit(questionpanel_img, (0, screen_height - 210))
	# #show knight stats
	# draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	# #show name and health
	# draw_text(f'{bandit1.name} HP: {bandit1.hp}', font, red, 550, (screen_height - bottom_panel + 10) + 60)

def draw_good_answer():
	draw_text(f'Good answer', font, green, (screen_width/2-78), screen_height-bottom_panel-question_panel-20)

def draw_wrong_answer():
	draw_text(f'Wrong answer', font, red, (screen_width / 2 - 92), screen_height-bottom_panel-question_panel-20)
#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()


	
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def reset (self):
		self.alive = True
		self.potions = self.start_potions
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
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, green, (self.x, self.y, 20, 120))
		pygame.draw.rect(screen, red, (self.x, self.y, 20, 120 - (120 * ratio)))
		#pygame.draw.rect(screen, green, (self.x, self.y + (120 - (120 * ratio)), 20, 120 * ratio))



class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()



damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 260, 'Knight', 50, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)

knight_health_bar = HealthBar(26, screen_height - 142, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(754, screen_height - 142, bandit1.hp, bandit1.max_hp)

#create buttons
# potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

# answer_img1 = Answer
answer_text1 = font.render(answer1, True, white)
answer_text2 = font.render(answer2, True, white)
answer1_button = button.Button(screen, screen_width * 0.25, screen_height - 100, answer_text1, 40, 30)
answer2_button = button.Button(screen, screen_width * 0.7, screen_height - 100, answer_text2, 40, 30)

# imgvalue = pygame.image.load(f'img/Icons/question_panel.png')
# imgvalue = pygame.transform.scale(imgvalue, ((imgvalue.get_width()-10), imgvalue.get_height()))
# left_answer_button = imgvalue.get_rect()
# left_answer_button.center = (0, screen_height-177)
#
# imgvalue2 = pygame.transform.scale(imgvalue, ((imgvalue.get_width()-10), imgvalue.get_height()))
# right_answer_button = imgvalue2.get_rect()
# right_answer_button.center = (800, screen_height-177)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)


	# draw question
	draw_text(question1, font, black, 185, (screen_height-195))
	answer1 = False
	answer2 = False
	result1 = True
	result2 = False
	if answer1_button.draw():
		answer1 = True
	if answer2_button.draw():
		answer2 = True
	#answer2_button.draw()
	#draw fighters
	knight.update()
	knight.draw()
	bandit1.update()
	bandit1.draw()

	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)

	#control player actions
	#reset action variables
	attack = False
	wrong_answer_attack = False
	#draw_good_answer = False
	#draw_wrong_answer = False
	#current_time = 0
	potion = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	posx, posy = pygame.mouse.get_pos()
	if posy > (screen_height-bottom_panel) and \
			posy < (screen_height-10) and posx > 80 and posx < (screen_width/2-10):
		#hide mouse
		pygame.mouse.set_visible(False)
		#show sword in place of mouse cursor
		screen.blit(sword_img, pos)
		if battle_clicked == True and result1 == True and bandit1.alive == True:
			attack = True
			target = bandit1
			#draw_good_answer()
		if battle_clicked == True and result1 == False and bandit1.alive == True:
			#draw_text(f'Rossz válasz', font, red, 100, 100)
			wrong_answer_attack = True

	if posy > (screen_height-bottom_panel) and \
			posy < (screen_height-10) and posx > (screen_width/2+10) and posx < (screen_width - 80):
		pygame.mouse.set_visible(False)
		screen.blit(sword_img, pos)
		if battle_clicked == True and result2 == True and bandit1.alive == True:
			attack = True
			target = bandit1
			#draw_good_answer()
		if battle_clicked == True and result2 == False and bandit1.alive == True:
			# draw_text(f'Rossz válasz', font, red, 100, 100)
			wrong_answer_attack = True



	# if potion_button.draw():
	# 	potion = True
	# #show number of potions remaining
	# draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

	# if draw_good_answer == True:
	# 	current_time = pygame.time.get_ticks()
	# 	draw_text(f'Jó válasz', font, green, 100, 100)
	# 	# if current_time > 15000:
	# 	# 	draw_good_answer = False
	# 	# 	#break

	if game_over == 0:
		#player action
		if knight.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action
					#attack
					if attack == True and target != None:
						knight.attack(target)
						#current_fighter += 1
						action_cooldown = 0
					if wrong_answer_attack == True:
						current_fighter += 1
						action_cooldown = 50

					# #potion
					# if potion == True:
					# 	if knight.potions > 0:
					# 		#check if the potion would heal the player beyond max health
					# 		if knight.max_hp - knight.hp > potion_effect:
					# 			heal_amount = potion_effect
					# 		else:
					# 			heal_amount = knight.max_hp - knight.hp
					# 		knight.hp += heal_amount
					# 		knight.potions -= 1
					# 		damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
					# 		damage_text_group.add(damage_text)
					# 		current_fighter += 1
					# 		action_cooldown = 0
		else:
			game_over = -1



		#enemy action
		if current_fighter == 2:
			if bandit1.alive == True:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#check if bandit needs to heal first
					# if (bandit1.hp / bandit1.max_hp) < 0.5 and bandit1.potions > 0:
					# 	#check if the potion would heal the bandit beyond max health
					# 	if bandit1.max_hp - bandit1.hp > potion_effect:
					# 		heal_amount = potion_effect
					# 	else:
					# 		heal_amount = bandit1.max_hp - bandit1.hp
					# 	bandit1.hp += heal_amount
					# 	bandit1.potions -= 1
					# 	damage_text = DamageText(bandit1.rect.centerx, bandit1.rect.y, str(heal_amount), green)
					# 	damage_text_group.add(damage_text)
					# 	current_fighter += 1
					# 	action_cooldown = 0
					# #attack
					# else:
					bandit1.attack(knight)
					current_fighter += 1
					action_cooldown = 0
			else:
				current_fighter += 1

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1

	if knight.action == 1:
		draw_good_answer()
	elif bandit1.action == 1:
		draw_wrong_answer()
	#check if all bandits are dead
	alive_bandits = 0
	if bandit1.alive == True:
		alive_bandits += 1
	if alive_bandits == 0:
		game_over = 1


	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			knight.reset()
			bandit1.reset()
			current_fighter = 1
			action_cooldown = 0
			game_over = 0



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			battle_clicked = True
		else:
			battle_clicked = False

	pygame.display.update()

pygame.quit()

