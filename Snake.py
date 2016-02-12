
import pygame
import random
from Utils import *

class Worm():
 def __init__(self, surface, wormSize):
  self.surface = surface
  ## starts in the middle
  self.x = surface.get_width() / 2
  self.y = surface.get_height() / 2
  self.size = wormSize ## worm size in pixels "set worm square size"
  self.length = 1
  self.grow_to = 20
  ## "velocity x and y"
  self.vx = 0
  self.vy = 0  ## starts going up
  ## body is list of tuples (self.x, self.y)
  self.body = [] #can be a list of sprite objects to get use of sprite collision methods
  self.crashed = False ## state
  self.invalidMove = False
  self.color = 255, 255, 0 ## color assigned to tuple


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
  ## Move the worm pos + "velocity"
  if self.vx >0 :
   self.x += self.vx + self.size
  elif self.vx <0 :
   self.x += self.vx - self.size
  elif self.vy >0:
   self.y += self.vy + self.size
  elif self.vy <0:
   self.y += self.vy - self.size

  ## snake eats itself
  if (self.x, self.y) in self.body:
   self.invalidMove = True

  self.body.insert(0, (self.x, self.y)) ## inserts item in list at given position (0)

  if (self.grow_to > self.length): ## initially the worm "grows" to 50 size units (rectangles)
   self.length += 1

  if len(self.body) > self.length: ## pops out of the list the erased snake pieces by draw
   self.body.pop() ## list method pop() removes last item in the list


 def draw(self):
  # draws next pixel erases last pixel
  x, y = self.body[0] ## sets x,y to tuple value (x,y)
  pygame.draw.rect(self.surface,white,(x,y,self.size,self.size))
  ## 3rd argument represents a rectangle

  #self.surface.set_at((int(x), int(y)), self.color) ## set_at method in surface asks for int value argument -> writes a single pixel

  x, y = self.body[-1] #erase last
  rect = pygame.draw.rect(self.surface,black,(x,y,self.size,self.size))
  ##rectangle - (color,(top left corner coord, width, height))


 def redraw(self):
  # function to redraw snake after screen resize
  if (len(self.body) != 0):
      self.body.pop() ## erases last element (frame delay)
  for x,y in self.body:
      rect = pygame.draw.rect(self.surface,white,(x,y,self.size,self.size))
      rect.center = (x,y)

 def checkBoundaries(self):
  ## returns pos tuple
    if self.x <= 0 or self.x >= self.surface.get_width():
        self.crashed = True
    elif self.y <= 0 or self.y >= self.surface.get_height():
        self.crashed = True
    return (self.x,self.y)



 def getCrashState(self):
  if self.crashed :
   self.crashed = not self.crashed ## inverts crash state
   return True
  return False
