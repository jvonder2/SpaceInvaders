# Imports
import pygame
from sys import exit
import random
import numpy as np
pygame.init()

# Variable
alienArray = np.zeros((2, 20), dtype=int)
velocity1 = 10
showCount = 0
difficulty = 1
difficultyTest = 2
difficultShow = 0
alienCount = 20
velocity = 5
score = 0
money = 0
bulletShot = False
collideEnemy = False
screenStatus = "home"
black = (0,0,0)
white = (255,255,255)
gray = (160,160,160)
lightGray = (224,224,224)
green = (0,204,0)
lightGreen = (0,255,0)
text_color = (255, 255, 255)
text_color2 = (128,128,128)
transparent = (0,0,0,0)
fontLarge = pygame.font.Font(None, 100)
fontSmall = pygame.font.Font(None,50)
run = True

with open('highScoreFile.txt', 'r') as file:
    content = file.read()
highScore = int(content)

# Game Boot
screen = pygame.display.set_mode((500,750))
pygame.display.set_caption("Space Adventure")
clock = pygame.time.Clock()

# Image Ports
background = pygame.image.load('Images/spaceBackground2.png')
endTest = pygame.image.load('Images/pixil-frame-0.png')
homeScreen = pygame.image.load("Images/homeScreen.png")
gameOver = pygame.image.load("Images/gameOver.png")

redEnemy = pygame.image.load('Images/redAlien2.png')
greenEnemy = pygame.image.load('Images/greenAlien1.png')
yellowEnemy = pygame.image.load('Images/yellowAlien2.png')
purpleEnemy = pygame.image.load('Images/purpleAlien1.png')
blueEnemy = pygame.image.load('Images/blueAlien2.png')
enemyBullets = pygame.image.load('Images/testingBullet2.png')
players = pygame.image.load('Images/pixil-frame-0 (15) (1).png')
playerBullets = pygame.image.load('Images/playerBullet1.png')

# Classes
class Alien:
    def __init__(self,x,y,minX,maxX,maxY,movementX,movementY,placement):
        self.y,self.initialY = y,y
        self.x,self.initialX = x,x
        self.minX = minX
        self.maxX = maxX
        self.maxY = maxY
        self.placement = placement
        self.movementX = movementX
        self.initialMovementX = movementX
        self.movementY = movementY
        self.initialMovementY = movementY
        alienArray[0,self.placement] = self.x
        alienArray[1,self.placement] = self.y

    def createEnemy(self,alienType):
        self.enemyHitBox = alienType.get_rect(center=((self.x,self.y)))
        screen.blit(alienType, self.enemyHitBox)
        return self.enemyHitBox

    def enemyMovement(self):
        self.x += self.movementX
        alienArray[0, self.placement] = self.x
        alienArray[1, self.placement] = self.y
        if self.x == self.minX or self.x == self.maxX:
            self.movementX *= -1
            if self.y < self.maxY:
                self.y += self.movementY
        
    def deadEnemy(self,bullet,alienCount,score,money):
        if bullet.colliderect(self.enemyHitBox):
            collideEnemy = True
            self.x += 1000
            self.y = 950
            self.movementX = 0
            self.movementY = 0
            alienCount -= 1
            score += 10
            money += 10
            return alienCount,collideEnemy,score,money
        else:
            collideEnemy = False
            return alienCount,collideEnemy,score,money

    def alienReset(self,alienCount):
        if alienCount == 0:
            self.x = self.initialX
            self.y = self.initialY
            self.movementX = self.initialMovementX
            self.movementY = self.initialMovementY
            alienArray[0, self.placement] = self.x
            alienArray[1, self.placement] = self.y
            alienCount = 20
        return alienCount


class enemyBullet:
    def __init__(self,ebX,ebY):
        self.ebX = ebX
        self.ebY = ebY

    def enemyBullet(self,bullet):
        self.enemyBulletHitBox = bullet.get_rect(center=((self.ebX, self.ebY)))
        screen.blit(bullet, self.enemyBulletHitBox)
        return self.enemyBulletHitBox

    def enemyBulletMovement(self):
        if self.ebY >= 1000:
            shoot = True
        else:
            shoot = False
        if shoot:
            self.bulletPlace = random.randint(0,19)
            self.ebX = alienArray[0,self.bulletPlace]
            self.ebY = alienArray[1,self.bulletPlace]
            shoot = False
        self.ebY += 10

