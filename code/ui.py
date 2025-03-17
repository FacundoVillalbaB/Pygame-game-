import pygame
from settings import *

class UI:
    def __init__(self):

        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

    def show_kill_count(self,kill_count):
        text_surf = self.font.render("kill count: " + str(int(kill_count)),False,TEXT_COLOR)
        x= self.display_surface.get_size()[0] - 20
        y= self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        self.display_surface.blit(text_surf,text_rect)
    def display(self,player):
        self.show_kill_count(player.kill_count)