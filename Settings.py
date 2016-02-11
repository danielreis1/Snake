import pygame
from Utils import *

class Settings:
    def __init__(self,surface):
        #default values
        # make dict that stores all images for event {"init" , (surface,surfaceCoords)} use in Menu function
        self.backgroundColor = black
        self.speed = 50 ##fps
        self.windowSize = (500,500)
        self.surface = surface
        self.menuCharactersColor = white
        #GameSpecific
        self.wormSize = 5 ## worm rectangles size (worm is made up of rectangles)
        self.foodRadius = 3
        self.score = 0
        self.bestScore = 0 ## placeholder value
        self.obsList = [] ##stores obstacles
        self.numberObs = 3
        self.collision = True

    def getCollision(self):
        return self.collision

    def getObsList(self):
        return self.obsList

    def obsDraw(self,a):
        screen = self.surface
        for obs in self.obsList:
            pygame.draw.rect(screen,obs.color,obs.rect)


    def update(self):
        # restart game Settings
        self.obsList = []
        self.score = 0

    def init(self):
        # Simple Settings example
        # Pre-set Settings screen size
        # init returns screen
        ## returns previous screen
        textcolor = self.menuCharactersColor
        backgroundColor = self.backgroundColor
        screen = pygame.display.set_mode((500,500)) ## set fixed  screen for settings
        screen.fill(backgroundColor)
        textSize = 12
        msgSurface("Use left mouse button to change settings", textSize,textcolor, backgroundColor,backgroundColor, -100,-100,screen)
        msgSurface("Press any Key to start", textSize,textcolor, backgroundColor,backgroundColor, 0, 0,screen)

        increaseSpeedSur, coordsIncSpeed = msgSurface("Speed +", textSize,textcolor, backgroundColor,backgroundColor, 150, 200,screen)

        decreaseSpeedSur,coordsDecSpeed = msgSurface("Speed -", textSize,textcolor, backgroundColor,backgroundColor, 150, 100,screen)

        ToggleCollSur, coordsToggleColl = msgSurface("Toggle Collision", textSize,textcolor, backgroundColor,backgroundColor, -100, 200,screen)

        bestScore = str(self.getBestScore())
        msgSurface("BestScore = " + bestScore, textSize,textcolor, backgroundColor,backgroundColor, 100, 0, screen)

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.event(decreaseSpeedSur, "speed-",event,coordsDecSpeed)
                    self.event(increaseSpeedSur, "speed+",event,coordsIncSpeed)
                    self.event(ToggleCollSur, "collision",event,coordsToggleColl)

    def event (self,surface, Str,event,coords ): #widget
        ## can also have starting size
        if pygame.mouse.get_pressed()[0] == True:
            x,y = event.pos
            surfaceX, surfaceY = surface.get_rect().center
            centerX , centerY = coords
            if  ((x > centerX - surfaceX) and (x< centerX + surfaceX) and (y>centerY - surfaceY)  and (y<centerY + surfaceY )):

                if Str == "speed-":
                    self.decreaseSpeed()

                elif Str == "speed+":
                    self.increaseSpeed()

                elif Str == "init":
                    return self.init()

                elif Str == "collision":
                    self.collision = not self.collision
                    return self.collision

    def getSpeed(self):
        return self.speed

    def increaseSpeed(self):
        self.speed += 2

    def decreaseSpeed(self):
        self.speed -= 2

    def setBackground(self,color):
        ## returns surface
        self.surface.fill(color)

    def setSurface(self,screen):
        self.windowSize = screen.get_size()
        self.surface = screen

    def getSurface(self):
        return self.surface

    def setFps(self,fps):
        self.speed = fps

    def setSize(self,size):
        self.windowSize = size

    def setScore(self, score):
        self.score = score

    def setFoodRadius(self, radius):
        self.foodRadius = radius

    def getFoodRadius(self):
        return self.foodRadius

    def setWormSize(self, size):
        self.wormSize = size

    def getWormSize(self):
        return self.wormSize

    def getBestScore(self):
        #returns int
        f = open ("Score.txt", "r")
        for line in f:
            num = int(line[0]) # doesn't read "\n"
            if num > self.bestScore:
                self.bestScore = int(line)
        f.close()
        return self.bestScore

    def saveScore(self,score):
        # saves score to best score list
        f = open ("Score.txt", "a")
        f.write(str(score) + " \n")
        f.close()

    def setWindowSize(self,size):
        self.windowSize = size

    def getWindowSize(self):
        return self.windowSize
