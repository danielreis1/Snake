import pygame
import random
import sys
from Utils import *

class Obstacle(pygame.sprite.Sprite): 
    #pos and size are tuples
    def __init__(self,color,centerPos,size,backgroundColor):
        super().__init__()
        self.color = color
        self.size = size
        self.backgroundColor = backgroundColor
        # can make method to load an image
        self.surface = pygame.Surface(size)
        self.center = centerPos  #obstacle center in background surface        
        self.surface.fill(color)
        self.rect = self.surface.get_rect(center = centerPos)
        self.surface.set_colorkey(self.backgroundColor) # pixels in obstacle with this color are transparent in the background
        
        