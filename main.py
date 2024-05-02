#AUTHOR: LIAM LEAHY
#ANIMATION/SPRITE SHEET CODE SOURCE: @CodingWithRuss on YouTube

#IMPORT STATEMENTS
import pygame, sys, os, spritesheet, random

#INITIALIZATION STATEMENT
pygame.init()

#CONSTANTS
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 250
BACKGROUND_COLOR = (0, 105, 148)

#GAME SET UP
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dodge the Nautilus')
clock = pygame.time.Clock()
score = 0
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player_alive = True

#BACKGROUND
sand_rect = pygame.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)


#SPRITE SHEETS
sprite_sheet_image = pygame.image.load('trilobite_sprite_sheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
ai_sprite_sheet_image = pygame.image.load('nautilius_sprite_sheet.png').convert_alpha()
ai_sprite_sheet = spritesheet.SpriteSheet(ai_sprite_sheet_image)

#IMAGES
seaweed_image = pygame.image.load('seaweed.png').convert_alpha()
new_seaweed_image = pygame.transform.scale(seaweed_image, (30 * 3, 30 * 3))
background_seaweed_image = pygame.transform.scale(seaweed_image, (30 , 30))
background_seaweed_image.set_colorkey((0, 0, 0))
background_seaweed_image.set_alpha(122)


#SPRITE ANIMATION
animation_list = []
animation_steps = [3, 3]
last_update = pygame.time.get_ticks()
animation_cooldown = 250
action = 0
frame = 0
step_counter = 0

ai_animation_list = []
ai_animation_steps = [4]
ai_last_update = pygame.time.get_ticks()
#ai_animation_cooldown = 300 #moved to enemy class for periodic update
ai_action = 0
ai_frame = 0
ai_step_counter = 0

#EXTRACTING/STORING SPRITE SHEET FRAMES
#FOR PLAYER
for animation in animation_steps:
	temp_img_list = []
	for _ in range(animation):
		temp_img_list.append(sprite_sheet.get_image(step_counter, 52, 25, 2, BACKGROUND_COLOR))
		step_counter += 1
	animation_list.append(temp_img_list)
#FOR ENEMY
for animation in ai_animation_steps:
	temp_img_list = []
	for _ in range(animation):
		temp_img_list.append(ai_sprite_sheet.get_image(ai_step_counter, 82, 40, 2, BACKGROUND_COLOR))
		ai_step_counter += 1
	ai_animation_list.append(temp_img_list)

############################## MODEL ##############################

#PLAYER SPRITE CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.action = 0
        self.frame = 0
        self.flip = False
        self.xpos = 0
        self.ypos = 0
        self.rect = pygame.Rect(self.xpos, self.ypos, 104, 50)
        self.hitbox = pygame.Rect(self.xpos, self.ypos, 99, 40)
        self.hitbox.center = self.rect.center
        self.speed = 3
    
    #KEY PRESSED DETECTION
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.xpos < SCREEN_WIDTH - 104:
            self.rect.move_ip(self.speed, 0)
            self.xpos = self.rect.x
        if keys[pygame.K_LEFT] and self.xpos > 0:
            self.rect.move_ip(-self.speed, 0)
            self.xpos = self.rect.x
        if keys[pygame.K_DOWN] and self.ypos < SCREEN_HEIGHT - 50 - 11:
            self.rect.move_ip(0, self.speed)
            self.ypos = self.rect.y
        if keys[pygame.K_UP] and self.ypos > 0:
            self.rect.move_ip(0, -self.speed)
            self.ypos = self.rect.y

    def draw(self, surface):
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.rect)
        self.hitbox.center = self.rect.center
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.hitbox)

#ENEMY SPRITE CLASS
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = SCREEN_WIDTH + 90
        self.ypos = SCREEN_HEIGHT / 2
        self.rect = pygame.Rect(self.xpos, self.ypos, 164, 80)
        self.hitbox = pygame.Rect(self.xpos, self.ypos, 149, 65)
        self.hitbox.center = self.rect.center
        self.speed = 1
        self.ai_animation_cooldown = 300

    def move(self):
        if(self.rect.x < -170):
            self.rect.x = SCREEN_WIDTH + 90
            self.rect.y = random.randint(0, (SCREEN_HEIGHT - 80 - 11))
        self.rect.move_ip(-self.speed, 0)
        self.xpos = self.rect.x
        self.ypos = self.rect.y

    def draw(self, surface):
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.rect)
        self.hitbox.center = self.rect.center
        pygame.draw.rect(surface, BACKGROUND_COLOR, self.hitbox)

