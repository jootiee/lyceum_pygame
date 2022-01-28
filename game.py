import pygame as pg

from config import *
from player import *
from props import *
from camera import *



class Game:
    def __init__(self):
        self.display = pg.display.set_mode(WIN_SIZE)
        self.clock = pg.time.Clock()
        self.running = True
        self.down = self.up = self.left = self.right = False
        self.played = 0.0
        self.player_created = False
        self.level = 1
        self.menu_state = 1
        self.ending_state = 0
        self.player = Player()
        self.load_map()

    # method for first load/reload sprites
    def load_sprites(self):
        self.objects = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.spikes = pg.sprite.Group()
        self.medkits = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.solid_blocks = pg.sprite.Group()
        Player.coins = self.coins
        Player.solid_blocks = self.solid_blocks
        self.camera = Camera(self.player, self.objects)

    # restarts the game, resets player stats
    def restart(self):
        self.level = 1
        self.player = Player()
        self.load_map()

    # loads map from /lvl/
    def load_map(self):
        self.load_sprites()
        map_path = LEVELS[self.level]
        with open(map_path, encoding='utf-8') as file:
            for y, line in enumerate(file):
                shift = 0
                for x, letter in enumerate(line):
                    if letter in MAP.keys():
                        pos = [x * TILE_SIZE - shift, y * TILE_SIZE]
                        image = MAP[letter]
                        if letter == '@':
                            shift += TILE_SIZE
                            player_pos = pos
                        if letter in SOLID_BLOCKS:
                            block = Sprite(*pos, image=image)
                            self.solid_blocks.add(block)
                        if letter in UNSOLID_BLOCKS:
                            block = Sprite(*pos, image=image, collidable=False)
                            self.solid_blocks.add(block)
                        elif letter == 'C':
                            shift += TILE_SIZE
                            pos[0] -= TILE_SIZE
                            pos[0] += TILE_SIZE // 4
                            pos[1] += TILE_SIZE // 4
                            block = Coin(*pos, value=1, image=image)
                            self.coins.add(block)
                        try: self.objects.add(block)
                        except: continue
        self.camera.update_borders()
        self.player.set_position(*player_pos)
        self.objects.add(self.player)


    # game run
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()

    # events catch
    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    self.down = True
                if event.key == pg.K_w:
                    self.up = True
                if event.key == pg.K_a:
                    self.left = True
                if event.key == pg.K_d:
                    self.right = True
                if event.key == pg.K_r:
                    self.restart()
            if event.type == pg.KEYUP:
                if event.key == pg.K_s:
                    self.down = False
                if event.key == pg.K_w:
                    self.up = False
                if event.key == pg.K_a:
                    self.left = False
                if event.key == pg.K_d:
                    self.right = False
                if event.key == pg.K_ESCAPE:
                    self.running = False
                if event.key == pg.K_k:
                    self.running = False

    # updates the screen
    def update(self):
        ms = self.clock.tick(FPS)
        self.played += ms / 1000
        self.camera.update()
        self.player.update(self.up, self.down, self.left, self.right, ms)
        self.coins.update()
        if self.player.rect.right >= WIN_SIZE[0]:
            self.level += 1
            print(self.level)
            if self.level > 6:
                self.running = False
            else:
                self.load_map()

    def render(self):
        self.objects.draw(self.display)
        pg.display.update()

    def menu(self):
        self.background = pg.image.load(MENU_BACKGROUND)
        self.background = pg.transform.scale(self.background, WIN_SIZE)


if __name__ == '__main__':
    game = Game()
    game.run()
    pg.quit()
