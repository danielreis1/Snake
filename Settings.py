import pygame
from Utils import *

class Settings:
    def __init__(self,surface):
        #default values
        # make dict that stores all images for event {"init" , (surface,surfaceCoords)} use in Menu function
        self.speed = 50 ##fps
        self.surface = surface
        self.backgroundColor = black # may be needed in case of transparency
        #GameSpecific
        self.SnakeSize = 5 ## Snake rectangles size (Snake is made up of rectangles)
        self.foodRadius = 3
        self.score = 0
        self.bestScore = 0 ## placeholder value
        self.obsList = [] ##stores obstacles
        self.textSurfaceDict = {} # dictionary keys are "commands" for event
        self.numberObs = 3
        self.collision = True #sets if Snake collides with outter Walls


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
        self.textSurfaceDict = {}
        self.score = 0

    def init(self):

        # Simple Settings example
        # Pre-set Settings screen size unresizable
        #
        # init returns screen
        ## returns previous screen
        screenSize = (500,500)
        textcolor = white
        backgroundColor = black
        textSize = 12
        self.textSurfaceDict = {}
        #Message Surfaces draw a rectangle with text to display
        screen = pygame.display.set_mode(screenSize)
        msgSurface("Use left mouse button to change settings", textSize,textcolor, backgroundColor,backgroundColor, -100,-100,screen)
        msgSurface("Press any Key to start", textSize,textcolor, backgroundColor,backgroundColor, 0, 0,screen)

        increaseSpeedSur, coordsIncSpeed = msgSurface("Speed +", textSize,textcolor, backgroundColor,backgroundColor, 150, 200,screen)
        self.textSurfaceDict["speed+"] = [increaseSpeedSur,coordsIncSpeed]

        decreaseSpeedSur,coordsDecSpeed = msgSurface("Speed -", textSize,textcolor, backgroundColor,backgroundColor, 150, 100,screen)
        self.textSurfaceDict["speed-"] = [decreaseSpeedSur,coordsDecSpeed]

        ToggleCollSur, coordsToggleColl = msgSurface("Toggle Collision", textSize,textcolor, backgroundColor,backgroundColor, -100, 200,screen)
        self.textSurfaceDict["collision"] = [ToggleCollSur,coordsToggleColl]

        bestScore = str(self.getBestScore())
        msgSurface("BestScore = " + bestScore, textSize,textcolor, backgroundColor,backgroundColor, 100, 0, screen)
        while True:
            event,Str = block()
            if Str == "quit":
                exit()
            elif Str == "keydown":
                    self.textSurfaceDict = {}
                    return
            elif Str == "mouse":
                dic = self.textSurfaceDict
                for Str in dic:
                    if hitCoords(event,dic[Str][0],dic[Str][1]):
                        self.event(dic[Str][0], Str)
                        #following lines make screen "blink"
                        screen.fill(black)
                        pygame.display.update()
                        return self.init()

    def event (self,surface, Str):
        # widget code
        ## can also have starting size
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

    def setSurface(self,screen):
        self.surface = screen

    def getSurface(self):
        return self.surface

    def setFps(self,fps):
        self.speed = fps

    def setScore(self, score):
        self.score = score

    def setFoodRadius(self, radius):
        self.foodRadius = radius

    def getFoodRadius(self):
        return self.foodRadius

    def setSnakeSize(self, size):
        self.SnakeSize = size

    def getSnakeSize(self):
        return self.SnakeSize

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