#OBSTACLE SPRITE CLASS
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = SCREEN_WIDTH / 2
        self.ypos = -91
        self.rect = new_seaweed_image.get_rect()
        self.rect.x = self.xpos
        self.rect.y = self.ypos
        self.speed = 2

    def move(self):
        if(self.rect.y > SCREEN_HEIGHT):
            self.rect.x = random.randint(0, (SCREEN_WIDTH - 90))
            self.rect.y = -91
        self.rect.move_ip(0, self.speed)
        self.xpos = self.rect.x
        self.ypos = self.rect.y

    def draw(self, surface):
        screen.blit(new_seaweed_image, self.rect)

#BACKGROUND SPRITE CLASS (DECORATION)
class BackgroundSeaweed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = random.randint(0, (SCREEN_WIDTH - 30))
        self.ypos = -31
        self.rect = background_seaweed_image.get_rect()
        self.rect.x = self.xpos
        self.rect.y = self.ypos
        self.speed = 1

    def move(self):
        if(self.rect.y > SCREEN_HEIGHT):
            self.rect.x = random.randint(0, (SCREEN_WIDTH - 30))
            self.rect.y = -31
        self.rect.move_ip(0, self.speed)
        self.xpos = self.rect.x
        self.ypos = self.rect.y

    def draw(self, surface):
        screen.blit(background_seaweed_image, self.rect)

#CREATING ALL SPRITES
player = Player()
enemy = Enemy()
obstacle1 = Obstacle()
obstacle2 = Obstacle()
obstacle3 = Obstacle()
obstacle4 = Obstacle()
obstacle5 = Obstacle()
background1 = BackgroundSeaweed()
background2 = BackgroundSeaweed()
background3 = BackgroundSeaweed()
background4 = BackgroundSeaweed()
background5 = BackgroundSeaweed()

obstacle2.speed = 3
obstacle3.speed = 1
obstacle4.speed = 2
obstacle5.speed = 3

#TEXT SETTINGS
title_font = pygame.font.SysFont('Camrbia', 30)
title_text = title_font.render('DODGE THE NAUTILUS', True, (255, 255, 255))
title_text_rect = title_text.get_rect()
title_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

