import pygame.surface


class WeaponBoard:
    def __init__(self, name, weapon_config, game):
        self.game = game
        self.config = weapon_config
        self.name = name
        self.surface = pygame.surface.Surface((200, 200), pygame.SRCALPHA).convert_alpha()
        self.image = pygame.transform.smoothscale(pygame.image.load(weapon_config["image"]).convert_alpha(), (170, 170))
        self.position = weapon_config["position"]
        self.ammo_state = weapon_config["initial_ammo"]
        self.highlight = False

    def set_ammo_state(self, ammo_state):
        self.ammo_state = ammo_state

    def update(self):
        self.surface.fill((0, 0, 0, 0))
        if self.highlight:
            pygame.draw.rect(self.surface, (249, 215, 28), (0, 0, 200, 200), 0, 10)
        self.surface.blit(self.image, (15, 0))
        self.game.render_text(self.surface, str(self.ammo_state), (255, 255, 255), 100, 175, 0.9)

    def render(self, surface):
        surface.blit(self.surface, self.position)


class WeaponMenu:
    def __init__(self, game, weapons, overworld):
        self.game = game
        self.surface = pygame.surface.Surface((560, 1080), pygame.SRCALPHA).convert_alpha()
        self.arrow = pygame.surface.Surface((100, 100), pygame.SRCALPHA).convert_alpha()
        self.weapon_board = pygame.surface.Surface((460, 1080))
        self.weapon_boards = []
        self.load_weapon_boards(weapons.get_all_weapons())
        self.state = "closed"
        self.position = [1820, 0]
        self.mouse_on_arrow = False
        self.mouse_on_weapon = None
        self.is_transition = False
        self.transition_counter = 560
        self.arrow_color = (255, 255, 255)
        self.arrow_sign = "<"
        self.weapons = weapons
        self.overworld = overworld

    def load_weapon_boards(self, weapons):
        for w in weapons:
            self.weapon_boards.append(WeaponBoard(w, weapons[w], self.game))

    def update_ammo_state(self, ammo_state):
        for wb in self.weapon_boards:
            wb.set_ammo_state(ammo_state[wb.name].ammo)

    def update(self, delta_time, actions):
        if self.is_transition:
            self.handle_transition()
        elif not self.overworld.current_player.current_worm.weapon.weapons[self.overworld.current_player.current_worm.weapon.current_weapon].in_action:
            self.handle_mouse_events(actions["mouse_move"], actions["mouse_left_click"])

        for w in self.weapon_boards:
            w.update()

    def handle_transition(self):
        if self.state == "opened":
            if self.position[0] > 1360:
                self.position[0] -= 60
            else:
                self.is_transition = False
        if self.state == "closed":
            if self.position[0] < 1820:
                self.position[0] += 60
            else:
                self.is_transition = False

    def handle_mouse_events(self, mm, mc):
        sc = self.game.GAME_W / self.game.SCREEN_WIDTH
        if mm:
            x, y = pygame.mouse.get_pos()
            x = x * sc
            y = y * sc
            if self.state == "closed":
                self.mouse_on_weapon = None
                if 1820 <= x <= 1920 and 0 <= y <= 100:
                    self.arrow_color = (249, 215, 28)
                    self.mouse_on_arrow = True
                else:
                    self.arrow_color = (255, 255, 255)
                    self.mouse_on_arrow = False

            else:
                if 1360 <= x:
                    if x <= 1460 and 0 <= y <= 100:
                        self.arrow_color = (249, 215, 28)
                        self.mouse_on_arrow = True
                    else:
                        self.arrow_color = (255, 255, 255)
                        self.mouse_on_arrow = False
                        for w in self.weapon_boards:
                            if w.position[0] + 1460 <= x <= w.position[0] + 1660 and w.position[1] <= y <= w.position[1] + 200:
                                w.highlight = True
                                self.mouse_on_weapon = w
                            else:
                                w.highlight = False
                else:
                    self.arrow_color = (255, 255, 255)
                    self.mouse_on_arrow = False
                    if self.mouse_on_weapon is not None:
                        self.mouse_on_weapon.highlight = False
                    self.mouse_on_weapon = None

        if mc:
            if self.mouse_on_arrow:
                if self.state == "closed":
                    self.state = "opened"
                    self.arrow_sign = ">"
                    self.is_transition = True
                else:
                    self.state = "closed"
                    self.arrow_sign = "<"
                    self.is_transition = True
                    if self.mouse_on_weapon is not None:
                        self.mouse_on_weapon.highlight = False
            elif self.mouse_on_weapon is not None:
                self.overworld.current_player.current_worm.weapon.set_current_weapon(self.mouse_on_weapon.name)
                self.state = "closed"
                self.arrow_sign = "<"
                self.is_transition = True
                self.mouse_on_weapon.highlight = False

    def render(self, surface):
        self.arrow.fill((0, 0, 0, 0))
        pygame.draw.rect(self.arrow, (87, 93, 145), (0, 0, 100, 100), 0, -1, 30, -1, 30)
        self.game.render_text(self.arrow, self.arrow_sign, self.arrow_color, 50, 50, 2)
        self.weapon_board.fill((129, 132, 150))
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.arrow, (0, 0))
        for w in self.weapon_boards:
            w.render(self.weapon_board)
        self.surface.blit(self.weapon_board, (100, 0))
        surface.blit(self.surface, self.position)
