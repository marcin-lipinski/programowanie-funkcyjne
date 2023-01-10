from button import TextButton
from overworld import Overworld
from map_board import Map_Board
from state import State
from text_input import TextInput


def play_game(self):
    config = self.parent.can_start()
    if config:
        self.parent.start_screen.exit_state()
        self.game.state_stack.append(Overworld(self.game, config[0], config[1], config[2]))


def return_function(self):
    self.parent.start_screen.state["main_menu"] = True
    self.parent.start_screen.state["new_game_config"] = False


class New_Game_Screen(State):
    def __init__(self, game, start_screen):
        State.__init__(self, game)
        self.start_screen = start_screen
        self.map_one = "images\\map_1.png"
        self.map_two = "images\\map_2.png"
        self.maps = self.generate_map()
        self.buttons = self.generate_buttons()
        self.text_inputs = self.generate_input()

    def generate_map(self):
        map_1 = Map_Board(100, 120, 760, 760 * self.game.SCREEN_RATIO, self.game, self.map_one, self)
        map_2 = Map_Board(1060, 120, 760, 760 * self.game.SCREEN_RATIO, self.game, self.map_two, self)
        return [map_1, map_2]

    def generate_buttons(self):
        start_button = TextButton(self.game.GAME_W * 0.5 - 200, self.game.GAME_H * 0.85, 200, 75, "PLAY", (255, 255, 255), self.game, play_game, self)
        exit_button = TextButton(self.game.GAME_W * 0.5, self.game.GAME_H * 0.85, 200, 75, "RETURN", (255, 255, 255), self.game, return_function, self)
        return [start_button, exit_button]

    def generate_input(self):
        player_1 = TextInput(50,  self.game.GAME_H * 0.5 + 100, "Player 1", 600, 75, self.game)
        player_2 = TextInput(50,  self.game.GAME_H * 0.5 + 200, "Player 2", 600, 75, self.game)
        return [player_1, player_2]

    def can_start(self):
        config = dict()
        for t in self.text_inputs:
            if len(t.written_text) < 1:
                return False
            config[t.written_text] = t.written_text

        for m in self.maps:
            if m.locked:
                config[m.image_source] = m.image_source[:-4]
        if len(list(config.keys())) < 3:
            return False
        return list(config.values())

    def update(self, delta_time, actions):
        for m in self.maps:
            m.update(actions)
        for b in self.buttons:
            b.update(actions)
        for t in self.text_inputs:
            t.update(actions)

    def render(self, surface):
        self.game.render_text(surface, "Choose map", (255, 255, 255), 200, 50, 1)
        for m in self.maps:
            m.render(surface)
        for b in self.buttons:
            b.render(surface)
        for t in self.text_inputs:
            t.render(surface)


