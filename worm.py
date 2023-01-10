import pygame
from pygame.sprite import Sprite


class ArrowOfDirection:
    def __init__(self, position, worm):
        self.image = pygame.image.load("images\\current_direction_arrow.png").convert_alpha()
        self.worm = worm
        self.pivot = [position[0] + 49.5, position[1] + 50]
        self.angle = 0

    def update(self, delta_time, actions):
        if actions["up"] or actions["hold"]["up_hold"]:
            if self.angle < 176:
                self.angle += 5
        if actions["down"] or actions["hold"]["down_hold"]:
            if self.angle > 4:
                self.angle -= 5

        self.pivot = [self.worm.position[0] + 49.5, self.worm.position[1] + 50]

    def render(self, surface):
        rot_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rot_image.get_rect()
        new_rect.center = self.pivot
        surface.blit(rot_image, new_rect)


class Weapon:
    def __init__(self, position, weapons, worm):
        self.angle = 0
        self.weapons = weapons.new_set(worm)
        self.position = position
        self.current_weapon = "grenade"
        self.worm = worm
        self.powerbar = PowerBar(self.position)
        self.power = 0
        self.sight = pygame.transform.smoothscale(pygame.image.load("images\\sight.png").convert_alpha(), (100, 100))

    def set_position(self, position):
        self.position = position
        self.position = [self.position[0] + 49.5, self.position[1] + 40]

    def set_current_weapon(self, name):
        self.current_weapon = name

    def set_rotate(self, angle):
        self.angle = angle

    def shot(self, power):
        self.weapons[self.current_weapon].use(power, self.angle, self.position)

    def update(self, delta_time, actions):
        if self.current_weapon != "pistol" and self.current_weapon != "m4a1" and self.current_weapon != "machete" and self.current_weapon != "jetpack" and self.current_weapon != "first-aid-kit" and self.current_weapon != "flame-thrower" and self.current_weapon != "dynamite":
            if actions["hold"]["e_hold"]:
                if self.power < 99:
                    self.power += 2
                    self.powerbar.set_power(self.power)

            elif self.power > 0:
                if not self.worm.movement["shooting"]:
                    self.shot(self.power)
                    self.power = 0
                    self.worm.movement["shooting"] = True

        elif actions["e"]:
            if self.current_weapon == "jetpack":
                if not self.worm.movement["jetpack_on"]:
                    self.worm.movement["jetpack_on"] = True
                    self.weapons["jetpack"].in_action = True
                    self.worm.movement["shooting"] = True
                    self.shot(self.power)
                else:
                    self.weapons["jetpack"].in_action = False
                    self.worm.movement["jetpack_on"] = False
                    self.worm.movement["shooting"] = False
                    self.worm.next_worm = True

            else:
                self.shot(self.power)

        if self.worm.movement["shooting"] or self.current_weapon == "dynamite":
            self.weapons[self.current_weapon].update(delta_time, actions)

    def rotate_image_and_blit(self, surface):
        rot_image = pygame.transform.rotate(self.weapons[self.current_weapon].image, self.angle)
        new_rect = rot_image.get_rect(center=self.weapons[self.current_weapon].image.get_rect(center=self.position).center)
        surface.blit(rot_image, new_rect)

    def render(self, surface):
        if self.worm.movement["shooting"] and self.current_weapon == "machete":
            pass
        else:
            self.rotate_image_and_blit(surface)

        if self.current_weapon != "mortar" and self.current_weapon != "pistol" and self.current_weapon != "m4a1" and self.current_weapon != "machete" and self.current_weapon != "jetpack" and self.current_weapon != "first-aid-kit" and self.current_weapon != "flame-thrower" and self.current_weapon != "dynamite":
            self.powerbar.render(surface)

        if self.current_weapon == "mortar" and self.worm == self.worm.player.overworld.current_player.current_worm:
            sc = self.worm.player.overworld.game.GAME_W / self.worm.player.overworld.game.SCREEN_WIDTH
            x, y = pygame.mouse.get_pos()
            x = x * sc
            y = y * sc
            surface.blit(self.sight, (x - 50, y - 50))


