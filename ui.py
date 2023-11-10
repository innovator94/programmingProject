import pygame

class UI:
    def __init__(self):
        self.display_screen = pygame.display.get_surface()
        self.font = pygame.font.Font("programming project 2/assets/Monocraft.ttf", 18)
        self.health_bar_rect = pygame.Rect(10, 450, 200, 20)
    
    #Creates red rectangle on screen, size dictated by Player.health   
    def show_bar(self, current, max_amount, bg_rect, colour):
        pygame.draw.rect(self.display_screen, '#222222', bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_screen, colour, current_rect)
    
    #Draws above bar onto screen
    def display(self, player):
        self.show_bar(player.health_curr, player.health, self.health_bar_rect, 'red')
        
