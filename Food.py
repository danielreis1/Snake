import pygame
import random
from Utils import *

## food class
class Food:
 def __init__(self, surface,radius):
  self.surface = surface
  self.x = 0
  self.y = 0
  self.color = white
  self.radius = radius
  self.foodCount = 0

 def set_surface(self,surface):
  self.surface = surface


 def setColor(self, cor):
  self.color = cor

 def foodCoords(self):
  if self.foodCount < 1: ## checks if there is already food
   self.x = random.randint(0, self.surface.get_width())
   self.y = random.randint(0, self.surface.get_height())
  return (self.x , self.y)

 def draw(self):
  if self.foodCount < 1:
   self.foodCount+=1
   pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)

 def erase(self):
  self.foodCount -=1
  pygame.draw.circle(self.surface, (0, 0, 0), (self.x, self.y), self.radius)
  self.x = 0
  self.y = 0

 def decreaseFood(self):
  self.foodCount-=1

 def check(self, x, y):
  radius = int(self.radius)
  # + and - constants for object center offset
  if x < self.x - radius - 3 or x > self.x + radius:
   return False
  elif y < self.y - radius -3 or y > self.y + radius:
   return False
  else:
   return True

 def redraw(self):
  pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)