class Worm(Sprite):
    def __init__(self, player, width, height, position, spritesheet, weapons, weapon_menu):
        super().__init__()
        self.life_points = 100
        self.player = player
        self.player.life_points += self.life_points
        self.spritesheet = spritesheet
        self.worm_image = self.spritesheet["move_right"][0]
        self.position = position
        self.jump_count = 5
        self.movement = {"is_jump": False, "move_direction": "right", "previous_move_direction": "left", "shooting": False, "jetpack_on": False, "is_falling": False}
        self.weapon_menu = weapon_menu
        self.weapon = Weapon([position[0] + 10, position[1] + 10], weapons, self)
        self.lifebar = Lifebar(self.position, self)
        self.arrow_of_direction = ArrowOfDirection(self.position, self)
        self.mask = pygame.mask.from_surface(self.worm_image)
        self.fall_height = 0
        self.alive = True
        self.vel = 3
        self.frame = 0
        self.frame_st = 0
        self.frame_time_change = 0
        self.next_worm = False
        self.fall_sound = pygame.mixer.Sound("sounds\\upadek.wav")
        self.death_sound = pygame.mixer.Sound("sounds\\death_sound.wav")

    def can_move(self, direction):
        i = 1
        m = 1
        n = 0
        if direction == "right":
            m = -1
        if direction == "up":
            m = 0
            n = 1
        if direction == "down":
            n = -1
            m = 0
        while i <= self.vel:
            if self.mask.overlap(self.player.overworld.map.mask, (-self.position[0] + i * m, -self.position[1] + i * n)):
                return False
            i += 1
        return True

    def how_much_fall(self):
        i = 1
        while i <= self.vel + 12:
            if self.mask.overlap(self.player.overworld.map.mask, (-self.position[0], -self.position[1] - i)):
                return i - 1
            i += 1
        return i

    def can_move_slope(self, direction):
        i = 1
        m = 1
        if direction == "right":
            m = -1
        while i <= self.vel:
            point = self.mask.overlap(self.player.overworld.map.mask, (-self.position[0] + i * m, -self.position[1]))
            if point is not None:
                if point[1] < 70:
                    return False
            i += 1
        return True

    def update(self, delta_time, actions):
        if self.next_worm:
            self.player.overworld.change_player()
            self.next_worm = False
            self.weapon.power = 0
            self.player.overworld.clock.time = 30

        elif self.alive:
            if self.player.overworld.current_player.current_worm == self:
                pos = [self.position[0], self.position[1] - 60]
                self.player.overworld.current_worm_arrow.set_position(pos)
                self.arrow_of_direction.update(delta_time, actions)
                if not self.movement["shooting"]:
                    if actions["a"] or actions["hold"]["a_hold"]:
                        self.movement["move_direction"] = "left"
                        if self.can_move("left"):
                            self.position[0] -= self.vel
                        elif self.can_move_slope("left"):
                            self.position[0] -= self.vel
                            self.position[1] -= self.vel

                    if actions["d"] or actions["hold"]["d_hold"]:
                        self.movement["move_direction"] = "right"
                        if self.can_move("right"):
                            self.position[0] += self.vel
                        elif self.can_move_slope("right"):
                            self.position[0] += self.vel
                            self.position[1] -= self.vel

                    if actions["space"]:
                        if not self.movement["is_falling"]:
                            self.movement["is_jump"] = True

                if self.movement["jetpack_on"]:
                    if actions["a"] or actions["hold"]["a_hold"]:
                        if self.can_move("left"):
                            self.movement["move_direction"] = "left"
                            self.position[0] -= self.vel

                    if actions["d"] or actions["hold"]["d_hold"]:
                        if self.can_move("right"):
                            self.movement["move_direction"] = "right"
                            self.position[0] += self.vel

                    if actions["w"] or actions["hold"]["w_hold"]:
                        if self.movement["jetpack_on"]:
                            if self.can_move("up"):
                                self.position[1] -= self.vel

                    if actions["s"] or actions["hold"]["s_hold"]:
                        if self.movement["jetpack_on"]:
                            if self.can_move("down"):
                                self.position[1] += self.vel

                self.weapon_menu.update_ammo_state(self.weapon.weapons)
                self.weapon.set_rotate(self.arrow_of_direction.angle)
                self.weapon.update(delta_time, actions)
            self.check_alive()

            if self.movement["is_jump"]:
                self.jump_function()
            elif not self.movement["jetpack_on"]:
                self.falling_function()

            if not self.movement["jetpack_on"]:
                self.update_frame(delta_time)
            self.flip_to_current_direction()
            self.weapon.set_position([self.position[0] + 10, self.position[1] + 10])
            self.mask = pygame.mask.from_surface(self.worm_image)
            self.lifebar.update(self.position)
            self.weapon.powerbar.update(self.position)

    def update_frame(self, dt):
        self.frame_time_change += dt
        if self.frame_time_change > 0.2:
            self.frame = (self.frame + 1) % 3
            if self.frame_st == 0:
                self.frame_st = 13
            else:
                self.frame_st = 0
            self.frame_time_change = 0

    def decrease_life_points(self, amount):
        if self.alive:
            self.life_points -= amount
            if self.life_points <= 0:
                self.life_points = 0

    def check_out_of_map(self):
        if self.position[0] + 100 <= 0 or self.position[0] >= 1920:
            return True
        if self.position[1] + 100 <= 0 or self.position[1] >= 1080:
            return True
        return False

    def check_alive(self):
        if self.check_out_of_map():
            self.life_points = 0
        if self.life_points <= 0:
            self.alive = False
            self.death_sound.play()
            self.position[0] += 20
            self.position[1] += 30
            self.worm_image = pygame.transform.smoothscale(pygame.image.load("images\\tombstone.png").convert_alpha(), (50, 50))
            self.player.overworld.clock.time = 30
            self.player.overworld.change_player()

    def flip_to_current_direction(self):
        if self.alive:
            if self.movement["is_jump"]:
                if self.movement["move_direction"] == "right":
                    worm_image_temp = self.spritesheet["jump_right"][0]
                else:
                    worm_image_temp = self.spritesheet["jump_left"][0]
            elif self.player.overworld.current_player.current_worm != self:
                if self.movement["move_direction"] == "right":
                    worm_image_temp = self.spritesheet["move_left"][self.frame_st]
                else:
                    worm_image_temp = self.spritesheet["move_left"][self.frame_st]
            else:
                if self.movement["move_direction"] == "right":
                    worm_image_temp = self.spritesheet["move_right"][self.frame]
                else:
                    worm_image_temp = self.spritesheet["move_left"][self.frame]
            if not pygame.mask.from_surface(worm_image_temp).overlap(self.player.overworld.map.mask, (-self.position[0], -self.position[1])):
                self.worm_image = worm_image_temp

    def falling_function(self):
        y = self.how_much_fall()
        if y > 1:
            self.position[1] += y
            if y > 3:
                self.movement["is_falling"] = True
                self.fall_height += y
        else:
            if self.fall_height > 250:
                self.fall_height = self.fall_height/800 * 100
                self.decrease_life_points(self.fall_height)
                self.fall_sound.play()
            self.fall_height = 0
            self.movement["is_falling"] = False

    def jump_function(self):
        height = (self.jump_count * abs(self.jump_count))
        if self.mask.overlap(self.player.overworld.map.mask, (-self.position[0], -self.position[1] + height)):
            self.jump_count = 5
            self.movement["is_jump"] = False
        elif self.jump_count >= -5:
            self.position[1] -= height
            self.jump_count -= 1
        else:
            self.jump_count = 5
            self.movement["is_jump"] = False

    def render(self, surface):
        if self.alive:
            if self.player.overworld.current_player.current_worm == self:
                self.arrow_of_direction.render(surface)
                if self.movement["shooting"]:
                    if self.movement["jetpack_on"]:
                        self.weapon.weapons[self.weapon.current_weapon].update_position(self.position[0], self.position[1])
                    self.weapon.weapons[self.weapon.current_weapon].render(surface)
                if self.weapon.current_weapon == "dynamite":
                    self.weapon.weapons[self.weapon.current_weapon].render(surface)
            self.weapon.render(surface)
            self.lifebar.render(surface)
        surface.blit(self.worm_image, self.position)


