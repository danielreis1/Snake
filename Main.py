# Worm Game

from Food import *
from Worm import *
from Obstacle import *
from Settings import *
from Utils import *
import pygame
import random
import sys


pygame.init() ## init display
#Global Vars
score = 0
size = (500,500)
screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
Settings = Settings(screen)
Settings.init()


def generateObstacles(num):
    # generates num number of obstacles with random Size and at a random Space
    for i in range(num):
        randomX = int(random.randrange(50, screen.get_width()-50))
        randomY = int(random.randrange(50,screen.get_height() -50))
        randomSizeX = int(random.randrange(20,100))
        randomSizeY = int(random.randrange(20,100))

        pos = (randomX,randomY)
        size = (randomSizeX,randomSizeY)
        obs = Obstacle(white,pos,size,Settings.backgroundColor)
        Settings.obsList.insert(0,obs)


def Menu(backgroundSurface):
    # sets starting game messages
    textSize = 12
    bestScore = "Best Score: " + str(Settings.getBestScore())
    scoreDisplay = "score:  " + str(score)
    msgSurface(bestScore, textSize, white, black, red, -100, 200,backgroundSurface)
    msgSurface(scoreDisplay, textSize, white,black, red, -100, 100,backgroundSurface)
    msgSurface("Start? Press key ", textSize, white, black,red, 100,0,backgroundSurface)
    msgSurface("Worm", textSize, white,black,red,0,0,backgroundSurface)
    tmpSurface, surfaceCoords = msgSurface("Settings", textSize, red,black, black, 50, 50,backgroundSurface)
    return (tmpSurface, surfaceCoords)

##Game Loop
def GameLoop(screen,fpsSet):
    ## returns score
    ## screen size
    score = 0
    ##pygame.mixer.init() ##sound
    ##chomp = pygame.mixer.Sound("chomp.wav") ##music
    # sets worm and food size in constructor to be able to change it in Settings
    running = True
    generateObstacles(Settings.numberObs) ## Settings class keeps obstacle number
    Settings.obsDraw(screen)
    pygame.display.update()
    foodRadius = Settings.getFoodRadius()
    wormSize = Settings.getWormSize()
    food = Food(screen,foodRadius)
    worm = Worm(screen,wormSize)


    # sets worm starting velocity
    event,screen,Str = block(screen) # blocks before game starts

    if Str == "quit":
        exit()

    elif Str == "mouse":
        return 0 ## score

    elif Str == "keydown":
        worm.event(event,True)
        while (worm.getVelocity() == (0,0)):
            event,screen,Str = block(screen)
            worm.event(event,True)

    elif Str == "resize":
        size = event.dict['size']
        Settings.setWindowSize(size)
        screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
        Settings.setSurface(screen)
        worm.set_surface(screen)
        food.set_surface(screen)
        food.redraw()
        worm.redraw()
        Settings.obsDraw(screen)

    while running:
        worm.move()
        worm.draw()

        # while loop allows for food to always be drawn in a single loop
        while True:
            coords = food.foodCoords()
            if not(coords in worm.getBody()):
                if checkObstacle(coords, Settings):
                    food.draw()
                    break;

        ## use screen.get_width and .get_height methods in case you need to resize

        running = checkObstacle(worm.getPos(),Settings) ## check if worm hit any obstacle


        if worm.checkInvalidMove():
            running = False

        if Settings.getCollision():
            worm.checkBoundaries()
            if worm.getCrashState():
                running = False
        else:
            x,y = worm.checkBoundaries()
            if worm.getCrashState():
                wormX,wormY = worm.getPos()
                if wormX > screen.get_width():
                    worm.x = 0
                elif wormX < 0:
                    worm.x = screen.get_width()
                elif wormY < 0:
                    worm.y = screen.get_height()
                elif wormY > screen.get_height():
                    worm.y = 0

        if food.check(worm.x, worm.y):
            score += 1
            worm.eat()
            ##chomp.play() ## music
            food.erase()

        event, screen, Str = nonBlock(screen)

        if Str == "none":
            a = " "
        elif Str == "quit":
            exit()
        elif Str == "keydown":
            worm.event(event,True)
        elif Str == "mouse":
            worm.event(event,False)
        elif Str == "resize":
            size = event.dict['size']
            Settings.setWindowSize(size)
            screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
            Settings.setSurface(screen)
            worm.set_surface(screen)
            food.set_surface(screen)
            food.redraw()
            worm.redraw()
            Settings.obsDraw(screen)

        pygame.display.update()
        clock.tick(fpsSet) ## fps set
    return score

##set-up loop
while True:
 ##running = True
    ## global vars
    global clock, food, worm
    clock = pygame.time.Clock()

    ## screenflag used to only set screen once, screensize unchanged after fist iteration
    pygame.display.set_caption('Worm') ## set window title
    pygame.display.set_mode(Settings.getSurface().get_size(),pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
    tmpSurface ,surfaceCoords = Menu(screen) # sets screen in Settings

    while True:
        pygame.display.update()
        event, screen, Str = block(screen)
        if Str == "quit":
            exit()
        elif Str == "mouse":
            Settings.event(tmpSurface,"init",event,surfaceCoords)
            screen.fill(black)
            pygame.display.set_mode(Settings.getSurface().get_size(), pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
            tmpSurface ,surfaceCoords = Menu(screen)
            continue
        elif Str == "keydown":
            break;
        elif Str == "resize":
            # possible solution -> store image in memory and load it after(use surface's transform method)
            screen = Settings.getSurface()
            pygame.image.save(screen, "snake.png") # saves image as .png
            size = event.dict['size'] ## get window size
            screen = pygame.display.set_mode(size, screen.get_flags())
            Settings.setSurface(screen)
            tempSurface = pygame.image.load("snake.png") # set background image
            screen.blit(pygame.transform.scale(tempSurface,size),(0,0))

    fpsSet = Settings.getSpeed()
    screen.fill(black)
    Settings.update()
    score = GameLoop(screen,fpsSet)
    Settings.saveScore(score)

    # make a music play
    # make option background rectangle blink red when u press a settings option
    # fix Menu function sending returned elements to Settings     # make Settings dict
