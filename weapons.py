import json
import math
from random import *

import pygame


class Weapons:
    def __init__(self):
        self.weapons = dict()
        self.load_weapons()

    def load_weapons(self):
        file = open("jsons\\weapons.json")
        data = json.load(file)
        file.close()
        for i in data:
            self.weapons[i] = data[i]

    def new_set(self, worm):
        return {"grenade": Grenade(self.weapons["grenade"], worm),
                "bazooka": Bazooka(self.weapons["bazooka"], worm),
                "pistol": Pistol(self.weapons["pistol"], worm),
                "dynamite": Dynamite(self.weapons["dynamite"], worm),
                "m4a1": M4A1(self.weapons["m4a1"], worm),
                "machete": Machete(self.weapons["machete"], worm),
                "jetpack": Jetpack(self.weapons["jetpack"], worm),
                "first-aid-kit": FirstAidKit(self.weapons["first-aid-kit"], worm),
                "mortar": Mortar(self.weapons["mortar"], worm),
                "flame-thrower": FlameThrower(self.weapons["flame-thrower"], worm)
                }

    def get_all_weapons(self):
        return self.weapons


class Weapon:
    def __init__(self, data, worm):
        self.explosion_images = None
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA).convert_alpha()
        self.image = pygame.transform.smoothscale(pygame.image.load(data["image"]).convert_alpha(), (100, 100))
        if data["bullet_image"] != "None":
            self.bullet_image = pygame.transform.smoothscale(pygame.image.load(data["bullet_image"]).convert_alpha(),
                                                             (40, 40))
        self.ammo = data["initial_ammo"]
        self.damage = data["damage"]
        self.worm = worm
        self.power = None
        self.angle = None
        self.direction = None
        self.did_collide = False
        self.out_of_the_map = False
        self.x = None
        self.y = None
        self.direction = None
        self.rotated_image = None
        self.rotated_image_position = None
        self.in_action = False
        self.load_explosion_images()

    def use(self, power, angle, position):
        self.did_collide = False
        self.out_of_the_map = False
        self.power = power
        self.angle = angle
        self.x = position[0]
        self.y = position[1]

    def rotate_bullet_image(self, surface):
        self.rotated_image = pygame.transform.rotate(self.bullet_image, self.angle)
        self.rotated_image_position = self.rotated_image.get_rect(center=self.bullet_image.get_rect(center=(self.x, self.y)).center)
        surface.blit(self.rotated_image, self.rotated_image_position)

    def load_explosion_images(self):
        self.explosion_images = [
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\explosion\\e1.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e2.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e3.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e4.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e5.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e6.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e7.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e8.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e9.png").convert_alpha(), (50, 50)),
            pygame.transform.smoothscale(
                pygame.image.load("images\\sprites\\explosion\\e10.png").convert_alpha(), (50, 50))
        ]


