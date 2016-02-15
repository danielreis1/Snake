# Snake Game
#Must know
#1. http://www.pygame.org/docs/tut/newbieguide.html
#2. http://www.pygame.org/docs/
#3. create a folder named playlist

from Food import *
from Snake import *
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
Settings.surfaceSize = size
pygame.mixer.init()
#playSong("REBECCA.mp3") # song starts after initial configurations
playPlaylist()


def generateObstacles(num,screen,collision):
    # generates num number of obstacles with random Size and at a random Space
    lista = []
    for i in range(num):
        randomX = int(random.randrange(50, screen.get_width()-50))
        randomY = int(random.randrange(50,screen.get_height() -50))
        randomSizeX = int(random.randrange(20,100))
        randomSizeY = int(random.randrange(20,100))
        pos = (randomX,randomY)
        size = (randomSizeX,randomSizeY)
        obs = Obstacle(white,pos,size,black) # can pass args from Settings
        lista.insert(0,obs)
        # can make collision with outter walls
    return lista

## Game Loop
# Wom Game Core
def GameLoop(screen,fpsSet):
    ## returns score
    ## screen size
    score = 0
    # sets Snake and food size in constructor to be able to change it in Settings
    running = True # game running flag
    size = Settings.surfaceSize
    screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
    Settings.surface = screen
    Settings.obsList = generateObstacles(Settings.numberObs, screen, Settings.getCollision()) ## Settings class keeps obstacle number
    Settings.obsDraw()
    pygame.display.update()
    foodRadius = Settings.getFoodRadius()
    SnakeSize = Settings.getSnakeSize()
    food = Food(screen,foodRadius)
    snake = Snake(screen,SnakeSize)

    # sets Snake starting velocity
    event,Str = block() # blocks before game starts

    if Str == "quit":
        exit()

    elif Str == "mouse":
        return 0 ## score

    elif Str == "keydown":
        snake.event(event,True)
        while (snake.getVelocity() == (0,0)):
            event,Str = block()
            snake.event(event,True)

    elif Str == "resize":
        size = event.dict['size']
        Settings.surfaceSize = size
        screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
        snake.set_surface(screen)
        food.set_surface(screen)
        food.redraw()
        snake.redraw()
        Settings.obsDraw(screen)

    while running:
        snake.move()
        snake.draw()
        # while loop allows for food to always be drawn in a single loop
        while True:
            coords = food.foodCoords()
            if not(coords in snake.getBody()):
                if checkObstacle(coords, Settings.obsList):
                    food.draw()
                    break;

        ## use screen.get_width and .get_height methods in case you need to resize
        snake.set_surface(screen)
        if not pygame.sprite.groupcollide(snake.sprites, Settings.obsSprites,False,False) == {}:
            running = False

        if snake.checkInvalidMove():
            running = False


        coll  = not Settings.getCollision()
        snakeX,snakeY = snake.getPos()
        if snakeX > snake.surface.get_width():
            if coll:
                snake.x = 0
            else:
                running= False
        elif snakeX < 0:
                if coll:
                    snake.x = snake.surface.get_width()
                else:
                    running= False
        elif snakeY < 0:
                if coll:
                    snake.y = snake.surface.get_height()
                else:
                    running= False
        elif snakeY > snake.surface.get_height():
                if coll:
                    snake.y = 0
                else:
                    running= False


        if food.check(snake.x, snake.y):
            score += 1
            snake.eat()
            food.erase() # can make food a sprite too

        event, Str = nonBlock()
        if Str == "quit":
            exit()

        if Str == "none":
            #do nothing
            a = None
        elif Str == "keydown":
            snake.event(event,True)
        elif Str == "mouse":
            snake.event(event,False)
        elif Str == "resize":
            size = event.dict['size']
            Settings.surfaceSize = size
            screen = pygame.display.set_mode(size,screen.get_flags())
            Settings.setSurface(screen)
            snake.set_surface(screen)
            food.set_surface(screen)
            food.redraw()
            snake.draw()
            Settings.obsDraw()

        pygame.display.update()
        clock.tick(fpsSet) ## fps set -> must be set in every loop of the game loop
    return score

##set-up loop
while True:
    global clock
    clock = pygame.time.Clock()

    pygame.display.set_caption('Snake') ## set window title
    size = Settings.surfaceSize
    screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)

    ## Menu function creates specific Menu
    tmpDict = Menu(screen,Settings.getBestScore(),Settings.score)
    tmpSurface ,surfaceCoords = tmpDict["init"]
    while True:
        pygame.display.update()
        event, Str = block()
        if Str == "quit":
            exit()
        elif Str == "mouse":
            if hitCoords(event,tmpSurface,surfaceCoords):
                screen.fill(black)
                pygame.display.update()
                Settings.event(tmpSurface,"init")
            size =  Settings.surfaceSize
            screen.fill(black)
            screen = pygame.display.set_mode(size, pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
            tmpDict = Menu(screen,Settings.getBestScore(),Settings.score)
            # Menu returns dictionary with info on surfaces present
            tmpSurface ,surfaceCoords = tmpDict["init"]
            continue
        elif Str == "keydown":
            break;
        elif Str == "resize":
            size = event.dict['size'] ## get window size
            Settings.surfaceSize =size
            # possible solution -> store image in memory and load it after(use surface's transform method)
            # loadAndResize(screen,screen, size, "snake.png") #  -> used as a load image example
            # the other solution is to redo menu
            screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
            screen.fill(black)
            tmpDict = Menu(screen,Settings.getBestScore(),Settings.score)
            tmpSurface ,surfaceCoords = tmpDict["init"]
            pygame.display.update()

    fpsSet = Settings.getSpeed()
    screen.fill(black)
    Settings.update()
    score = GameLoop(screen,fpsSet)
    Settings.saveScore(score)

    # Sounds -> made playlist play for sounds pygame part
    # bitmaps -> store image function
    # sprites -> se block class in snake blocks (different branch)
    # controls -> done
    # graphics -> done?
    # animations -> done?
    # finished comments
