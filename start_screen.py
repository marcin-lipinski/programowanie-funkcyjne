import pygame
from button import *
from new_game_screen import New_Game_Screen
from state import State
from welcome_page import Welcome_Page


class Start_Screen(State):
    def __init__(self, game, screen):
        State.__init__(self, game)
        self.current_background_animation_frame = 0
        self.welcome_screen = Welcome_Page(self.game, self)
        self.new_game_screen = New_Game_Screen(self.game, self)
        self.background_image = pygame.transform.smoothscale(pygame.image.load("images\\tlo.png").convert_alpha(), (game.GAME_W, game.GAME_H))
        self.main_menu = True
        pygame.mixer.music.load("sounds\\menu.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def update(self, delta_time, actions):
        if self.main_menu:
            self.welcome_screen.update(delta_time, actions)
        else:
            self.new_game_screen.update(delta_time, actions)

    def render(self, surface):
        surface.fill((255, 255, 255))
        surface.blit(self.background_image, (0, 0))
        if self.main_menu:
            self.welcome_screen.render(surface)
        else:
            self.new_game_screen.render(surface)
