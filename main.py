import pygame
from pygame import mixer
import random
import math

#Initialize
pygame.init()

#Create Game Screen
screen = pygame.display.set_mode((800, 600))

#Title, Icon, Background Image & Sound
pygame.display.set_caption("Galaga 2.0")

icon = pygame.image.load("./images/icon.png")
pygame.display.set_icon(icon)

bg = pygame.image.load('./images/bg_img.png')

mixer.music.load('./audio/backgroundMusic.mp3')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('./images/ship.png')
playerX = 368
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = [] 
no_enemies = 5

for i in  range(no_enemies):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 100))

enemyX_change = 0.5
enemyY_change = 0.5

#Laser
laserImg = pygame.image.load('./images/laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 7.5
laserState = "ready"

#Score
enemiesKilled = 0
font = pygame.font.Font('./font/scoreFont.ttf', 25)
textX = 25
textY = 25

gameOverFont = pygame.font.Font('./font/scoreFont.ttf', 60)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    for i in range (no_enemies):
        screen.blit(enemyImg[i], (x, y))

def laserFire(x, y):
    global laserState 
    laserState = "fire"
    screen.blit(laserImg, (x, y))

def isCollision(enemyX, enemyY, laserX, laserY):
    dist = math.sqrt(math.pow((laserX - enemyX), 2) + math.pow((laserY - enemyY), 2))
    if  dist < 36:
        return True
    else:
        return False

def scoreDisplay(x, y):
    score = font.render("Score:" +  str(enemiesKilled*100), True, (255, 255, 255))
    screen.blit(score, (x , y))


def gameOver():
    over = gameOverFont.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (125, 270))

#Level Start Sound
levelStart = mixer.Sound('./audio/levelStart.mp3')
levelStart.play()

#Window Loop
running = True
while running:

    #Screen colour
    screen.fill((0, 0, 0))

    #Background Image
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():

        #Window Close Event
        if event.type == pygame.QUIT:
            running = False

    #Keyboard Control
        keypress = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if  event.key == pygame.K_RIGHT:
                playerX_change = 1
            if  event.key == pygame.K_UP:
                playerY_change = -1
            if   event.key == pygame.K_DOWN:
                playerY_change = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    laserFire(playerX, laserY)
    # laserSound = mixer.Sound('./audio/laser.mp3')
    # laserSound.play()

    #Player Boundaries
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    if playerY <=0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    #Enemy Movement
    for i in range (no_enemies):

        #Game Over
        if enemyY[i] > 536:
            for j in range (no_enemies):
                enemyY[j] = 1000
            gameOver()
            laserState = "ready"
            laserY = 1000
            break

        enemyX[i] += enemyX_change
        enemyY[i] += enemyY_change

        if enemyX[i] <= 0:
            enemyX_change = 0.5
        elif enemyX[i] >= 736:
            enemyX_change = -0.5
        if enemyY[i] <=0:
            enemyY_change = 0.5
        # elif enemyY[i] >= 536:
        #     enemyY_change = -0.5

        #Collision Logic
        collision = isCollision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            enemyKilled = mixer.Sound('./audio/enemyKillSound.mp3')
            enemyKilled.play()
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)
            enemiesKilled += 1
            # print(score)

        enemy(enemyX[i], enemyY[i], i)

    #Laser Movement
    if laserY <= 0:
        laserY = playerY
        laserState == "ready"

    laserX = playerX
    if laserState == "fire":
        laserFire(laserX, laserY)
        laserY -= laserY_change

    #Player Display
    player(playerX, playerY)
    scoreDisplay(textX, textY)
    pygame.display.update()