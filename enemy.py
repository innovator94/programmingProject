import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, boundary_sprites, screen_sprites):
        super().__init__(groups)
        #Sprite
        self.image = pygame.image.load(f"programming project 2/assets/{name}.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.sprite_type = 'enemy'
        
        #Movement related attributes
        self.hitbox = self.rect.inflate(0, -10)
        self.boundary_sprites = boundary_sprites
        self.screen_sprites = screen_sprites
        
        self.direction = pygame.math.Vector2()
        self.distance = None
        
        #Stats
        self.enemy_info = enemy_data[name]
        self.health = self.enemy_info["health"]
        self.damage = self.enemy_info["damage"]
        self.speed = self.enemy_info["speed"]
        self.attack_radius = self.enemy_info["attack_radius"]
        self.notice_radius = self.enemy_info["notice_radius"]
        
        self.attacking = False
        self.attack_cooldown = self.enemy_info["attack_cooldown"]
        
        self.hit = False
        self.hit_cooldown = 400
        
        self.dead = False
        
    #Where and how far away is the player
    def get_player_location(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        
        self.distance = (player_vector - enemy_vector).magnitude()
        
        if self.distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()
        
        return(self.distance, self.direction)
        
    #What is the enemy doing right now
    def change_state(self, player):
        distance = self.get_player_location(player)[0]
        
        if distance <= self.attack_radius and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.state = "attack"
        elif distance <= self.notice_radius:
            self.state = "move"
        else:
            self.state = "idle"
            
    #Deals damage to the enemy depending on if the enemy is able to get hit based on cooldown
    def take_damage(self):
        if not self.hit:
            self.health -= 100
            if self.health <= 0:
                self.dead = True
                self.kill()
            else:
                self.hit = True
                self.hit_time = pygame.time.get_ticks()
    
    #Tells the bullet if the enemy is dead            
    def is_dead(self):
        return self.dead
    
    #Depending on what the enemy is doing, what action must they perform
    def actions(self, player):
        if self.state == "attack":
            player.take_damage(self.damage)
            print(self.attack_time, player.health_curr)
        elif self.state == "move":
            self.direction = self.get_player_location(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    #Stops enemy from infinitely attacking
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        
        if self.hit:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.hit = False
            
    #Moves enemy
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
    
    #Stops enemy from no-clipping wall
    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.boundary_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.boundary_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    #Both continuously call the functions     
    def update(self):
        self.cooldowns()
        self.move(self.speed)
        
    def enemy_update(self, player):
        self.change_state(player)
        self.actions(player)