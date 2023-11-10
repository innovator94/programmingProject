import pygame
pygame.init()
font = pygame.font.Font("programming project 2/assets/Monocraft.ttf",30)
 
#Shows passed in parameter on the screen
def show_points(info,y = 430, x = 650):
    display_surface = pygame.display.get_surface()
    points_surface = font.render(str(info),True,'White')
    points_rect = points_surface.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surface, 'Black', points_rect.inflate(35, 5))
    display_surface.blit(points_surface, points_rect)