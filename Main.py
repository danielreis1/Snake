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
playSong("REBECCA.mp3",True) # song starts after initial configurations

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


## Game Loop
# Wom Game Core
def GameLoop(screen,fpsSet):
    ## returns score
    ## screen size
    score = 0
    # sets worm and food size in constructor to be able to change it in Settings
    running = True # game running flag
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
                if checkObstacle(coords, Settings.obsList):
                    food.draw()
                    break;

        ## use screen.get_width and .get_height methods in case you need to resize

        running = checkObstacle(worm.getPos(),Settings.obsList) ## check if worm hit any obstacle


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
    global clock
    clock = pygame.time.Clock()

    pygame.display.set_caption('Worm') ## set window title
    pygame.display.set_mode(Settings.getSurface().get_size(),pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
    ## Menu function creates specific Menu
    tmpDict = Menu(screen,Settings.getBestScore(),Settings.score)
    tmpSurface ,surfaceCoords = tmpDict["init"]
    while True:
        pygame.display.update()
        event, screen, Str = block(screen)
        if Str == "quit":
            exit()
        elif Str == "mouse":
            if hitCoords(event,tmpSurface,surfaceCoords):
                Settings.event(tmpSurface,"init")
            screen.fill(black)
            pygame.display.set_mode(Settings.getSurface().get_size(), pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
            tmpDict = Menu(screen,Settings.getBestScore(),Settings.score)
            tmpSurface ,surfaceCoords = tmpDict["init"]
            continue
        elif Str == "keydown":
            break;
        elif Str == "resize":
            # possible solution -> store image in memory and load it after(use surface's transform method)
            screen = Settings.getSurface()
            size = event.dict['size'] ## get window size
            loadAndResize(screen, size, "snake.png")

    fpsSet = Settings.getSpeed()
    screen.fill(black)
    Settings.update()
    score = GameLoop(screen,fpsSet)
    Settings.saveScore(score)
    # make a music play
    # made option background rectangle blink when u press a settings option
    # fixed Menu function sending returned elements to Settings
    # made Settings dict
    # fixed Settings event
    # decoupled eventCoords from event
