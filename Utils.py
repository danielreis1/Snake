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




def playSong(path):
    # check sound Object in pygame documentation (different) from pygame.mixer.music
    pygame.mixer.music.load(path)
    # following line sends out USEREVENT every time song finishes
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    # userevent resolved directly in event() function in this specific example
    # you may set in Settings your next song in a specific playlist
    pygame.mixer.music.play()


def loadAndResize(screen,size,path):
    # loads and resizes an image to (size) specified by path arg
    pygame.image.save(screen, path) # saves image as .png
    screen = pygame.display.set_mode(size, screen.get_flags())
    Settings.setSurface(screen)
    tempSurface = pygame.image.load(path) # set background image
    screen.blit(pygame.transform.scale(tempSurface,size),(0,0))

def Menu(backgroundSurface, bestScore,score):
    # sets starting game messages
    # returns dictionary with widgets surface and surfaceCoords
    dictt = {}
    textSize = 12
    # Menu function message-specific arguments, like the following:
    ## get the arguments from Settings
    bestScore = "Best Score: " + str(bestScore)
    scoreDisplay = "score:  " + str(score)

    msgSurface(bestScore, textSize, white, black, red, -100, 200,backgroundSurface)
    msgSurface(scoreDisplay, textSize, white,black, red, -100, 100,backgroundSurface)
    msgSurface("Start? Press key ", textSize, white, black,red, 100,0,backgroundSurface)
    msgSurface("Worm", textSize, white,black,red,0,0,backgroundSurface)
    tmpSurface, surfaceCoords = msgSurface("Settings", textSize, red,black, black, 50, 50,backgroundSurface)
    dictt["init"] = [tmpSurface,surfaceCoords]
    return dictt

def hitCoords(event,surface,coords):
    # good for settings widget boundaries
    if pygame.mouse.get_pressed()[0] == True:
        x,y = event.pos
        # following line gives us coordinates in the "rectangle referential", top-left = (0,0)
        surfaceX, surfaceY = surface.get_rect().center
        #print ("rectangle coordinates center: " + "("+ str(surfaceX) +") " + "(" + str(surfaceY) +")")
        centerX , centerY = coords
        #print ("background coordinates surface center: " + "("+ str(centerY) +") " + "(" + str(centerX) +")")
        if  ((x > centerX - surfaceX) and (x< centerX + surfaceX) and (y>centerY - surfaceY)  and (y<centerY + surfaceY )):
            return True
    return False

def drawBackground(backgroundPath):
    # use to draw screen to background
    screen = pygame.display.set_mode((backgroundPath.get_width(), backgroundPath.get_height()))
    screen.blit(backgroundPath, [0,0])
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
    # returns textSurface and center of rectangle in the rectangle referential(top-left (0,0))
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


def checkObstacle(pos,obsList):
    # receives position tuple
    # returns False if position in obstacle
    for obstacle in obsList:
        x,y = pos
        obstacleX, obstacleY = obstacle.center # background referential center
        #print("obstacleX: "+ str(obstacleX) + "obstacleY: " + str(obstacleY))
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
            elif event.type == pygame.USEREVENT:
                # event sent by music in Worm game
                playSong("REBECCA.mp3")



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
        elif event.type == pygame.USEREVENT:
            playSong("REBECCA.mp3")
            #nonBlock(screen)

    return (None, screen,"none")