class Lifebar:
    def __init__(self, position, worm):
        self.position = position
        self.worm = worm
        self.surface = pygame.Surface((70, 10), pygame.SRCALPHA)
        self.value = self.init_value = worm.life_points
        self.color = (0, 255, 0)

    def update(self, position):
        self.value = self.worm.life_points
        self.position = position

    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))

        temp_value = self.value / self.init_value
        rect_border = pygame.rect.Rect(0, 0, 70 * temp_value, 10)
        rect_fill = pygame.rect.Rect(0, 0, 70 * temp_value, 10)
        pygame.draw.rect(self.surface, self.color, rect_fill, 0, 7)
        pygame.draw.rect(self.surface, (0, 0, 0), rect_border, 2, 7)

        surface.blit(self.surface, (self.position[0] + 20, self.position[1] + 80))


class PowerBar:
    def __init__(self, position):
        self.surface = pygame.Surface((70, 10), pygame.SRCALPHA)
        self.position = position
        self.power = 0

    def set_power(self, power):
        self.power = power

    def update(self, position):
        self.position = position

    def render(self, surface):
        self.surface.fill((255, 255, 255, 0))
        if self.power == 0:
            powerbar_background = pygame.rect.Rect(0, 0, 0, 10)
        else:
            powerbar_background = pygame.rect.Rect(0, 0, 70, 10)
        pygame.draw.rect(self.surface, (150, 150, 0), powerbar_background)
        powerbar = pygame.rect.Rect(0, 0, self.power/100 * 70, 10)
        pygame.draw.rect(self.surface, (0, 150, 0), powerbar)

        surface.blit(self.surface, (self.position[0] + 20, self.position[1] + 95))