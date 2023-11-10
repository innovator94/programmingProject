import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, boundary_sprites, screen_sprites, add_point):
        super().__init__(groups)
        
        self.image = pygame.Surface((5, 5)).convert_alpha()
        self.image.fill("black")
        self.rect = self.image.get_rect(topleft = pos)
        self.boundary_sprites = boundary_sprites
        self.screen_sprites = screen_sprites
        
        self.set_direction()
        self.move()
        
        self.add_point = add_point
        
    def set_direction(self):
        self.direction = pygame.math.Vector2()
        self.direction.x = pygame.mouse.get_pos()[0] - 360
        self.direction.y = pygame.mouse.get_pos()[1] - 240
        
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
    def move(self):
        self.rect.x += self.direction.x * 5
        self.rect.y += self.direction.y * 5
        
        self.collision()
        
    def collision(self):
        for sprite in self.screen_sprites:
            if sprite.rect.colliderect(self.rect):
                if sprite.__class__.__name__ == "Tile":
                    self.kill()
                elif sprite.__class__.__name__ == "Enemy":
                    sprite.take_damage()
                    if sprite.is_dead():
                        self.add_point()
                    self.kill()
    
    def update(self):
        self.move()