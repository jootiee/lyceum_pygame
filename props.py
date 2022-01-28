from config import *
from parents import *
import random
import math

class Coin(Sprite):
    def __init__(self, x=None, y=None, value=1, size=TILE_SIZE // 2, speed=10, image=MISSING):
        if x is None:
            self.x = random.randint(0, WIN_SIZE[0] - size)
        else:
            self.x = x
        if y is None:
            self.y = random.randint(0, WIN_SIZE[1] - size)
        else:
            self.y = y
        super().__init__(self.x, self.y, size, speed, image)
        self.ticks = random.choice(range(0, 360, 5))
        self.forward = 1
        self.spawn = self.rect.topleft
        self.value = value
        self.animated = True

    def update(self, *args):
        if self.ticks >= 360:
            self.ticks -= 360
        self.ticks += 5

        # if no animation
        if not self.speed:
            return
        dy = math.sin(math.radians(self.ticks)) * self.speed
        self.rect.y = self.spawn[1] + dy