instructions_font = pygame.font.SysFont('Camrbia', 20)
instructions_text = instructions_font.render('', True, (255, 255, 255))
instructions_text_rect = instructions_text.get_rect()
instructions_text_rect.center = ((SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT / 2)

score_font = pygame.font.SysFont('Arial', 15)
score_text = score_font.render('DODGE COUNT: ' + str(score), True, (255, 255, 255))
score_text_rect = score_text.get_rect()
score_text_rect.center = (SCREEN_WIDTH - 75, 25)

############################## GAME LOOP ##############################

while True:

    current_time = pygame.time.get_ticks()
    #UPDATE BACKGROUND (BACKGROUND COMPONENTS ARE SPACED OUT TO CREATES 'RANDOMIZED' LOOK)
    screen.fill(BACKGROUND_COLOR)
    background1.draw(screen)
    background1.move()
    if current_time >= 3000:
        background2.draw(screen)
        background2.move()
    if current_time >= 5000:
        background3.draw(screen)
        background3.move()
    if current_time >= 7000:
        background4.draw(screen)
        background4.move()
    if current_time >= 9000:
        background5.draw(screen)
        background5.move()
    #RECT TO ACT AS A DECORATIVE 'SEA FLOOR'
    pygame.draw.rect(screen, (194,178,128), sand_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        #KEY DOWN DETECTION TO UPDATE ANIMATION ACTION/DIRECTION
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and player_alive:
                player.action = 1
                player.frame = 0
                player.flip = False
            if event.key == pygame.K_LEFT and player_alive:
                player.action = 1
                player.frame = 0
                player.flip = True
        #KEY UP DETECTION TO UPDATE ANIMATION ACTION/DIRECTION
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.action = 0
                player.frame = 0
            if event.key == pygame.K_LEFT:
                player.action = 0
                player.frame = 0

    #LOOP CURRENT ANIMATION ACTION
    if current_time - last_update >= animation_cooldown and player_alive:
        player.frame += 1
        last_update = current_time
        if player.frame >= len(animation_list[player.action]):
            player.frame = 0

    if current_time - ai_last_update >= enemy.ai_animation_cooldown:
        ai_frame += 1
        ai_last_update = current_time
        if ai_frame >= len(ai_animation_list[ai_action]):
            ai_frame = 0

    #DISPLAY AND MOVE PLAYER RECT (HITBOX)
    player.draw(screen)
    if player_alive:
        player.handle_keys()

    #DISPALY AND MOVE ENEMY RECT (HITBOX)
    enemy.draw(screen)
    enemy.move()

    #DISPALY/ADD AND MOVE OBSTACLE RECT BASED ON SCORE (HITBOX)
    if score >= 1:
        obstacle1.draw(screen)
        obstacle1.move()
    if score >= 5:
        obstacle2.draw(screen)
        obstacle2.move()
    if score >= 10:
        obstacle3.draw(screen)
        obstacle3.move()
    if score >= 15:
        obstacle4.draw(screen)
        obstacle4.move()
    if score >= 20:
        obstacle5.draw(screen)
        obstacle5.move()

    #DISPLAY PLAYER SPRITE ANIMATION AT PLAYER RECT LOCATION
    if player.flip == False and player_alive == True:
        screen.blit(animation_list[player.action][player.frame], (player.xpos,player.ypos))
    if player.flip == True and player_alive == True:
        flipped_frame = pygame.transform.flip(animation_list[player.action][player.frame], True, False).convert_alpha()
        screen.blit(flipped_frame, (player.xpos,player.ypos))
    
    #DISPLAY AI SPRITE ANIMATION AT ENEMY RECT LOCATION
    screen.blit(ai_animation_list[ai_action][ai_frame], (enemy.xpos, enemy.ypos))

    #INCREMENT SCORE AND INCREASE ENEMY SPEED
    if(enemy.xpos < -170):
        score += 1
        score_text = score_font.render('DODGE COUNT: ' + str(score), True, (255, 255, 255))
        if(score == 2 or score == 3):
            enemy.speed = 2
            enemy.ai_animation_cooldown = 275
        elif(score == 4 or score == 5):
            enemy.speed = 3
            enemy.ai_animation_cooldown = 250
        elif(score == 6 or score == 7):
            enemy.speed = 4
            enemy.ai_animation_cooldown = 225
        elif(score == 8 or score == 9):
            enemy.speed = 5
            enemy.ai_animation_cooldown = 200
        elif(score == 10 or score == 11):
            enemy.speed = 6
            enemy.ai_animation_cooldown = 175
        elif(score >= 12):
            enemy.speed = 7
            enemy.ai_animation_cooldown = 150
    
    #DISPLAY TEXT
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(instructions_text, instructions_text_rect)
    if current_time >= 5000:
        title_text = title_font.render('', True, (255, 255, 255))
        instructions_text = instructions_font.render('use the arrow keys to move', True, (255, 255, 255))
        if current_time >= 10000:
            instructions_text = instructions_font.render('dodge the Nautilus 30 times to win', True, (255, 255, 255))
        if current_time >= 15000:
            instructions_text = instructions_font.render('', True, (255, 255, 255))
    display_surface.blit(score_text, score_text_rect)


    #CHECK IF PLAYER HITS OBSTACLE
    if player.rect.colliderect(obstacle1.rect) or player.rect.colliderect(obstacle2.rect) or player.rect.colliderect(obstacle3.rect) or player.rect.colliderect(obstacle4.rect) or player.rect.colliderect(obstacle5.rect):
        player.speed = 1
    else:
        player.speed = 3

    #CHECK IF PLAYER HITS ENEMY
    if player.hitbox.colliderect(enemy.hitbox):
        dead_player_image = pygame.transform.flip(animation_list[player.action][player.frame], False, True).convert_alpha()
        screen.blit(dead_player_image, (player.xpos,player.ypos))
        player_alive = False
        player.speed = 0
        enemy.speed = 0
        obstacle1.speed = 0
        obstacle2.speed = 0
        obstacle3.speed = 0
        obstacle4.speed = 0
        obstacle5.speed = 0
        title_text = title_font.render('GAME OVER', True, (139, 0, 0))

    #CHECK WIN CONDITION
    if score >= 30:
        player.speed = 0
        enemy.speed = 0
        obstacle1.speed = 0
        obstacle2.speed = 0
        obstacle3.speed = 0
        obstacle4.speed = 0
        obstacle5.speed = 0
        title_text = title_font.render('YOU WIN', True, (1, 50, 32))


    pygame.display.update()
    clock.tick(40)