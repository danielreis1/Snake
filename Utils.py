#Utils

import pygame
import random
import sys
import os

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
purple = (255,0,255)


def playlist(playlistFolderPath = "playlist/"):
    """ gets all files and folders in given folder into a list and returns it
    """
    lista = []
    n = 0
    # use os module to manipulate file system
    try:
        for i in os.listdir(playlistFolderPath):
            lista.append(i)
        return lista
    except FileNotFoundError as Error:
        print ("create playlist folder to listen to your songs")

def playPlaylist(playlistFolderPath = "playlist/"):
    """ plays songs in a folder in random order
    """
    #play playlist on shuffle
    SongList = playlist(playlistFolderPath)
    if SongList == None: # no playlist folder
        return
    listLen = len(SongList)
    if listLen == 0:
        return
    i = random.randint(0,listLen-1)
    print("\n" +SongList[i])
    pygame.mixer.music.load(playlistFolderPath + SongList[i]) # sets filename from "playlist" folder
    pygame.mixer.music.set_endevent(pygame.USEREVENT) # sends ou event when song finishses
    pygame.mixer.music.play()



def playSong(path):
    """ play a song specified by path, sends out pygame.USEREVENT when song ends"""

    pygame.mixer.music.load(path)
    # following line sends out USEREVENT every time song finishes
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    # userevent resolved directly in event() function in this specific example
    # also in this specific case the song plays forever remove set_endevent for the set song to play only once
    pygame.mixer.music.play()


def loadAndResize(screen,image,size,path = "snake.png",coords=(0,0)):
    """
    first argument = background, second arg image to resize, third image size,
    fourth path to image, last coords to blit image
    returns loaded image surface
    """
    # loads and resizes an image to (size) specified by path argument
    # default values for background
    pygame.image.save(image, path) # saves image as .png
    print("saved")
    screen = pygame.display.set_mode(size,pygame.RESIZABLE| pygame.HWSURFACE|pygame.DOUBLEBUF)
    tempSurface = pygame.image.load(path).convert() # set image
    screen.blit(pygame.transform.scale(tempSurface,size),coords)
    print("blited")
    # pygame.display.update()
    return tempSurface

def Menu(backgroundSurface, bestScore,score):
    """
    This function is an example for a specific Menu,
    returns dictionary with keys: "command" -> [surface, surfaceCoords] for all
    event bound text surfaces,
    command is used in Settings event
    """
    # sets starting game messages
    # returns dictionary with widgets surface and surfaceCoords
    dictt = {}
    textSize = 12
    # Menu function message-specific arguments, like the following:
    ## get the arguments from Settings
    size = backgroundSurface.get_size()
    bestScore = "Best Score: " + str(bestScore)
    scoreDisplay = "score:  " + str(score)
    # u can set a portion of the screen instead of fixed sizes in msgSurface
    # example: msgSurface(bestScore, textSize, white, black, red, screen.get_width()/5,screen.get_height()/5,backgroundSurface)
    msgSurface(bestScore, textSize, white, black, red, -100, 200,backgroundSurface)
    msgSurface(scoreDisplay, textSize, white,black, red, -100, 100,backgroundSurface)
    msgSurface("Arrow keys to Starts | Left mouse button over Settings to change them", textSize, white, black,red, 100,0,backgroundSurface)
    msgSurface("Snake", textSize, white,black,red,0,0,backgroundSurface)
    tmpSurface, surfaceCoords = msgSurface("Settings", textSize, red,black, black, 50, 50,backgroundSurface)
    dictt["init"] = [tmpSurface,surfaceCoords]
    return dictt

def hitCoords(event,surface,coords):
    """
    receives event to check mouse coordinates, surface to check,
    and Surface center coordinates in backgroundSurface referential
    returns true if user pressed on the given surface
    """
    # good for settings widget boundaries
    if pygame.mouse.get_pressed()[0] == True:
        x,y = event.pos
        # following line gives us coordinates in the "rectangle referential", top-left = (0,0)
        surfaceX, surfaceY = surface.get_rect().center
        #print ("rectangle coordinates center: " + "("+ str(surfaceX) +") " + "(" + str(surfaceY) +")")
        centerX , centerY = coords # coords in backgroundSurface referential
        #print ("background coordinates surface center: " + "("+ str(centerY) +") " + "(" + str(centerX) +")")
        if  ((x > centerX - surfaceX) and (x< centerX + surfaceX) and (y>centerY - surfaceY)  and (y<centerY + surfaceY )):
            return True
    return False

def exit():
    pygame.quit()
    sys.exit()

def makeTextObjs(text, font, tcolor,backgroundColor):
    """
    text , font ,text color and the background color and renders the text accordingly
    returns tuple (surface, rectangle)
    """
    ## auxiliary function to msgSurface
    ## return tuple, function used to output text boxes
    textSurface = font.render(text, True, tcolor,backgroundColor) ## render fonts
    ## check font.Font methods in pygame.font module
    return textSurface, textSurface.get_rect()


def msgSurface(text,textSize,textColor,backgroundColor,outlineColor, verticalOffset, horizontaOffset,screen):
    """
    outlineColor for text outter window color,
    vertical and horizontalOffset from original backgroundSurface center coordinates =(0,0) in background Surface
    must receive "main surface" ->special displayed surface in the last argument
    returns textSurface and center of rectangle in the rectangle referential(top-left (0,0))
    """

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
    """
    receives position tuple and obstacle List
    returns False if position in obstacle
    """
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

def block(): #decoupled block function
    """
    function blocks game waiting for events
    returns (event, String) -> string used to reference event
    """

    pygame.display.update() ## displays last screen while waits for event
    while (True):     ## loop to check when key was pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return (event, "quit")
            elif event.type == pygame.VIDEORESIZE:
                return (event,"resize")
            elif event.type == pygame.KEYDOWN:
                return (event,"keydown")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return (event,"mouse")
            elif event.type == pygame.USEREVENT:
                # event sent by music in Snake game
                # playSong("REBECCA.mp3")
                playPlaylist()


def nonBlock():
    """
    function doesn't block game waiting for events
    returns (event, String) -> string used to reference event
    returns (None, "none") in case of no event
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (event, "quit")
        elif event.type == pygame.VIDEORESIZE:
            return (event,"resize")
        elif event.type == pygame.KEYDOWN:
            return (event,"keydown")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return (event,"mouse")
        elif event.type == pygame.USEREVENT:
            #playSong("REBECCA.mp3") # -> play same song forever
            playPlaylist() #  -> play playlist on shuffle
            nonBlock()
    return (None, "none")