class Grenade(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.explosion_time = 4
        self.this_explosion_time = 0
        self.vel = 10
        self.temp_vel = 0
        self.move = False
        self.mask_top = pygame.mask.from_surface(pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\grenade_top.png").convert_alpha(), (100, 100)))
        self.mask_bottom = pygame.mask.from_surface(
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\grenade_bottom.png").convert_alpha(),
                                         (100, 100)))
        self.mask_left = pygame.mask.from_surface(
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\grenade_left.png").convert_alpha(),
                                         (100, 100)))
        self.mask_right = pygame.mask.from_surface(
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\grenade_right.png").convert_alpha(),
                                         (100, 100)))
        self.explode_radius = 40
        self.explode_surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA).convert_alpha()
        self.zmienna = False
        self.mask = None
        self.did_explode = False
        self.throw_sound = pygame.mixer.Sound("sounds\\grendae_throw_sound.wav")
        self.bounce_sound = pygame.mixer.Sound("sounds\\grenade_bounce_sound.wav")
        self.boom_sound = pygame.mixer.Sound("sounds\\grenade_boom_sound.wav")
        self.boom_sound.set_volume(0.3)
        self.boom_sound_played = False
        self.klatka = 0

    def use(self, power, angle, position):
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            self.klatka = 0
            self.zmienna = False
            self.did_explode = False
            self.boom_sound_played = False
            self.in_action = True
            Weapon.use(self, power, angle, position)
            self.move = False
            self.this_explosion_time = self.explosion_time
            self.calculate_xy()
            self.temp_vel = 10 + self.vel * power/100
            self.throw_sound.play()

        if angle < 90:
            self.direction = "right"
        else:
            self.direction = "left"

    def explode(self, surface):
        self.explode_surface.fill((0, 0, 0, 0))
        if not self.zmienna:
            pygame.draw.circle(self.explode_surface, (255, 0, 0), (self.x + 50, self.y + 50), self.explode_radius)
            self.mask = pygame.mask.from_surface(self.explode_surface)
        surface.blit(self.explosion_images[self.klatka], (self.x + 25, self.y + 25))

        if not self.boom_sound_played:
            self.boom_sound.play()
            self.boom_sound_played = True

        if self.mask.overlap(self.worm.player.overworld.map.mask, (0, 0)) and not self.zmienna:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if worm.mask.overlap(self.mask, (-worm.position[0], -worm.position[1])):
                    x = (worm.position[0] + 50) - self.x
                    y = (worm.position[1] + 50) - self.y
                    d = math.sqrt(x * x + y * y)
                    worm.decrease_life_points(self.damage * d / self.explode_radius)

            pygame.draw.circle(self.worm.player.overworld.map.front_original, (0, 255, 0), (self.x + 50, self.y + 50), self.explode_radius)
            pygame.image.save(self.worm.player.overworld.map.front_original, "images\\temp_map.png")
            self.worm.player.overworld.map.front_original = pygame.image.load("images\\temp_map.png")
            self.zmienna = True

        if self.klatka < 9:
            self.klatka += 1
        else:
            self.in_action = False
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True

    def calculate_xy(self):
        if self.angle < 90:
            rotated_x = 40 * math.cos(math.radians(self.angle))
            rotated_y = 40 * math.sin(math.radians(self.angle))
            self.x += rotated_x
            self.y -= rotated_y + 30
        else:
            rotated_x = 40 * math.cos(math.radians(180 - self.angle))
            rotated_y = 40 * math.sin(math.radians(180 - self.angle))
            self.x -= rotated_x
            self.y -= rotated_y + 30

    def bounce(self, mask):
        self.bounce_sound.play()
        point = mask.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y))
        #od gory
        if self.mask_top.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y)):
            self.angle = -self.angle
        #od dolu
        elif self.mask_bottom.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y)):
            self.angle = -self.angle
        #od lewej
        elif self.mask_left.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y)):
            self.angle = 180 - self.angle
            self.direction = "right"
        #od prawej
        elif self.mask_right.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y)):
            self.angle = 180 - self.angle
            self.direction = "left"
        self.move = True

    def update(self, delta_time, actions):
        mask = pygame.mask.from_surface(self.image)
        self.this_explosion_time -= delta_time
        if not mask.overlap(self.worm.player.overworld.map.mask, (-self.x, -self.y)) or self.move:
            self.move = False
            if self.this_explosion_time > 0:
                if self.direction == "right":
                    a = math.cos(math.radians(self.angle)) * self.temp_vel
                    b = math.sin(math.radians(self.angle)) * self.temp_vel
                    self.x += a
                    self.y -= b
                    if self.angle > -45:
                        self.angle -= (5 - self.power / 100 * 3)
                    elif self.angle > -70:
                        self.angle -= 4 - self.power / 100 * 3
                    elif self.angle > -85:
                        self.angle -= 2 - self.power / 100 * 1
                else:
                    a = math.cos(math.radians(180 - self.angle)) * self.temp_vel
                    b = math.sin(math.radians(180 - self.angle)) * self.temp_vel
                    self.x -= a
                    self.y -= b
                    if self.angle < 225:
                        self.angle += (5 - self.power / 100 * 3)
                    elif self.angle < 250:
                        self.angle += 4 - self.power / 100 * 3
                    elif self.angle < 265:
                        self.angle += 2 - self.power / 100 * 1
                self.power *= 0.98
            else:
                self.did_explode = True
        else:
            self.bounce(mask)

    def render(self, surface):
        if self.did_explode:
            self.explode(surface)
        else:
            surface.blit(self.image, (self.x, self.y))


