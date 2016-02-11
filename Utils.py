#Utils

import pygame
import random
import sys

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
purple = (255,0,255)


def drawBackground(background):
    # use to draw screen to background
    screen = pygame.display.set_mode((background.get_width(), background.get_height()))
    screen.blit(background, [0,0])
    pygame.display.flip()


def exit():
    pygame.quit()
    sys.exit()

def makeTextObjs(text, font, tcolor,backgroundColor):
    ## auxiliary function to msgSurface
    ## return tuple, function used to output text boxes
    textSurface = font.render(text, True, tcolor,backgroundColor) ## render fonts
    ## check font.Font methods in pygame.font module
    return textSurface, textSurface.get_rect()


def msgSurface(text,textSize,textColor,backgroundColor,outlineColor, verticalOffset, horizontaOffset,screen):
    ## "pixel counting" starts top left corner
    width, height = screen.get_size()
    # can also set text object's font in arguments
    ## sets fonts
    textFont = pygame.font.Font('freesansbold.ttf', textSize)
    ## auxiliary function
    titleTextSurf, titleTextRect = makeTextObjs(text,textFont , textColor, black)
    titleTextRect.center = (int(width/2)+ horizontaOffset , int(height/2)+ verticalOffset)          ## set CenterCoords

    pygame.draw.rect(screen, outlineColor,titleTextRect,10) #draw built-in outline
    ## blit -> draws image on top of another
    screen.blit(titleTextSurf, titleTextRect) ## adds image
    return titleTextSurf, titleTextRect.center


def checkObstacle(pos,Settings):
    # receives position tuple
    # returns False if position in obstacle
    for obstacle in Settings.getObsList():
        x,y = pos
        obstacleX, obstacleY = obstacle.center
        left = obstacleX - int(obstacle.size[0]/2)
        right = obstacleX + int(obstacle.size[0]/2)
        top = obstacleY + int(obstacle.size[1]/2)
        bot = obstacleY - int(obstacle.size[1]/2)
        if ((x >= left and x <= right) and (y >=bot and y <= top)):
            return False
    return True

def block(screen): #decoupled block function
    # returns (event, screen, String)
    ## function blocks game waiting for events
    pygame.display.update() ## displays last screen while waits for event

    while (True):     ## loop to check when key was pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (event, screen, "quit")
            elif event.type == pygame.VIDEORESIZE:
                return (event,screen,"resize")
            elif event.type == pygame.KEYDOWN:
                return (event,screen,"keydown")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return (event,screen,"mouse")


def nonBlock(screen):
    # returns (event, screen, String)
    ## function gets event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (event, screen, "quit")
        elif event.type == pygame.VIDEORESIZE:
            return (event,screen,"resize")
        elif event.type == pygame.KEYDOWN:
            return (event,screen,"keydown")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return (event,screen,"mouse")
    return (None, screen,"none")
