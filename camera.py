from config import *
from player import *


class Camera:
    def __init__(self, player, blocks):
        self.player = player
        self.blocks = blocks
        self.speed = self.player.speed_x_max
        self.dx = 0
        self.dy = 0
        self.top = self.left = self.right = self.bottom = self.player

    def update_borders(self):
        for block in self.blocks:
            if not block.player:
                if block.rect.top < self.top.rect.top:
                    self.top = block
                if block.rect.bottom > self.bottom.rect.bottom:
                    self.bottom = block
                if block.rect.left < self.left.rect.left:
                    self.left = block
                if block.rect.right > self.right.rect.right:
                    self.right = block

    def update(self):
        w, h = WIN_SIZE
        dx = -(self.player.rect.x + self.player.rect.w // 2 - w // 2)
        dy = -(self.player.rect.y + self.player.rect.h // 2 - h // 2)

        if self.top.rect.top + dy >= 0:
            dy = -self.top.rect.top
        if self.bottom.rect.bottom + dy <= h:
            dy = h - self.bottom.rect.bottom
        if self.left.rect.left + dx >= 0:
            dx = -self.left.rect.left
        if self.right.rect.right + dx <= w:
            dx = w - self.right.rect.right

        for block in self.blocks:
            if block.animated:
                block.rect = block.rect.move(dx, 0)
                block.spawn = (block.spawn[0], block.spawn[1] + dy)
            else:
                block.rect = block.rect.move(dx, dy)