class Bazooka(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.vel = 15
        self.explode_radius = 40
        self.explode_surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA).convert_alpha()
        self.zmienna = False
        self.mask = None
        self.boom_sound = pygame.mixer.Sound("sounds\\grenade_boom_sound.wav")
        self.boom_sound_played = False
        self.start_sound = pygame.mixer.Sound("sounds\\bazooka_start_sound.wav")
        self.boom_sound.set_volume(0.3)
        self.klatka = 0

    def use(self, power, angle, position):
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            Weapon.use(self, power, angle, position)
            self.klatka = 0
            self.calculate_xy()
            self.boom_sound_played = False
            self.in_action = True
            self.zmienna = False
            self.explode_radius = 40
            self.start_sound.play()
            self.ammo -= 1

        if angle < 90:
            self.direction = "right"
        else:
            self.direction = "left"

    def calculate_xy(self):
        rotated_x = 40 * math.cos(math.radians(self.angle))
        rotated_y = 40 * math.sin(math.radians(self.angle))
        self.x += rotated_x
        self.y -= rotated_y

    def check_is_out_of_the_map(self):
        if self.x > 1920 or self.x < 0:
            self.out_of_the_map = True
            self.in_action = False
        if self.y > 1080 or self.y < 0:
            self.out_of_the_map = True
            self.in_action = False

    def check_did_collide(self):
        mask = pygame.mask.from_surface(self.rotated_image)
        if mask.overlap(self.worm.player.overworld.map.mask, (-self.rotated_image_position[0], -self.rotated_image_position[1])):
            self.did_collide = True
        else:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if mask.overlap(worm.mask, (worm.position[0] - self.rotated_image_position[0], worm.position[1] - self.rotated_image_position[1])):
                    self.did_collide = True

    def explode(self, surface):
        self.explode_surface.fill((0, 0, 0, 0))
        if not self.zmienna:
            pygame.draw.circle(self.explode_surface, (255, 0, 0), (self.x, self.y), self.explode_radius)
            self.mask = pygame.mask.from_surface(self.explode_surface)

        surface.blit(pygame.transform.smoothscale(self.explosion_images[self.klatka], (100, 100)), (self.x - 50, self.y - 50))

        if not self.boom_sound_played:
            self.boom_sound.play()
            self.boom_sound_played = True

        if self.mask.overlap(self.worm.player.overworld.map.mask, (0, 0)) and not self.zmienna:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if worm.mask.overlap(self.mask, (-worm.position[0], -worm.position[1])):
                    if worm != self.worm:
                        x = (worm.position[0] + 50) - self.x
                        y = (worm.position[1] + 50) - self.y
                        d = math.sqrt(x * x + y * y)
                        worm.decrease_life_points(self.damage * d / self.explode_radius)

            pygame.draw.circle(self.worm.player.overworld.map.front_original, (0, 255, 0), (self.x, self.y),
                               self.explode_radius)
            pygame.image.save(self.worm.player.overworld.map.front_original, "images\\temp_map.png")
            self.worm.player.overworld.map.front_original = pygame.image.load("images\\temp_map.png")
            self.zmienna = True

        if self.klatka < 9:
            self.klatka += 1
        else:
            self.in_action = False
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True

    def update(self, delta_time, actions):
        if not self.did_collide and not self.out_of_the_map:
            if self.direction == "right":
                a = math.cos(math.radians(self.angle)) * self.vel
                b = math.sin(math.radians(self.angle)) * self.vel
                self.x += a
                self.y -= b
                if self.angle > -45:
                    self.angle -= (5 - self.power / 100 * 5)
                elif self.angle > -80:
                    self.angle -= 0.5
                else:
                    self.angle -= 0.3
            else:
                a = math.cos(math.radians(180 - self.angle)) * self.vel
                b = math.sin(math.radians(180 - self.angle)) * self.vel
                self.x -= a
                self.y -= b
                if self.angle < 225:
                    self.angle += (5 - self.power / 100 * 5)
                elif self.angle < 260:
                    self.angle += 0.5
                else:
                    self.angle += 0.3
        elif self.out_of_the_map:
            self.worm.movement["shooting"] = False

    def render(self, surface):
        self.rotate_bullet_image(surface)
        self.check_did_collide()
        self.check_is_out_of_the_map()
        if self.did_collide:
            self.explode(surface)