class player():
    def __init__ (self,pX,pY):
        self.pX = pX
        self.pY = pY
        self.playerHitBox = None

    def player(self,player):
        self.playerHitBox = player.get_rect(center=((self.pX, self.pY)))
        screen.blit(player, self.playerHitBox)
        return self.playerHitBox

    def playerMovement(self,velocity,keys):
        if keys[pygame.K_LEFT] and self.pX > 50:
            self.pX -= (velocity + 2)
        if keys[pygame.K_RIGHT] and self.pX < 450:
            self.pX += (velocity + 2)

    def deadPlayer(self,enemyBullet):
        if enemyBullet.colliderect(self.playerHitBox):
            screenStatus = "end"
        else:
            screenStatus = "game"
        return screenStatus

class playerBullet():
    def __init__(self, bulletX,bulletY,velocity):
        self.bulletX = bulletX
        self.bulletY = bulletY
        self.bulletHitBox = None
        self.bulletShot = False
        self.velocity = velocity
    def bullet(self,bulletImage,pX,pY,collideEnemy):
        if collideEnemy:
            self.bulletShot = False
            colideEnemy = False
        if not self.bulletShot:
            self.bulletX = pX
            self.bulletY = pY + 10
        self.bulletHitBox = bulletImage.get_rect(center=((self.bulletX, self.bulletY)))
        screen.blit(bulletImage,self.bulletHitBox)
        return self.bulletHitBox

    def bulletShoot(self, keys):
        if keys[pygame.K_LCTRL] and not self.bulletShot:
            self.bulletShot = True
        if self.bulletShot:
            self.bulletY -= self.velocity
            if self.bulletY < 0:
                self.bulletShot = False

