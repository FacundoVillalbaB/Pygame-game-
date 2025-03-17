import pygame 
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,-26)

		#Animations
		self.import_player_assets()
		self.status = 'down'

		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

		#attack
		self.attacking =False
		self.attack_cooldown = 400
		self.attack_time = None
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack

		#stats
		self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 5}
		self.health = self.stats['health'] * 0.5
		self.speed = self.stats['speed']
		self.kill_count = 0

		#damage timer
		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

		#sound
		self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.4)

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {'up': [],'down':[],'left': [],'right':[],'up_idle': [],'down_idle':[],'left_idle': [],'right_idle':[],'up_attack': [],'down_attack':[],'left_attack': [],'right_attack':[]}
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)
		print(self.animations)

	#movement
	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0

		#attack
		if keys[pygame.K_q] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			self.create_attack()
			self.weapon_attack_sound.play()

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data['sword']['damage']

		return base_damage + weapon_damage

	def get_status(self):
		#idle
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'
		#attack
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '')

	def animate(self):
		animation=self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		#set image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldown(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data['sword']['cooldown']:
				self.attacking = False
				self.destroy_attack()
		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

	def update(self):
		self.input()
		self.cooldown()
		self.get_status()
		self.animate()
		self.move(self.speed)