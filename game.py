import time

import pygame
from start_screen import Start_Screen


class Game:
    def __init__(self):
        self.actions = None
        pygame.init()
        self.GAME_W, self.GAME_H = 1920, 1080
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.SCREEN_RATIO = 1080/1920
        self.size_change_ratio = 0
        pygame.display.set_caption("The Sewers")

        self.fullscreen = False
        self.clock = pygame.time.Clock()
        self.scale = 1
        self.running = True
        self.fullscreen = False
        self.dt, self.prev_time = 0, 0
        self.init_keys_states()
        self.state_stack = []
        self.load_assets()
        self.load_states()

    def run(self):
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(60)

    def init_keys_states(self):
        self.actions = {"left": False, "right": False, "up": False, "down": False, "mouse_move": False,
                        "mouse_left_click": False, "mouse_right_click": False,
                        "capital_letter": False, "escape": False, "backspace": False, "space": False, "scroll_up": False
                        , "scroll_down": False
                        , "a": False, "b": False, "c": False, "d": False, "e": False, "f": False
                        , "g": False, "h": False, "i": False, "j": False, "k": False, "l": False, "m": False, "n": False
                        , "o": False, "p": False, "r": False, "s": False, "t": False, "u": False, "w": False, "x": False
                        , "y": False, "z": False, "0": False, "1": False, "2": False, "3": False, "4": False, "5": False
                        , "6": False, "7": False, "8": False, "9": False, "hold": {
                        "s_hold": False, "w_hold": False, "e_hold": False, "a_hold": False, "d_hold": False, "up_hold": False, "down_hold": False, "left_button_hold": False
            }}

    def clear_actions(self):
        for action in self.actions:
            if action != "hold":
                self.actions[action] = False

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def get_events(self):
        self.clear_actions()
        self.size_change_ratio = self.GAME_W / self.SCREEN_WIDTH
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.SCREEN_WIDTH = event.w
                    self.SCREEN_HEIGHT = self.SCREEN_WIDTH * self.SCREEN_RATIO
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.MOUSEMOTION:
                self.actions["mouse_move"] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions["mouse_left_click"] = True
                    self.actions["left_button_hold"] = True
                if event.button == 3:
                    self.actions["mouse_right_click"] = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions["left_button_hold"] = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    self.actions["scroll_up"] = True
                if event.y == -1:
                    self.actions["scroll_down"] = True
            if pygame.key.get_mods() & (pygame.KMOD_SHIFT | pygame.KMOD_CAPS):
                self.actions["capital_letter"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.actions["hold"]["up_hold"] = False
                if event.key == pygame.K_DOWN:
                    self.actions["hold"]["down_hold"] = False
                if event.key == pygame.K_a:
                    self.actions["hold"]["a_hold"] = False
                if event.key == pygame.K_d:
                    self.actions["hold"]["d_hold"] = False
                if event.key == pygame.K_e:
                    self.actions["hold"]["e_hold"] = False
                if event.key == pygame.K_w:
                    self.actions["hold"]["w_hold"] = False
                if event.key == pygame.K_s:
                    self.actions["hold"]["s_hold"] = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.actions["up"] = True
                    self.actions["hold"]["up_hold"] = True
                if event.key == pygame.K_DOWN:
                    self.actions["down"] = True
                    self.actions["hold"]["down_hold"] = True
                if event.key == pygame.K_LEFT:
                    self.actions["left"] = True
                if event.key == pygame.K_RIGHT:
                    self.actions["right"] = True
                if event.key == pygame.K_SPACE:
                    self.actions["space"] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions["escape"] = True
                if event.key == pygame.K_BACKSPACE:
                    self.actions["backspace"] = True
                if event.key == pygame.K_a:
                    self.actions["a"] = True
                    self.actions["hold"]["a_hold"] = True
                if event.key == pygame.K_b:
                    self.actions["b"] = True
                if event.key == pygame.K_c:
                    self.actions["c"] = True
                if event.key == pygame.K_d:
                    self.actions["d"] = True
                    self.actions["hold"]["d_hold"] = True
                if event.key == pygame.K_e:
                    self.actions["e"] = True
                    self.actions["hold"]["e_hold"] = True
                if event.key == pygame.K_f:
                    self.actions["f"] = True
                if event.key == pygame.K_g:
                    self.actions["g"] = True
                if event.key == pygame.K_h:
                    self.actions["h"] = True
                if event.key == pygame.K_i:
                    self.actions["i"] = True
                if event.key == pygame.K_j:
                    self.actions["j"] = True
                if event.key == pygame.K_k:
                    self.actions["k"] = True
                if event.key == pygame.K_l:
                    self.actions["l"] = True
                if event.key == pygame.K_m:
                    self.actions["m"] = True
                if event.key == pygame.K_n:
                    self.actions["n"] = True
                if event.key == pygame.K_o:
                    self.actions["o"] = True
                if event.key == pygame.K_p:
                    self.actions["p"] = True
                if event.key == pygame.K_r:
                    self.actions["r"] = True
                if event.key == pygame.K_s:
                    self.actions["s"] = True
                    self.actions["hold"]["s_hold"] = True
                if event.key == pygame.K_t:
                    self.actions["t"] = True
                if event.key == pygame.K_u:
                    self.actions["u"] = True
                if event.key == pygame.K_w:
                    self.actions["w"] = True
                    self.actions["hold"]["w_hold"] = True
                if event.key == pygame.K_x:
                    self.actions["x"] = True
                if event.key == pygame.K_y:
                    self.actions["y"] = True
                if event.key == pygame.K_z:
                    self.actions["z"] = True
                if event.key == pygame.K_0:
                    self.actions["0"] = True
                if event.key == pygame.K_1:
                    self.actions["1"] = True
                if event.key == pygame.K_2:
                    self.actions["2"] = True
                if event.key == pygame.K_3:
                    self.actions["3"] = True
                if event.key == pygame.K_4:
                    self.actions["4"] = True
                if event.key == pygame.K_5:
                    self.actions["5"] = True
                if event.key == pygame.K_6:
                    self.actions["6"] = True
                if event.key == pygame.K_7:
                    self.actions["7"] = True
                if event.key == pygame.K_8:
                    self.actions["8"] = True
                if event.key == pygame.K_9:
                    self.actions["9"] = True

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)
        self.clear_actions()

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.smoothscale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    def load_assets(self):
        pass

    def load_states(self):
        self.start_screen = Start_Screen(self, self.screen)
        self.state_stack.append(self.start_screen)

    def render_text(self, surface, text, text_color, x, y, scale):
        self.draw_text(surface, text, (0, 0, 0), x - 2, y - 2, scale)
        self.draw_text(surface, text, (0, 0, 0), x - 2, y + 2, scale)
        self.draw_text(surface, text, (0, 0, 0), x + 2, y - 2, scale)
        self.draw_text(surface, text, (0, 0, 0), x + 2, y + 2, scale)
        self.draw_text(surface, text, text_color, x, y, scale)

    def draw_text(self, surface, text, color, x, y, scale):
        font = pygame.font.Font("chainwhacks-font\\Chainwhacks-vm72E.ttf", int(35 * scale))
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

