import pygame


class Map:
    def __init__(self, source):
        self.source = source
        self.background = self.background_original = pygame.transform.smoothscale(pygame.image.load(source + "_background.png").convert_alpha(), (1920, 1080))
        self.front = self.front_original = pygame.transform.smoothscale(pygame.image.load(source + "_front.png"), (1920, 1080))
        self.zoom = 1.0
        self.size = [1920, 1080]
        self.click_x, self.click_y = 0, 0
        self.left_corner = [0, 0]
        self.right_bottom_corner = [1920, 1080]
        self.mask = pygame.mask.from_surface(self.front)

    def update(self, delta_time, actions):
        if actions["scroll_up"]:
            if self.zoom < 2.1:
                self.zoom += 0.1
                self.size = [1920 * self.zoom, 1080 * self.zoom]
                self.left_corner = [-self.left_corner[0] * self.zoom, -self.left_corner[1] * self.zoom]
                self.right_bottom_corner = [self.right_bottom_corner[0] * self.zoom, self.right_bottom_corner[1] * self.zoom]
        if actions["scroll_down"]:
            if self.zoom > 1.0:
                self.zoom -= 0.1
                self.size = [1920 * self.zoom, 1080 * self.zoom]
                self.left_corner = [-self.left_corner[0] / 2, -self.left_corner[1] * self.zoom]
                self.right_bottom_corner = [self.right_bottom_corner[0] * self.zoom, self.right_bottom_corner[1] * self.zoom]

        if actions["mouse_left_click"]:
            self.click_x = pygame.mouse.get_pos()[0]
            self.click_y = pygame.mouse.get_pos()[1]

        if actions["hold"]["left_button_hold"]:
            if actions["mouse_move"]:
                x, y = pygame.mouse.get_pos()
                x -= self.click_x
                y -= self.click_y
                self.click_x += x
                self.click_y += y

                # temp_size = [1920 * self.zoom, 1080 * self.zoom]
                # if self.left_corner[0] + x <= 0 and self.left_corner[1] + y <= 0:
                #     if self.right_bottom_corner[0] + x >= 1920 and self.right_bottom_corner[1] + y >= 1080:
                #         self.left_corner = [self.left_corner[0] + x, self.left_corner[1] + y]
                #         self.right_bottom_corner = [self.right_bottom_corner[0] + x, self.right_bottom_corner[1] + y]

        self.background = pygame.transform.smoothscale(self.background_original, self.size)
        self.front = self.front_original
        self.front.set_colorkey((0, 255, 0))
        self.mask = pygame.mask.from_surface(self.front)


    def render(self, surface):
        surface.blit(self.background, self.left_corner)
        surface.blit(self.front, self.left_corner)