class Pistol(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.vel = 15
        self.shot_sound = pygame.mixer.Sound("sounds\\pistol_sound.wav")
        self.hit_body_sound = pygame.mixer.Sound("sounds\\bullet_body_sound.wav")
        self.hit_metal_sound = pygame.mixer.Sound("sounds\\bullet_metal_sound.wav")

    def use(self, power, angle, position):
        self.in_action = True
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            Weapon.use(self, power, angle, position)
            self.ammo -= 1
            self.calculate_xy()
            self.shot_sound.play()

            if angle < 90:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            self.worm.movement["shooting"] = False

    def calculate_xy(self):
        rotated_x = 40 * math.cos(math.radians(self.angle))
        rotated_y = 40 * math.sin(math.radians(self.angle))
        self.x += rotated_x
        self.y -= rotated_y

    def explode(self):
        pass

    def check_is_out_of_the_map(self):
        if self.x > 1920 or self.x < 0:
            self.out_of_the_map = True
            self.in_action = False
        if self.y > 1080 or self.y < 0:
            self.out_of_the_map = True
            self.in_action = False

    def check_did_collide(self):
        mask = pygame.mask.from_surface(self.rotated_image)
        # map
        if mask.overlap(self.worm.player.overworld.map.mask,
                        (-self.rotated_image_position[0], -self.rotated_image_position[1])):
            self.did_collide = True
            self.in_action = False
            self.hit_metal_sound.play()
        else:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if mask.overlap(worm.mask, (worm.position[0] - self.rotated_image_position[0], worm.position[1] - self.rotated_image_position[1])):
                    if worm != self.worm:
                        worm.decrease_life_points(self.damage)
                        self.did_collide = True
                        self.in_action = False
                        self.hit_body_sound.play()

    def update(self, delta_time, actions):
        if not self.did_collide and not self.out_of_the_map:
            if self.direction == "right":
                a = math.cos(math.radians(self.angle)) * self.vel
                b = math.sin(math.radians(self.angle)) * self.vel
                self.x += a
                self.y -= b
            else:
                a = math.cos(math.radians(180 - self.angle)) * self.vel
                b = math.sin(math.radians(180 - self.angle)) * self.vel
                self.x -= a
                self.y -= b
        else:
            self.in_action = False
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True

    def render(self, surface):
        self.rotate_bullet_image(surface)
        self.check_is_out_of_the_map()
        self.check_did_collide()


class Bomb:
    def __init__(self, image_position, worm, dyn):
        self.worm = worm
        self.position = image_position[1]
        self.image = image_position[0]
        self.explode_radius = 30
        self.explode_surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA).convert_alpha()
        self.zmienna = False
        self.mask = None
        self.boom_sound = pygame.mixer.Sound("sounds\\grenade_boom_sound.wav")
        self.boom_sound_played = False
        self.boom_sound.set_volume(0.3)
        self.klatka = 0
        self.explosion_images = dyn.explosion_images
        self.dyn = dyn

    def explode(self, surface):
        self.explode_surface.fill((0, 0, 0, 0))
        if not self.zmienna:
            pygame.draw.circle(self.explode_surface, (255, 0, 0), (self.position[0] + 50, self.position[1] + 60), self.explode_radius)
            self.mask = pygame.mask.from_surface(self.explode_surface)

        surface.blit(pygame.transform.smoothscale(self.explosion_images[self.klatka], (100, 100)), (self.position[0], self.position[1]))

        if not self.boom_sound_played:
            self.boom_sound.play()
            self.boom_sound_played = True

        if self.mask.overlap(self.worm.player.overworld.map.mask, (0, 0)) and not self.zmienna:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if worm.mask.overlap(self.mask, (-worm.position[0], -worm.position[1])):
                    x = (worm.position[0] + 50) - (self.position[0] + 50)
                    y = (worm.position[1] + 50) - (self.position[1] + 60)
                    d = math.sqrt(x * x + y * y)
                    worm.decrease_life_points(self.dyn.damage * d / self.explode_radius)

            pygame.draw.circle(self.worm.player.overworld.map.front_original, (0, 255, 0), (self.position[0] + 50, self.position[1] + 60),
                               self.explode_radius)
            pygame.image.save(self.worm.player.overworld.map.front_original, "images\\temp_map.png")
            self.worm.player.overworld.map.front_original = pygame.image.load("images\\temp_map.png")
            self.zmienna = True

        if self.klatka < 9:
            self.klatka += 1
        else:
            self.in_action = False
            self.worm.movement["shooting"] = False

    def render(self, surface):
        surface.blit(self.image, self.position)


