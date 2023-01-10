import pygame
from state import State


class LifeBar(State):
    def __init__(self, game, player, position_x, position_y, color):
        State.__init__(self, game)
        self.surface = pygame.Surface((392, 50), pygame.SRCALPHA)
        self.player_name_surface = pygame.Surface((140, 40), pygame.SRCALPHA)
        self.life_level_surface = pygame.Surface((230, 40), pygame.SRCALPHA)
        self.basic_size = (position_x, position_y * game.GAME_H, 392, 50)
        self.player = player
        self.value = self.init_value = player.life_points
        self.game.render_text(self.player_name_surface, self.player.name, (255, 255, 255), 70, 22.5, 0.8)
        self.color = color

    def update(self, delta_time, actions):
        self.value = self.player.life_points

    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))
        self.life_level_surface.fill((255, 255, 255, 0))

        temp_value = self.value / self.init_value
        rect_border = pygame.rect.Rect(5, 5, 224 * temp_value, 34)
        rect_fill = pygame.rect.Rect(5, 5, 224 * temp_value, 34)
        pygame.draw.rect(self.life_level_surface, self.color, rect_fill, 0, 10)
        pygame.draw.rect(self.life_level_surface, (0, 0, 0), rect_border, 3, 10)

        self.surface.blit(self.player_name_surface, (5, 5))
        self.surface.blit(self.life_level_surface, (157, 5))
        surface.blit(self.surface, (self.basic_size[0], self.basic_size[1]))
