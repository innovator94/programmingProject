import pygame
from settings import *

#For the wall sprite
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        
        super().__init__(groups)
        
        self.sprite_type = 'tile'
        
        self.image = pygame.image.load("programming project 2/assets/tile.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -10)