#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import math
from pygame import mixer

pygame.init()  # initializing the pygame
screen = pygame.display.set_mode((800, 600))  # create the window

# anything happening inside the game window is called event

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
textX = 10
textY = 10

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,772))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(3)
    enemyY_change.append(40)

#background
background = pygame.image.load('bg.jpg')

#background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)#this will play on loop

#bullet
#ready state- cant see the bullet on screen
#fire state- bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+3,y+10))

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw

def enemy(enemyImg,x, y):
    screen.blit(enemyImg, (x, y))  

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    return False

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))

# Game Loop
running = True
while running:

    screen.fill((255, 180, 200))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left

        if event.type == pygame.KEYDOWN:  # if any keystroke is pressed
            if event.key == pygame.K_LEFT:  # if keystroke is left
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # if keystroke is right
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    #checking for boundaries 
    playerX += playerX_change
    if playerX<=0 :
        playerX = 0
    elif playerX>=772 :
        playerX = 772

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #enemy movements
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0 :
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=772 :
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]


        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: 
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50,150)

        enemy(enemyImg[i],enemyX[i],enemyY[i])
   


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()


			