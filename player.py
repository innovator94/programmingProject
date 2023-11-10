import pygame
from settings import *
from bullet import Bullet
from points import*

#Player class to spawn player into the game
class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, boundary_sprites, screen_sprites, state_change):
        
        super().__init__(groups)
        
        #Sprite display
        self.image = pygame.image.load("programming project 2/assets/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.sprite_type = 'player'
        
        self.boundary_sprites = boundary_sprites
        self.screen_sprites = screen_sprites
        
        #Player stats/(non-compsci)attributes
        self.v = pygame.math.Vector2()
        self.speed = 5
        
        self.hitbox = self.rect.inflate(0, -26)
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        
        self.health = 100
        self.health_curr = self.health
        
        self.points = 0
        
        #Death
        
        self.state_change = state_change
    
    def take_damage(self, damage):
        if self.health_curr > 0:
            self.health_curr -= damage
        else:
            self.state_change("Dead")
    
    #Adds points upon every killing of an enemy
    def add_point(self):
        self.points += 1
    
    #Create bullet
    def shoot(self):
        Bullet((self.rect.x + 24, self.rect.y + 20), [self.screen_sprites], self.boundary_sprites, self.screen_sprites, self.add_point)
    
    #Take keyboard and mouse presses and react accordingly
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.v.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.v.y = 1
        else:
            self.v.y = 0
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.v.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.v.x = -1
        else:
            self.v.x = 0
            
        if pygame.mouse.get_pressed()[0] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.shoot()
        
    #Move rectangle for player
    def move(self, speed):
        if self.v.magnitude() != 0:
            self.v = self.v.normalize()
            
        self.hitbox.x += self.v.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.v.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
        
    #Stop moving if hit wall
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.boundary_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.v.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.v.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.boundary_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.v.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.v.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    #So that the player can't infinitely attack
    def cooldown(self):
        curr_time = pygame.time.get_ticks()
        
        if self.attacking:
            if curr_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    #Continuously runs these functions
    def update(self):
        self.input()
        self.cooldown()
        self.move(self.speed)