class Dynamite(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.placed = []
        self.exp = False

    def use(self, power, angle, position):
        self.exp = False
        Weapon.use(self, power, angle, position)
        if self.ammo > 0:
            self.in_action = True
            self.placed.append(Bomb(self.rotate_image(), self.worm, self))
            self.ammo -= 1

    def rotate_image(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_image_position = rotated_image.get_rect(center=self.image.get_rect(center=(self.x, self.y)).center).topleft
        return [rotated_image, rotated_image_position]

    def update(self, delta_time, actions):
        if actions["r"]:
            self.exp = True
        if self.worm.player.overworld.clock.time <= 0:
            self.exp = True

    def render(self, surface):
        if self.exp:
            for p in self.placed:
                p.explode(surface)
                if p.klatka > 8:
                    self.placed.remove(p)
            if len(self.placed) == 0:
                self.in_action = False
                self.worm.next_worm = True
                self.worm.movement["shooting"] = False
        else:
            for p in self.placed:
                p.render(surface)


class Bullet:
    def __init__(self, image, angle, position, m4a1, start_time):
        self.m4a1 = m4a1
        self.image = image
        self.angle = angle
        self.rotated_image = None
        self.rotated_image_position = None
        self.x = position[0]
        self.y = position[1]
        self.did_collide = False
        self.out_of_the_map = False
        self.start_time = start_time
        if angle < 90:
            self.direction = "right"
        else:
            self.direction = "left"
        self.hit_body_sound = pygame.mixer.Sound("sounds\\bullet_body_sound.wav")
        self.hit_metal_sound = pygame.mixer.Sound("sounds\\bullet_metal_sound.wav")
        self.shot = False

    def rotate_bullet_image(self, surface):
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_image_position = self.rotated_image.get_rect(center=self.image.get_rect(center=(self.x, self.y)).center)
        surface.blit(self.rotated_image, self.rotated_image_position)

    def check_is_out_of_the_map(self):
        if self.x > 1920 or self.x < 0:
            self.out_of_the_map = True
        if self.y > 1080 or self.y < 0:
            self.out_of_the_map = True

    def check_did_collide(self):
        mask = pygame.mask.from_surface(self.rotated_image)
        # map
        if collid(mask, self.m4a1.worm.player.overworld.map.mask, self.rotated_image_position[0], self.rotated_image_position[1]):
            self.did_collide = True
            self.hit_metal_sound.play()
        else:
            for i in range(6):
                worm = self.m4a1.worm.player.overworld.all_worms[i]
                if collid(mask, worm.mask, -worm.position[0] + self.rotated_image_position[0], -worm.position[1] + self.rotated_image_position[1]):
                    if worm != self.m4a1.worm:
                        if worm.life_points > 0:
                            worm.decrease_life_points(self.m4a1.damage)
                            self.did_collide = True
                            self.hit_body_sound.play()


def collid(ob1, ob2, ob1_x, ob1_y):
    if ob1.overlap(ob2, (-ob1_x, -ob1_y)):
        return True
    return False


class M4A1(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.vel = 15
        self.bullets = None
        self.time_of_shootout = None
        self.time_from_shoot = None
        self.shot_sound = pygame.mixer.Sound("sounds\\m4a1_sound.wav")

    def use(self, power, angle, position):
        self.in_action = True
        self.time_of_shootout = 1.5
        self.time_from_shoot = 0
        self.bullets = []
        if self.ammo > 15:
            self.worm.movement["shooting"] = True
            Weapon.use(self, power, angle, position)
            self.ammo -= 15
            self.calculate_xy()
            for i in range(15):
                dangle = angle + randint(-2, 2)
                self.bullets.append(Bullet(self.bullet_image, dangle, (self.x, self.y), self, self.time_of_shootout/15 * i))
        else:
            self.worm.movement["shooting"] = False

    def calculate_xy(self):
        rotated_x = 40 * math.cos(math.radians(self.angle))
        rotated_y = 40 * math.sin(math.radians(self.angle))
        self.x += rotated_x
        self.y -= rotated_y

    def explode(self):
        pass

    def update(self, delta_time, actions):
        do_end = 0
        self.time_from_shoot += delta_time
        for bullet in self.bullets:
            if bullet.start_time <= self.time_from_shoot:
                if not bullet.shot:
                    self.shot_sound.play()
                    bullet.shot = True
                if not bullet.did_collide and not bullet.out_of_the_map:
                    if bullet.direction == "right":
                        a = math.cos(math.radians(bullet.angle)) * self.vel
                        b = math.sin(math.radians(bullet.angle)) * self.vel
                        bullet.x += a
                        bullet.y -= b
                    else:
                        a = math.cos(math.radians(180 - bullet.angle)) * self.vel
                        b = math.sin(math.radians(180 - bullet.angle)) * self.vel
                        bullet.x -= a
                        bullet.y -= b
                else:
                    do_end += 1
        if do_end == 15:
            self.worm.next_worm = True
            self.in_action = False
            self.worm.movement["shooting"] = False

    def render(self, surface):
        for bullet in self.bullets:
            bullet.rotate_bullet_image(surface)
            bullet.check_is_out_of_the_map()
            if not bullet.did_collide:
                bullet.check_did_collide()


class Machete(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.frame = None
        self.frame_change_time = 0.005
        self.rotate_range = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 45, 45, 25, -5, -20, -40, -40, -40, -40, 0]
        self.current_image = None
        self.last_change_time = None
        self.current_image = None

    def use(self, power, angle, position):
        self.in_action = True
        self.current_image = pygame.transform.rotate(self.image, angle)
        self.frame = 0
        self.last_change_time = 0
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            Weapon.use(self, power, angle, position)
            self.ammo -= 1
            self.calculate_xy()
            if angle < 90:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            self.worm.shooting = False

    def check_did_collide(self):
        mask = pygame.mask.from_surface(self.rotated_image)
        if not self.did_collide:
            for i in range(6):
                if self.worm.player.overworld.all_worms[i] != self.worm:
                    if mask.overlap(self.worm.player.overworld.all_worms[i].mask, (self.worm.player.overworld.all_worms[i].position[0] - self.rotated_image_position[0],
                            self.worm.player.overworld.all_worms[i].position[1] - self.rotated_image_position[1])):
                        self.worm.player.overworld.all_worms[i].decrease_life_points(self.damage)
                        self.did_collide = True

    def calculate_xy(self):
        if self.angle < 90:
            rotated_x = 40 * math.cos(math.radians(self.angle))
            rotated_y = 40 * math.sin(math.radians(self.angle))
            self.x += rotated_x
            self.y -= rotated_y
        else:
            rotated_x = 40 * math.cos(math.radians(180 - self.angle))
            rotated_y = 40 * math.sin(math.radians(180 - self.angle))
            self.x -= rotated_x
            self.y -= rotated_y

    def explode(self):
        pass

    def update(self, delta_time, actions):
        self.last_change_time += delta_time
        if self.last_change_time >= self.frame_change_time:
            self.last_change_time = 0
            self.frame += 1
        if self.frame == len(self.rotate_range):
            self.in_action = False
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True

    def render(self, surface):
        self.rotated_image = pygame.transform.rotate(self.current_image, self.rotate_range[self.frame])
        self.rotated_image_position = self.rotated_image.get_rect(center=self.current_image.get_rect(center=(self.x, self.y)).center)
        surface.blit(self.rotated_image, self.rotated_image_position)
        self.check_did_collide()


class Jetpack(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.one_fuel_use_time = 0.15
        self.last_fuel_use_time = 0
        self.smoke = [
            pygame.image.load("images\\smoke1.png").convert_alpha(),
            pygame.image.load("images\\smoke2.png").convert_alpha(),
            pygame.image.load("images\\smoke3.png").convert_alpha()
        ]
        self.frame = 0
        self.time_change = 0
        self.currentimage = self.smoke[0]
        self.sound = pygame.mixer.Sound("sounds\\jetpack_sound.wav")

    def use(self, power, angle, position):
        if self.ammo > 0:
            Weapon.use(self, power, angle, position)
            self.worm.movement["jetpack_on"] = True
            self.worm.movement["shooting"] = True

    def update(self, delta_time, actions):
        self.last_fuel_use_time += delta_time
        if self.ammo > 0:
            if self.last_fuel_use_time > self.one_fuel_use_time:
                self.ammo -= 1
                self.last_fuel_use_time = 0
                self.frame = (self.frame + 1) % 3
                self.currentimage = self.smoke[self.frame]
                self.sound.play()
        else:
            self.worm.movement["jetpack_on"] = False
            self.worm.movement["shooting"] = True
            self.in_action = False
            self.worm.next_worm = True
    def update_position(self, x, y):
        self.x = x
        self.y = y

    def render(self, surface):
        surface.blit(self.currentimage, (self.x + 10, self.y))


class FirstAidKit(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.sound = pygame.mixer.Sound("sounds\\first-aid-kit_sound.wav")

    def use(self, power, angle, position):
        self.worm.movement["shooting"] = True
        if self.worm.life_points < 100 and self.ammo > 0:
            self.sound.play()
            self.worm.life_points += self.damage
            self.ammo -= 1
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True
        self.in_action = False
        self.worm.movement["shooting"] = False

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass


class Mortar(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        if self.ammo > 0:
            Weapon.__init__(self, data, worm)
            self.explode_radius = 40
            self.explode_surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA).convert_alpha()
            self.explosion = False
            self.boom_sound = pygame.mixer.Sound("sounds\\grenade_boom_sound.wav")
            self.boom_sound.set_volume(0.3)
            self.boom_sound_played = False
            self.zmienna = False
            self.klatka = 0
            self.ammo -= 1

    def use(self, power, angle, position):
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            Weapon.use(self, power, angle, position)
            self.klatka = 0
            self.boom_sound_played = False
            self.explosion = True
            self.explode_radius = 40
            self.zmienna = False
            self.x, self.y = pygame.mouse.get_pos()
            sc = self.worm.player.overworld.game.GAME_W / self.worm.player.overworld.game.SCREEN_WIDTH
            self.x = self.x * sc
            self.y = self.y * sc

    def update(self, delta_time, actions):
        pass

    def explode(self, surface):
        self.explode_surface.fill((0, 0, 0, 0))
        if not self.zmienna:
            pygame.draw.circle(self.explode_surface, (255, 0, 0), (self.x, self.y), self.explode_radius)
            self.mask = pygame.mask.from_surface(self.explode_surface)

        surface.blit(pygame.transform.smoothscale(self.explosion_images[self.klatka], (100, 100)), (self.x - 50, self.y - 50))

        if not self.boom_sound_played:
            self.boom_sound.play()
            self.boom_sound_played = True

        if self.mask.overlap(self.worm.player.overworld.map.mask, (0, 0)) and not self.zmienna:
            for i in range(6):
                worm = self.worm.player.overworld.all_worms[i]
                if worm.mask.overlap(self.mask, (-worm.position[0], -worm.position[1])):
                    if worm != self.worm:
                        x = (worm.position[0] + 50) - (self.x + 20)
                        y = (worm.position[1] + 50) - (self.y + 20)
                        d = math.sqrt(x * x + y * y)
                        worm.decrease_life_points(self.damage * d / self.explode_radius)

            pygame.draw.circle(self.worm.player.overworld.map.front_original, (0, 255, 0), (self.x, self.y),
                               self.explode_radius)
            pygame.image.save(self.worm.player.overworld.map.front_original, "images\\temp_map.png")
            self.worm.player.overworld.map.front_original = pygame.image.load("images\\temp_map.png")
            self.zmienna = True

        if self.klatka < 9:
            self.klatka += 1
        else:
            self.worm.next_worm = True
            self.in_action = False
            self.worm.movement["shooting"] = False

    def render(self, surface):
        if self.explosion:
            self.explode(surface)
            while self.klatka < 9:
                self.explode(surface)


class FlameThrower(Weapon):
    def __init__(self, data, worm):
        Weapon.__init__(self, data, worm)
        self.fire_size = (140, 140)
        self.fires = [
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_1.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_2.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_3.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_4.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_5.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_6.png").convert_alpha(), self.fire_size),
            pygame.transform.smoothscale(pygame.image.load("images\\sprites\\weapons\\flame_thrower_fires\\part_7.png").convert_alpha(), self.fire_size),
        ]
        self.one_fire_time = 0.07
        self.last_fire_time = 0
        self.frame = 0
        self.sound = pygame.mixer.Sound("sounds\\flamethrower_sound.wav")
        self.sound.set_volume(0.3)

    def use(self, power, angle, position):
        self.in_action = True
        self.last_fire_time = 0
        self.frame = 0
        if self.ammo > 0:
            self.worm.movement["shooting"] = True
            self.sound.play()
            Weapon.use(self, power, angle, position)
            self.calculate_xy()
            self.ammo -= 1

    def calculate_xy(self):
        rotated_x = 120 * math.cos(math.radians(self.angle))
        rotated_y = 120 * math.sin(math.radians(self.angle))
        self.x += rotated_x
        self.y -= rotated_y

    def explode(self):
        pass

    def check_did_collide(self):
        mask = pygame.mask.from_surface(self.rotated_image)
        for i in range(6):
            if self.worm.player.overworld.all_worms[i] != self.worm:
                if mask.overlap(self.worm.player.overworld.all_worms[i].mask, (self.worm.player.overworld.all_worms[i].position[0] - self.rotated_image_position[0],
                self.worm.player.overworld.all_worms[i].position[1] - self.rotated_image_position[1])):
                    self.worm.player.overworld.all_worms[i].decrease_life_points(self.damage)
                    self.did_collide = True

    def update(self, delta_time, actions):
        self.last_fire_time += delta_time
        if self.last_fire_time >= self.one_fire_time:
            self.last_fire_time = 0
            self.frame += 1
        if self.frame == 14:
            self.in_action = False
            self.worm.movement["shooting"] = False
            self.worm.next_worm = True
            self.sound.stop()

    def render(self, surface):
        self.rotate_bullet_image(surface)

    def rotate_bullet_image(self, surface):
        self.rotated_image = pygame.transform.rotate(self.fires[self.frame % 7], self.angle)
        self.rotated_image_position = self.rotated_image.get_rect(center=self.fires[self.frame % 7].get_rect(center=(self.x, self.y)).center)
        surface.blit(self.rotated_image, self.rotated_image_position)
        if not self.did_collide:
            self.check_did_collide()
