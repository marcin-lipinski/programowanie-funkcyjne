import pygame
from state import State


class Clock(State):
    def __init__(self, game, overworld):
        State.__init__(self, game)
        self.overworld = overworld
        self.surface = pygame.Surface((200, 200), pygame.SRCALPHA)
        self.time = 30
        self.text_time = str(self.time)

    def change_player(self):
        self.overworld.change_player()

    def update(self, delta_time, actions):
        self.time -= delta_time
        if self.time <= 0 and not self.overworld.current_player.current_worm.weapon.weapons[self.overworld.current_player.current_worm.weapon.current_weapon].in_action:
            self.change_player()
            self.time = 30
        if self.time >= 0:
            self.text_time = str(self.time)[:2]
        else:
            self.text_time = "0."
        if self.text_time[1] not in "0123456789":
            self.text_time = " " + self.text_time[0]

    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))
        self.game.render_text(self.surface, self.text_time, (255, 255, 255), 50, 50, 1.5)
        surface.blit(self.surface, (0, 0))