class buttons():
    def __init__(self, color, highlightColor, textColor, font, x, y, width, height):
        self.color = color
        self.highlightColor = highlightColor
        self.textColor = textColor
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def drawButton(self,mousePos,screen,text):
        self.buttonRect = pygame.Rect(self.x,self.y,self.width,self.height)
        if self.buttonRect.collidepoint(mousePos):
            pygame.draw.rect(screen, self.highlightColor, self.buttonRect)
        else:
            pygame.draw.rect(screen, self.color, self.buttonRect)

        textSurf = self.font.render(text, True, self.textColor)
        textRect = textSurf.get_rect(center= self.buttonRect.center)
        screen.blit(textSurf, textRect)
        return self.buttonRect

    def buttonInteraction(self,screenStatus,changeScreen,mousePos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttonRect.collidepoint(mousePos):
                screenStatus = changeScreen
        return screenStatus



redAlien1 = Alien(50,50,-50,150,275,1,75,0)
redAlien2 = Alien(50,125,-50,150,350,1,75,1)
redAlien3 = Alien(50,200,-50,150,425,1,75,2)
redAlien4 = Alien(50,275,-50,150,500,1,75,3)

blueAlien1 = Alien(150,50,50,250,275,1,75,4)
blueAlien2 = Alien(150,125,50,250,350,1,75,5)
blueAlien3 = Alien(150,200,50,250,425,1,75,6)
blueAlien4 = Alien(150,275,50,250,500,1,75,7)

greenAlien1 = Alien(250,50,150,350,275,1,75,8)
greenAlien2 = Alien(250,125,150,350,350,1,75,9)
greenAlien3 = Alien(250,200,150,350,425,1,75,10)
greenAlien4 = Alien(250,275,150,350,500,1,75,11)

purpleAlien1 = Alien(350,50,250,450,275,1,75,12)
purpleAlien2 = Alien(350,125,250,450,350,1,75,13)
purpleAlien3 = Alien(350,200,250,450,425,1,75,14)
purpleAlien4 = Alien(350,275,250,450,500,1,75,15)

yellowAlien1 = Alien(450,50,350,550,275,1,75,16)
yellowAlien2 = Alien(450,125,350,550,350,1,75,17)
yellowAlien3 = Alien(450,200,350,550,425,1,75,18)
yellowAlien4 = Alien(450,275,350,550,500,1,75,19)

enemyBullet1 = enemyBullet(1000,800)
enemyBullet2 = enemyBullet(1000,800)
enemyBullet3 = enemyBullet(700,800)

playerBullet1 = playerBullet(1000,0,velocity1)
player1 = player(250,600)

# Buttons
playButton = buttons(green,lightGreen,white,fontLarge,100,500,300,100)
exitButton = buttons(green,lightGreen,white,fontLarge,150,400,200,100)
pauseButton = buttons(gray, lightGray, white, fontSmall,10,10,50,50)
pausePlayButton = buttons(gray,lightGray,white,fontLarge,100,375,300,100)

# Text
spaceSurface = buttons(black,black,white,fontLarge,100,200,300,100)
invadersSurface = buttons(black,black,white,fontLarge,75,275,350,100)
bottomSurface = buttons(gray,gray, white,fontSmall,0,675,500,75)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if screenStatus == "game":
        screen.blit(background, (0,0))
        keys = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()

        redAlien1.createEnemy(redEnemy)
        redAlien1.enemyMovement()
        redAlien2.createEnemy(redEnemy)
        redAlien2.enemyMovement()
        redAlien3.createEnemy(redEnemy)
        redAlien3.enemyMovement()
        redAlien4.createEnemy(redEnemy)
        redAlien4.enemyMovement()

        blueAlien1.createEnemy(blueEnemy)
        blueAlien1.enemyMovement()
        blueAlien2.createEnemy(blueEnemy)
        blueAlien2.enemyMovement()
        blueAlien3.createEnemy(blueEnemy)
        blueAlien3.enemyMovement()
        blueAlien4.createEnemy(blueEnemy)
        blueAlien4.enemyMovement()

        greenAlien1.createEnemy(greenEnemy)
        greenAlien1.enemyMovement()
        greenAlien2.createEnemy(greenEnemy)
        greenAlien2.enemyMovement()
        greenAlien3.createEnemy(greenEnemy)
        greenAlien3.enemyMovement()
        greenAlien4.createEnemy(greenEnemy)
        greenAlien4.enemyMovement()

        purpleAlien1.createEnemy(purpleEnemy)
        purpleAlien1.enemyMovement()
        purpleAlien2.createEnemy(purpleEnemy)
        purpleAlien2.enemyMovement()
        purpleAlien3.createEnemy(purpleEnemy)
        purpleAlien3.enemyMovement()
        purpleAlien4.createEnemy(purpleEnemy)
        purpleAlien4.enemyMovement()

        yellowAlien1.createEnemy(yellowEnemy)
        yellowAlien1.enemyMovement()
        yellowAlien2.createEnemy(yellowEnemy)
        yellowAlien2.enemyMovement()
        yellowAlien3.createEnemy(yellowEnemy)
        yellowAlien3.enemyMovement()
        yellowAlien4.createEnemy(yellowEnemy)
        yellowAlien4.enemyMovement()

        
        eBulletHitBox = enemyBullet1.enemyBullet(enemyBullets)
        enemyBullet1.enemyBulletMovement()
        eBulletHitBox2 = enemyBullet2.enemyBullet(enemyBullets)
        eBulletHitBox3 = enemyBullet3.enemyBullet(enemyBullets)

        playerBullet1.bulletShoot(keys)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY,collideEnemy)
        alienCount, collideEnemy,score,money = redAlien1.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = redAlien2.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = redAlien3.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = redAlien4.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = blueAlien1.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = blueAlien2.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = blueAlien3.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = blueAlien4.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = greenAlien1.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = greenAlien2.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = greenAlien3.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = greenAlien4.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = purpleAlien1.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = purpleAlien2.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = purpleAlien3.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = purpleAlien4.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = yellowAlien1.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = yellowAlien2.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = yellowAlien3.deadEnemy(pBulletHitBox, alienCount,score,money)

        pBulletHitBox = playerBullet1.bullet(playerBullets, player1.pX, player1.pY, collideEnemy)
        alienCount, collideEnemy,score,money = yellowAlien4.deadEnemy(pBulletHitBox, alienCount,score,money)

        redAlien1.alienReset(alienCount)
        redAlien2.alienReset(alienCount)
        redAlien3.alienReset(alienCount)
        redAlien4.alienReset(alienCount)

        blueAlien1.alienReset(alienCount)
        blueAlien2.alienReset(alienCount)
        blueAlien3.alienReset(alienCount)
        blueAlien4.alienReset(alienCount)

        greenAlien1.alienReset(alienCount)
        greenAlien2.alienReset(alienCount)
        greenAlien3.alienReset(alienCount)
        greenAlien4.alienReset(alienCount)

        purpleAlien1.alienReset(alienCount)
        purpleAlien2.alienReset(alienCount)
        purpleAlien3.alienReset(alienCount)
        purpleAlien4.alienReset(alienCount)

        yellowAlien1.alienReset(alienCount)
        yellowAlien2.alienReset(alienCount)
        yellowAlien3.alienReset(alienCount)
        alienCount = yellowAlien4.alienReset(alienCount)

        player1.player(players)
        player1.playerMovement(velocity,keys)

        screenStatus = player1.deadPlayer(eBulletHitBox)

        if screenStatus == "game" and score >= 200:
            difficulty = 2
            if difficultyTest == 2:
                showCount = 0
                difficultyTest += 1
                difficultShow = 0
            enemyBullet2.enemyBulletMovement()
            screenStatus = player1.deadPlayer(eBulletHitBox2)

        if screenStatus == "game" and score >= 400:
            difficulty = 3
            if difficultyTest == 3:
                showCount = 0
                difficultShow = 0
                difficultyTest += 1
            enemyBullet3.enemyBulletMovement()
            screenStatus = player1.deadPlayer(eBulletHitBox3)

        text_surface = fontSmall.render("Score: " + str(score), True, (255,255,255))
        screen.blit(text_surface, (300,15))
        text_surfaceMoney = fontSmall.render("Money: " + str(money), True, (137,243,54))
        #screen.blit(text_surfaceMoney, (10, 400))

        if difficultShow < 15 and showCount <= 2:
            difficultSurface = fontSmall.render("Difficulty: " + str(difficulty), True, (255, 255, 255))
            screen.blit(difficultSurface, (150, 450))
        difficultShow += 1

        if difficultShow == 30:
            difficultShow = 0
            showCount += 1

        mousePos = pygame.mouse.get_pos()
        pauseButtonRect = pauseButton.drawButton(mousePos,screen,"||")
        screenStatus = pauseButton.buttonInteraction(screenStatus, "pause",mousePos)
        bottomSurface.drawButton(mousePos, screen, "")

    elif screenStatus == "pause":
        screen.blit(endTest,(800,0))
        mousePos = pygame.mouse.get_pos()
        pausePlayButtonRect = pausePlayButton.drawButton(mousePos,screen,"Play")
        screenStatus = pausePlayButton.buttonInteraction(screenStatus,"game",mousePos)

    elif screenStatus == "end":
        screen.blit(gameOver,(0,0))
        if score >= highScore:
            highScore = score
            highScoreCopy = open('highScoreFile.txt', 'w')
            highScoreCopy.write(str(highScore))
            highScoreCopy.close()
            text_surface2 = fontSmall.render("New High Score!",True,(255,255,255))
            screen.blit(text_surface2, (110,500))

        text_surface1 = fontLarge.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text_surface1, (100, 600))
        mousePos = pygame.mouse.get_pos()
        exitButtonRect = exitButton.drawButton(mousePos,screen,"Exit")
        screenStatus = exitButton.buttonInteraction(screenStatus,"home",mousePos)
        enemyBullet1.ebX = 1000
        enemyBullet2.ebX = 1000
        enemyBullet3.ebX = 1000
        playerBullet1.bulletY = -100
        player1.pX = 250
        alienCount = 0

    else:
        mousePos = pygame.mouse.get_pos()
        screen.blit(background,(0,0))
        invadersSurface.drawButton(mousePos, screen, "Invaders")
        spaceSurface.drawButton(mousePos,screen,"Space")
        playButtonRect = playButton.drawButton(mousePos,screen,"Play")
        highScore_surface = fontSmall.render("High Score: " + str(highScore), True, (255, 255, 255))
        screen.blit(highScore_surface , (110,400))
        mousePos = pygame.mouse.get_pos()
        screenStatus = playButton.buttonInteraction(screenStatus,"game",mousePos)
        if screenStatus == "game":
            alienCount = 0
            showCount = 0
            difficulty = 1
            difficultyTest = 2
            difficultCount = 0
            redAlien1.alienReset(alienCount)
            redAlien2.alienReset(alienCount)
            redAlien3.alienReset(alienCount)
            redAlien4.alienReset(alienCount)

            blueAlien1.alienReset(alienCount)
            blueAlien2.alienReset(alienCount)
            blueAlien3.alienReset(alienCount)
            blueAlien4.alienReset(alienCount)

            greenAlien1.alienReset(alienCount)
            greenAlien2.alienReset(alienCount)
            greenAlien3.alienReset(alienCount)
            greenAlien4.alienReset(alienCount)

            purpleAlien1.alienReset(alienCount)
            purpleAlien2.alienReset(alienCount)
            purpleAlien3.alienReset(alienCount)
            purpleAlien4.alienReset(alienCount)

            yellowAlien1.alienReset(alienCount)
            yellowAlien2.alienReset(alienCount)
            yellowAlien3.alienReset(alienCount)
            alienCount = yellowAlien4.alienReset(alienCount)
        mousePos = pygame.mouse.get_pos()
        score = 0
    pygame.display.update()
    clock.tick(30)