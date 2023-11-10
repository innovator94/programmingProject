import pygame
from settings import *
from tile import *
from player import *
from points import *
from ui import UI
from enemy import Enemy

class Level:
	def __init__(self, state_change):
		#Screen and sprites
		self.display_screen = pygame.display.get_surface()
		self.screen_sprites = CameraGroupY()
		self.boundary_sprites = pygame.sprite.Group()
		self.state_change = state_change
		self.map_positions()
		self.ui = UI()
	
	#What are we spawning and where
	def map_positions(self):
		for row_index, row in enumerate(playable_world):
			for col_index, col in enumerate(row):
				x = col_index * 32
				y = row_index * 32
				if col == "x":
					Tile((x, y), [self.screen_sprites, self.boundary_sprites])
				if col == "p":
					self.player = Player((x, y), [self.screen_sprites], self.boundary_sprites, self.screen_sprites, self.state_change)
				if col == "f":
					Enemy("fire", (x, y), [self.screen_sprites], self.boundary_sprites, self.screen_sprites)
				if col == "w":
					Enemy("water", (x, y), [self.screen_sprites], self.boundary_sprites, self.screen_sprites)
				if col == "b":
					Enemy("bubble", (x, y), [self.screen_sprites], self.boundary_sprites, self.screen_sprites)

	#Actually drawing the sprites in
	def run(self):
		self.screen_sprites.remix_draw(self.player)
		self.screen_sprites.update()
		self.screen_sprites.enemy_update(self.player)
		self.ui.display(self.player)
		show_points(self.player.points)

#Keeps the player centred on the screen
class CameraGroupY(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_screen = pygame.display.get_surface()
		self.half_width = self.display_screen.get_size()[0] // 2
		self.half_height = self.display_screen.get_size()[1] // 2
		self.offset = pygame.math.Vector2(100, 200)
	
	def remix_draw(self, player):

		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height
     
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_coord = sprite.rect.topleft - self.offset
			self.display_screen.blit(sprite.image, offset_coord)

	def enemy_update(self, player):
		enemy_sprites = [sprite for sprite in self.sprites() if sprite.__class__.__name__ == "Enemy"]
		for enemy in enemy_sprites:
			enemy.enemy_update(player)