
import pygame
import random
from Obstacle import *


class Snake():
    def __init__(self, surface, SnakeSize):
        self.surface = surface
        ## starts in the middle
        self.x = surface.get_width() / 2
        self.y = surface.get_height() / 2
        self.size = SnakeSize ## Snake size in pixels "set Snake square size"
        self.length = 1
        self.grow_to = 20
        ## "velocity x and y"
        self.vx = 0
        self.vy = 0  ## starts going up
        ## body is list of tuples (self.x, self.y)
        self.color = white ## color assigned to tuple
        self.body = [] #can be a list of sprite objects to get use of sprite collision methods
        self.surfaceBody = [Obstacle(self.color,(self.x,self.y),(self.size,self.size),black)]
        self.sprites = pygame.sprite.Group(self.surfaceBody[0]) # -> snake has obstacles or blocks
        self.crashed = False ## state
        self.invalidMove = False


    def checkInvalidMove(self):
        #checks invalidMove flag
        if self.invalidMove:
            self.invalidMove = False
            return True
        return False

    def getVelocity(self):
        return (self.vx, self.vy)

    def getPos(self):
        return (self.x,self.y)

    def set_surface(self,surface):
        self.surface = surface

    def eat(self):
        self.grow_to += 10

    def getBody(self):
        return self.body

    def event(self, event, keyBoolean):
    ## Handles events.
    # keyBoolean true for keyboard false for mouse
        if (self.vx == 0 and self.vy == 0) and keyBoolean:
            if event.key == pygame.K_UP:
                self.vy = -1
            elif event.key == pygame.K_DOWN:
                self.vy = 1
            elif event.key == pygame.K_LEFT:
                self.vx = -1
            elif event.key == pygame.K_RIGHT:
                self.vx = 1

        if keyBoolean:
            if event.key == pygame.K_UP:
                if self.vy == 1:
                    return
                self.vx = 0
                self.vy = -1
            elif event.key == pygame.K_DOWN:
                if self.vy == -1:
                    return
                self.vx = 0
                self.vy = 1
            elif event.key == pygame.K_LEFT:
                if self.vx == 1:
                    return
                self.vx = -1
                self.vy = 0
            elif event.key == pygame.K_RIGHT:
                if self.vx == -1:
                    return
                self.vx = 1
                self.vy = 0

        else:    ## play snake with mouse| get_pressed method returns bool tuple (left, middle, right) True for the mouse button pressed, False otherwise
            if pygame.mouse.get_pressed()[0] == True:
                x,y = event.pos
                if  self.vx == 1 or self.vx == -1:
                    if y < self.y:
                        self.vx = 0
                        self.vy = -1
                    else:
                        self.vx = 0
                        self.vy = 1
                elif  self.vy == 1 or self.vy == -1:
                    if x < self.x:
                        self.vx = -1
                        self.vy = 0
                    else:
                        self.vx = 1
                        self.vy = 0


    def move(self):
      #can also be done with vectors
      ## Move the Snake pos + "velocity"
        if self.vx >0 :
            self.x += self.vx + self.size
        elif self.vx <0 :
            self.x += self.vx - self.size
        elif self.vy >0:
            self.y += self.vy + self.size
        elif self.vy <0:
            self.y += self.vy - self.size

        ## calls obstacle class update method
        #self.sprites.update((self.vx,self.vy)) # updates whole snake
        # the previous line needs to be fixed update not working correctly

        #create more Snake
        block = Obstacle(self.color,(self.x,self.y),(self.size,self.size),black)
        self.surfaceBody.insert(0,block) ## inserts item in list at given position (0)
        self.sprites.add(self.surfaceBody[0])


        if (self.grow_to > self.length): ## initially the Snake "grows" to 50 size units (rectangles)
            self.length += 1

        if len(self.surfaceBody) > self.length:
            tmpS = self.surfaceBody.pop()
            self.sprites.remove(tmpS)


        ## snake eats itself
        sprite = self.surfaceBody[0] # takes head of snake
        # removes 1st element so head doesnt collide with it
        self.sprites.remove(self.surfaceBody[0])
        group = self.sprites
        if pygame.sprite.spritecollide(sprite,group,False):
            self.invalidMove = True

        self.sprites.add(self.surfaceBody[0])


    def draw(self):
        # draws next pixel erases last
        #creates a surface with the background color
        backgroundSurface = pygame.Surface(self.surface.get_size())
        backgroundSurface.fill(black)
        self.surfaceBody[-1].kill()
        self.sprites.clear(self.surface,backgroundSurface)
        self.sprites.draw(self.surface) # calls obstacle class draw method


    def getCrashState(self):
        if self.crashed:
            self.crashed = not self.crashed ## inverts crash state
            return True
        return False
