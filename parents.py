from config import *
import pygame as pg


class Sprite(pg.sprite.Sprite):
    def __init__(self, x=0, y=0, size=TILE_SIZE, speed=0, image=MISSING, collidable=True):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.speed = speed
        self.tick = 0
        self.frames = 0
        self.image = pg.transform.scale(pg.image.load(image), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.animated = False
        self.collidable = collidable
        self.player = False
        self.animation_speed = 0.5

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def animation_tick_count(self):
        self.frames += 1
        if not self.frames % (FPS * self.animation_speed):
            self.tick = not self.tick

    def animation_tick_reset(self):
        self.tick = 0

    def animation_movement(self):
        if self.speed_x > 0:
            self.image_flipped = False
        if self.speed_x < 0:
            self.image_flipped = True

        if self.speed_x:
            if self.image_flipped:
                self.image = pg.transform.scale(self.pictures['walk_flipped'][self.tick], (self.size, self.size))
            else:
                self.image = pg.transform.scale(self.pictures['walk'][self.tick], (self.size, self.size))
        else:
            if self.image_flipped:
                self.image = pg.transform.scale(self.pictures['idle_flipped'][self.tick], (self.size, self.size))
            else:
                self.image = pg.transform.scale(self.pictures['idle'][self.tick], (self.size, self.size))

        if self.speed_y < 0:
            self.image = pg.transform.scale(self.pictures['back'][self.tick], (self.size, self.size))
