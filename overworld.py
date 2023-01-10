from random import random, randint

import pygame
from clock import Clock
from lifebar import LifeBar
from map import Map
from map_config import MapConfig
from player import Player
from state import State
from weapon_menu import WeaponMenu
from weapons import Weapons


class CurrentWormArrow:
    def __init__(self):
        self.image = pygame.transform.smoothscale(pygame.image.load("images\\current_worm_arrow.png").convert_alpha(), (70, 70))
        self.position = [0, 0]
        self.position_change = 0
        self.y_change = 1

    def set_position(self, position):
        self.position = position
        self.position[0] += 15

    def update(self, delta_time, actions):
        if self.position_change == 20:
            self.y_change = -1
        if self.position_change == -20:
            self.y_change = 1
        self.position_change += self.y_change

    def render(self, surface):
        surface.blit(self.image, (self.position[0], self.position[1] + self.position_change))


class Overworld(State):
    def __init__(self, game, playerA_name, playerB_name, map):
        State.__init__(self, game)
        self.playerB_resp_points = None
        self.playerA_resp_points = None
        self.map = map
        self.player1_name = playerA_name
        self.player2_name = playerB_name
        self.current_player = None
        self.all_worms = []
        self.clock = Clock(game, self)

        self.weapons = Weapons()
        self.weapon_menu = WeaponMenu(game, self.weapons, self)
        self.current_worm_arrow = CurrentWormArrow()
        self.map_config = MapConfig(map)
        self.draw_resp_points()
        self.map = Map(map)
        self.generate_players()
        self.generate_players_lifebars()
        self.winner = None
        pygame.mixer.music.load("sounds\\in_game.mp3")
        pygame.mixer.music.set_volume(0.07)
        pygame.mixer.music.play(-1)

    def draw_resp_points(self):
        playerA_resp_points = []
        playerB_resp_points = []
        resp_points = self.map_config.get_render_points()
        while len(playerA_resp_points) < 3:
            r = randint(0, len(resp_points) - 1)
            if r not in playerA_resp_points:
                playerA_resp_points.append(r)
        while len(playerB_resp_points) < 3:
            r = randint(0, len(resp_points) - 1)
            if r not in playerA_resp_points and r not in playerB_resp_points:
                playerB_resp_points.append(r)

        self.playerA_resp_points = [resp_points[playerA_resp_points[0]], resp_points[playerA_resp_points[1]], resp_points[playerA_resp_points[2]]]
        self.playerB_resp_points = [resp_points[playerB_resp_points[0]], resp_points[playerB_resp_points[1]], resp_points[playerB_resp_points[2]]]

    def generate_players(self):
        self.playerA = self.current_player = Player(self.player1_name, "pink", self.playerA_resp_points, self.weapons, self.weapon_menu, self)
        self.playerB = Player(self.player2_name, "blue", self.playerB_resp_points, self.weapons, self.weapon_menu, self)

    def generate_players_lifebars(self):
        self.barA = LifeBar(self.game, self.playerA, 1400, 0.90, (173, 61, 155))
        self.barB = LifeBar(self.game, self.playerB, 1400, 0.95, (50, 151, 168))

    def change_player(self):
        if self.current_player == self.playerA:
            self.current_player = self.playerB
        else:
            self.current_player = self.playerA

        self.current_player.change_worm()

    def check_is_game_over(self):
        if self.barA.value <= 0:
            self.winner = self.player2_name + " won"
        if self.barB.value <= 0:
            self.winner = self.player1_name + " won"

    def update(self, delta_time, actions):
        if self.winner is None:
            self.playerA.update(delta_time, actions)
            self.playerB.update(delta_time, actions)
            self.barA.update(delta_time, actions)
            self.barB.update(delta_time, actions)
            self.map.update(delta_time, actions)
            self.weapon_menu.update(delta_time, actions)
            self.current_worm_arrow.update(delta_time, actions)
            self.clock.update(delta_time, actions)
            self.check_is_game_over()
        elif actions["mouse_left_click"]:
            self.game.running = False

    def render(self, surface):
        if self.winner is not None:
            surface.fill((255, 255, 255))
        self.map.render(surface)
        self.playerA.render(surface)
        self.playerB.render(surface)
        self.barA.render(surface)
        self.barB.render(surface)
        self.clock.render(surface)
        self.weapon_menu.render(surface)
        self.current_worm_arrow.render(surface)
        if self.winner is not None:
            self.game.render_text(surface, self.winner, (249, 215, 28), 960, 540, 10)