import pygame
import json

from state import State
from worm import Worm


class Player(State):
    def __init__(self, name, sprite_color, resp_positions, weapons, weapon_menu, overworld):
        self.name = name
        self.overworld = overworld
        self.sprite_color = sprite_color
        self.life_points = 0
        self.load_spritesheet(sprite_color)
        self.worms = []
        self.current_worm = None
        self.current_worm_number = 0
        self.create_worms(resp_positions, weapons, weapon_menu)

    def load_spritesheet(self, color):
        file = open("jsons\\slime.json")
        data = json.load(file)[color]
        file.close()
        self.spritesheet = {"move_left": [], "move_right": [], "jump_left": [], "jump_right": [], "death": []}
        for i in data["move"]:
            image = pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), [99, 80])
            self.spritesheet["move_right"].append(image)
            self.spritesheet["move_left"].append(pygame.transform.flip(image, True, False))

        for i in data["jump"]:
            image = pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), [99, 80])
            self.spritesheet["jump_right"].append(image)
            self.spritesheet["jump_left"].append(pygame.transform.flip(image, True, False))
        for i in data["death"]:
            image = pygame.transform.smoothscale(pygame.image.load(i).convert_alpha(), [99, 80])
            self.spritesheet["death"].append(image)

    def create_worms(self, resp_positions, weapons, weapon_menu):
        for i in range(3):
            self.worms.append(Worm(self, 10, 10, resp_positions[i], self.spritesheet, weapons, weapon_menu))
            self.overworld.all_worms.append(self.worms[i])
        self.current_worm = self.worms[self.current_worm_number]

    def check_are_alive(self):
        for i in range(3):
            if self.worms[i].alive:
                return True
        return False

    def change_worm(self):
        if self.check_are_alive():
            self.current_worm_number = (self.current_worm_number + 1) % 3
            if self.worms[self.current_worm_number].alive:
                self.current_worm = self.worms[self.current_worm_number]
            else:
                self.change_worm()
        else:
            self.overworld.check_is_game_over()

        self.current_worm.movement["shooting"] = False

    def update(self, delta_time, actions):
        self.life_points = self.worms[0].life_points + self.worms[1].life_points + self.worms[2].life_points
        for worm in self.worms:
            worm.update(delta_time, actions)

    def render(self, surface):
        for worm in self.worms:
            worm.render(surface)
