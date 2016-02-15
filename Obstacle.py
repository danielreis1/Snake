import pygame
import random
import sys
from Utils import *

class Obstacle(pygame.sprite.Sprite):
    # pos and size are tuples
    # try using sprites (extend from sprite class)
    def __init__(self,color,centerPos,size,backgroundColor):
        super().__init__()
        self.color = color
        self.size = size
        self.backgroundColor = backgroundColor
        # can make method to load an image
        self.surface = pygame.Surface(size)
        self.image = self.surface
        self.center = centerPos  #obstacle center in background surface
        self.surface.fill(color)
        self.rect = self.surface.get_rect(center = centerPos)
        self.surface.set_colorkey(self.backgroundColor) # pixels in obstacle with this color are transparent in the background

    def update(self,vel=(0,0)):
        # rectangle doesnt move by default
        # get snake
        if vel == (0,0):
            return
        else:
            self.rect.move(vel)
