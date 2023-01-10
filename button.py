import pygame


class TextButton:
    def __init__(self, x, y, width, height, text, text_color, game, click_function, parent):
        self.surface = pygame.Surface((game.GAME_W, game.GAME_H), pygame.SRCALPHA).convert_alpha()
        self.rect = pygame.Rect(x, y, width, height)
        self.rect_size_basic = (x, y, width, height)
        self.text = text
        self.scale = 1
        self.game = game
        self.parent = parent
        self.text_color = text_color
        self.click_function = click_function
        self.mouse_on = False

    def update(self, actions):
        x, y = pygame.mouse.get_pos()
        x = x * self.game.size_change_ratio
        y = y * self.game.size_change_ratio

        if actions["mouse_move"]:
            if self.rect.collidepoint(x, y):
                self.text_color = (249, 215, 28)
                if self.scale < 1.2:
                    self.scale += 0.1
            else:
                self.text_color = (255, 255, 255)
                if self.scale > 1:
                    self.scale -= 0.1

        new_width = self.rect_size_basic[2] * self.scale
        new_height = self.rect_size_basic[3] * self.scale
        new_x = self.rect_size_basic[0] - (new_width - self.rect_size_basic[2])/2
        new_y = self.rect_size_basic[1] - (new_height - self.rect_size_basic[3])/2
        self.rect.update(new_x, new_y, new_width, new_height)

        if actions["mouse_left_click"]:
            if self.rect.collidepoint(x, y):
                self.click_function(self)

    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))
        self.game.render_text(self.surface, self.text, self.text_color, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2,  self.scale)
        surface.blit(self.surface, (0, 0))
