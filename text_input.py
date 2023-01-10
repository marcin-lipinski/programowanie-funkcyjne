import re

import pygame
from state import State


class TextInput(State):
    def __init__(self, x, y, comment, width, height, game):
        State.__init__(self, game)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.text_surface = pygame.Surface((width/2 + 40, height), pygame.SRCALPHA)
        self.text_surface_color = [249, 215, 28, 64]
        self.comment_surface = pygame.Surface((width/2 - 50, height), pygame.SRCALPHA)

        self.basic_size = (x, y, width, height)
        self.mouse_on = False
        self.is_writable = False
        self.written_text = ""
        self.comment = comment
        self.focused_on = False

    def update(self, actions):
        sc = self.game.GAME_W / self.game.SCREEN_WIDTH

        if actions["mouse_move"]:
            x, y = pygame.mouse.get_pos()
            x *= sc
            y *= sc
            if self.basic_size[0] + 110 <= x <= self.basic_size[0] + self.basic_size[2]:
                if self.basic_size[1] <= y <= self.basic_size[1] + self.basic_size[3]:
                    self.mouse_on = True
                else:
                    self.mouse_on = False
            else:
                self.mouse_on = False

        if self.mouse_on:
            self.text_surface_color[3] = 128
        elif not self.focused_on:
            self.text_surface_color[3] = 64

        if actions["mouse_left_click"]:
            if self.mouse_on:
                self.text_surface_color[3] = 128
                self.focused_on = True
            else:
                self.text_surface_color[3] = 64
                self.focused_on = False

        if self.focused_on:
            if actions["backspace"]:
                self.written_text = self.written_text[:-1]
            if actions["space"]:
                self.written_text += "  "
            for key in "abcdefghijklmnoprstuwxyz0123456789":
                if actions[key]:
                    self.written_text += key


    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))
        rect = self.text_surface.get_rect()
        rect.x, rect.y = 0, 0
        pygame.draw.rect(self.text_surface, self.text_surface_color, rect, 0, 25)
        self.game.render_text(self.text_surface, self.written_text, (255, 255, 255), self.text_surface.get_width() / 2, self.text_surface.get_height() / 2, 1)
        self.surface.blit(self.text_surface, (self.basic_size[2]/2 - 40, 0))

        self.game.render_text(self.comment_surface, self.comment, (255, 255, 255), self.comment_surface.get_width()/2, self.comment_surface.get_height()/2, 1)
        self.surface.blit(self.comment_surface, (0, 0))

        surface.blit(self.surface, (self.basic_size[0], self.basic_size[1]))

