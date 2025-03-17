import pygame
import sys
from level import Level
from settings import *
from enemy import Enemy


class Game:

	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()

		self.level = Level()

		#sound
		##main_sound = pygame.mixer.Sound('../audio/main.ogg')
		#main_sound.play(loops = -1) #infinite loop for music
		#main_sound.set_volume(0.05)




	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('white')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()