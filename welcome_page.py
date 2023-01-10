import pygame

from button import TextButton
from state import State


def quit_function(self):
    self.game.running = False


def start_game(self):
    self.parent.start_screen.main_menu = False


class Welcome_Page(State):
    def __init__(self, game, start_screen):
        State.__init__(self, game)
        self.start_screen = start_screen
        self.game_title = pygame.transform.smoothscale(pygame.image.load("images\\game_logo.png").convert_alpha(), (game.GAME_W, game.GAME_H))
        self.buttons = self.generate_buttons()

    def generate_buttons(self):
        start_button = TextButton(self.game.GAME_W * 0.5 - 100, self.game.GAME_H * 0.6 - 37.5, 200, 75, "START", (255, 255, 255), self.game, start_game, self)
        exit_button = TextButton(self.game.GAME_W * 0.5 - 100, self.game.GAME_H * 0.8 - 37.5, 200, 75, "EXIT", (255, 255, 255), self.game, quit_function, self)
        return [start_button, exit_button]

    def update(self, delta_time, actions):
        for b in self.buttons:
            b.update(actions)

    def render(self, surface):
        surface.blit(self.game_title, (0, 0))
        for b in self.buttons:
            b.render(surface)
