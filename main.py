import pygame
from pygame import mixer
import random
import math

#Initialize
pygame.init()

clock = pygame.time.Clock()
FPS = 60

#Create Game Screen
screen = pygame.display.set_mode((800, 600))

#Title, Icon, Background Image & Sound
pygame.display.set_caption("Galaga 2.0")

icon = pygame.image.load("./images/icon.png")
pygame.display.set_icon(icon)

bg = pygame.image.load('./images/bg_img.png')
bg_y1 = 0
bg_y2 = bg.get_height()

mixer.music.load('./audio/backgroundMusic.mp3')
mixer.music.play(-1)

#Player
playerImg = pygame.image.load('./images/ship.png')
playerX = 368
playerY = 480
playerXChange = 0
playerYChange = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = [] 
no_enemies = 1

for i in range(no_enemies):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 50))

enemyXChange = 2
enemyYChange = 2

#Laser
laserImg = pygame.image.load('./images/laser.png')
laserX = 0
laserY = 480
laserXChange = 0
laserYChange = 10
laserState = "ready"

#Score
enemiesKilled = 0
font = pygame.font.Font('./font/scoreFont.ttf', 25)
textX = 25
textY = 25

gameOverFont = pygame.font.Font('./font/scoreFont.ttf', 60)
resetGameFont = pygame.font.Font('./font/scoreFont.ttf', 20)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    if i < len(enemyImg):
        screen.blit(enemyImg[i], (x, y))

def laserFire(x, y):
    global laserState 
    laserState = "fire"
    screen.blit(laserImg, (x, y))

def shipContact(enemyX, enemyY, X, Y):
    shipDestroy = math.sqrt(math.pow((X - enemyX), 2) + math.pow((Y - enemyY), 2))

    return shipDestroy <= 36;

def scoreDisplay(x, y):
    score = font.render("Score:" +  str(enemiesKilled*100), True, (255, 255, 255))
    screen.blit(score, (x , y))

def gameOver():
    global gameOverB
    gameOverB = True
    over = gameOverFont.render("Game Over", True, (255, 255, 255))
    resetGame = resetGameFont.render("Press SPACE to reset game.", True, (255, 255, 255))
    screen.blit(over, (125, 270))
    screen.blit(resetGame, (155, 350))

def resetGame():
    global playerX, playerY, laserY, laserState, enemiesKilled, gameOverB, gameOverSound, no_enemies
    playerX = 368
    playerY = 480
    laserY = 480
    gameOverB = False
    gameOverSound = True
    laserState = "ready"
    enemiesKilled = 0
    no_enemies = 1  # Increment the number of enemies
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    for i in range(no_enemies):
        enemyImg.append(pygame.image.load('./images/enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(0, 100))

#Level Start/End Sound
levelStart = mixer.Sound('./audio/levelStart.mp3')
levelStart.play()
levelOver = mixer.Sound('./audio/gameOver.mp3')
gameOverSound = True

#Window Loop
running = True
while running:

    clock.tick(FPS)
    
    #Background Image
    screen.blit(bg, (0, bg_y1))
    screen.blit(bg, (0, bg_y2))
    bg_y1 += 2
    bg_y2 += 2
    if bg_y1 >= bg.get_height():
        bg_y1 = -bg.get_height()
    if bg_y2 >= bg.get_height():
        bg_y2 = -bg.get_height()

    for event in pygame.event.get():

        #Window Close Event
        if event.type == pygame.QUIT:
            running = False

        #Keyboard Control
        keypress = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerXChange = -3
            if  event.key == pygame.K_d:
                playerXChange = 3
            if  event.key == pygame.K_w:
                playerYChange = -3
            if   event.key == pygame.K_s:
                playerYChange = 3

            if event.key == pygame.K_SPACE and gameOverB:
                levelStart.play()
                mixer.music.play(-1)
                resetGame()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerXChange = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                playerYChange = 0

    laserFire(playerX, laserY)
    # laserSound = mixer.Sound('./audio/laser.mp3')
    # laserSound.play()

    #Player Boundaries
    playerX += playerXChange
    playerY += playerYChange

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
        shipDestruction = shipContact(enemyX[i], enemyY[i], playerX, playerY)

        if enemyY[i] > 552 or shipDestruction:
            for j in range (no_enemies):
                enemyY[j] = 1000
            mixer.music.stop()
            gameOver()
            laserState = "ready"
            laserY = 1000

            if gameOverSound:
                levelOver.play()
                gameOverSound = False
            break

        enemyX[i] += enemyXChange
        enemyY[i] += enemyYChange

        if enemyX[i] <= 0:
            enemyXChange = 2
        elif enemyX[i] >= 736:
            enemyXChange = -2
        if enemyY[i] <=0:
            enemyYChange = 2
        # elif enemyY[i] >= 536:
        #     enemyYChange = -2

        #Collision Logic
        collision = shipContact(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            enemyKilled = mixer.Sound('./audio/enemyKillSound.mp3')
            enemyKilled.play()
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(0, 100)
            enemiesKilled += 1

            if enemiesKilled % 5 == 0:
                no_enemies += 1
                enemyImg.append(pygame.image.load('./images/enemy.png'))
                enemyX.append(random.randint(0, 736))
                enemyY.append(random.randint(0, 50))

        enemy(enemyX[i], enemyY[i], i)

    #Laser Movement
    if laserY <= 0:
        laserY = playerY
        laserState == "ready"

    laserX = playerX
    if laserState == "fire":
        laserFire(laserX, laserY)
        laserY -= laserYChange

    #Player Display
    player(playerX, playerY)
    scoreDisplay(textX, textY)
    pygame.display.update()