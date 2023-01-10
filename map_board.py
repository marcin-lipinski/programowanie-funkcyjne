import pygame

from state import State


class Map_Board(State):
    def __init__(self, x, y, width, height, game, image, parent):
        State.__init__(self, game)
        self.surface = pygame.Surface((width, height))
        self.image_source = image
        self.image = pygame.image.load(self.image_source)
        self.basic_size = (x, y, width, height)
        self.current_size = (x, y, width, height)
        self.border_color = (255, 255, 255)
        self.scale = 1
        self.mouse_on = False
        self.locked = False
        self.parent = parent

    def update(self, actions):
        sc = self.game.GAME_W / self.game.SCREEN_WIDTH

        if actions["mouse_move"]:
            x, y = pygame.mouse.get_pos()
            x *= sc
            y *= sc
            if self.current_size[0] <= x <= self.current_size[0] + self.current_size[2]:
                if self.current_size[1] <= y <= self.current_size[1] + self.current_size[3]:
                    self.mouse_on = True
                else:
                    self.mouse_on = False
            else:
                self.mouse_on = False

        if self.mouse_on:
            self.border_color = (249, 215, 28)
            if self.scale < 1.15:
                self.scale += 0.05
        elif not self.locked:
            self.border_color = (255, 255, 255)
            if self.scale > 1:
                self.scale -= 0.05

        new_width = self.basic_size[2] * self.scale
        new_height = self.basic_size[3] * self.scale
        new_x = self.basic_size[0] - (new_width - self.basic_size[2]) / 2
        new_y = self.basic_size[1] - (new_height - self.basic_size[3]) / 2
        self.current_size = (new_x, new_y, new_width, new_height)

        if actions["mouse_left_click"]:
            if self.mouse_on:
                self.locked = not self.locked
                for m in self.parent.maps:
                    if not m == self:
                        m.locked = False

    def render(self, surface):
        surface2 = pygame.Surface((self.current_size[2], self.current_size[3]))
        image = pygame.transform.scale(self.image, (self.current_size[2] - 20 * self.scale, self.current_size[3] - 20 * self.scale))
        surface2.fill(self.border_color)
        surface2.blit(image, (10, 10))
        surface.blit(surface2, (self.current_size[0], self.current_size[1]))

