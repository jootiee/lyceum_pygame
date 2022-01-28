from parents import *
import pygame as pg

class Player(Sprite):
    # variables that arent supposed to be used in other objects
    spikes = None
    coins = None
    medkits = None
    damage = None
    frames = 0

    def __init__(self, x=150, y=150, size=60, speed=10, image=MISSING):
        Sprite.__init__(self, x, y, size, speed, image)
        self.money = 0
        self.hp_max = 100
        self.hp_start = self.hp_max
        self.hp = self.hp_start
        self.delay = 500
        self.cooldown = self.delay
        self.jump_force = 10
        self.speed_x = 0
        self.accel_x = 2
        self.speed_x_max = 5.5
        self.speed_y = 0
        self.accel_y = 2
        self.speed_y_max = 5.5
        self.x0 = x
        self.y0 = y
        self.player = True
        self.collidable = False

        # pictures load
        self.image_flipped = False
        self.pictures = dict()

        # loads pictures from config.py
        for key in PLAYER_ASSETS.keys():
            self.pictures[key] = [pg.image.load(pic) for pic in PLAYER_ASSETS[key]]

        # flipped versions of pictures
        for key in PLAYER_ASSETS.keys():
            self.pictures[f'{key}_flipped'] = [pg.transform.flip(pic, True, False) for pic in self.pictures[key]]

    # sets position from load_map
    def set_position(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update(self, up, down, left, right, ms):
        self.collide_check(ms)
        self.animation_tick_count()

        if up == down:
            self.speed_y *= 0.9
            if abs(self.speed_y) < .5:
                self.speed_y = 0
        elif up:
            self.speed_y -= self.accel_y
            if abs(self.speed_y) > self.speed_y_max:
                self.speed_y = -self.speed_y_max
        elif down:
            self.speed_y += self.accel_y
            if abs(self.speed_y) > self.speed_y_max:
                self.speed_y = self.speed_y_max

        self.rect.y += self.speed_y

        # collide check - if on block
        is_bottom_colliding = False
        for block in self.solid_blocks:
            if block.collidable:
                if pg.sprite.collide_rect(self, block):
                    if self.speed_y < 0:
                        self.rect.top = block.rect.bottom
                        self.speed_y = 0
                    else:
                        self.rect.bottom = block.rect.top

                        

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_SIZE[1]:
            self.rect.bottom = WIN_SIZE[1]

        # walking (x movement)
        if left == right:
            self.speed_x *= 0.9
            if abs(self.speed_x) < .5:
                self.speed_x = 0
        elif left:
            self.speed_x -= self.accel_x
            if abs(self.speed_x) > self.speed_x_max:
                self.speed_x = -self.speed_x_max
        elif right:
            self.speed_x += self.accel_x
            if abs(self.speed_x) > self.speed_x_max:
                self.speed_x = self.speed_x_max

        self.rect.x += self.speed_x

        # collide check - if touching block
        for block in self.solid_blocks:
            if block.collidable:
                if pg.sprite.collide_rect(self, block):
                    if self.speed_x < 0:
                        self.rect.left = block.rect.right
                        self.speed_x = 0
                    else:
                        self.rect.right = block.rect.left
                        self.speed_x = 0

        # prevents character from leaving screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIN_SIZE[0]:
            self.rect.right = WIN_SIZE[0]

        # death track
        if self.hp <= 0:
            self.respawn()

        # parent animation method
        self.animation_movement()

    def collide_check(self, ms):
        if self.coins:
            for coin in self.coins:
                if pg.sprite.collide_rect(self, coin):
                    self.money += coin.value
                    coin.kill()

        if self.spikes:
            for spike in self.spikes:
                if pg.sprite.collide_rect(self, spike):
                    self.hp -= self.take_damage(ms, spike.damage)

        # if self.medkits:
        #     for medkit in self.medkits:
        #         if pg.sprite.collide_rect(self, medkit):
        #             if self.hp + medkit.value < 100:
        #                 self.hp += medkit.value
        #             else:
        #                 self.hp = self.maxhp
        #             medkit.kill()

    # method that changes player hp depending on colliding spikes or not
    def take_damage(self, ms, damage):
        if self.cooldown > 0:
            self.cooldown -= ms
            self.taking_damage = False
            return 0
        if self.cooldown <= 0:
            self.cooldown = 0
        if self.cooldown == 0:
            self.cooldown = self.delay
            self.taking_damage = True
            return damage

    # method called when player hp <= 0 - death
    def respawn(self):
        self.money = round(self.money * 0.9)
        self.rect.topleft = self.x0, self.y0
        self.hp = self.hp_max
