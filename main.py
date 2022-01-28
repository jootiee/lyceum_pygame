import pygame as pg
from game import *


class Menu:
    def __init__(self):
        pg.init()
        self.font = pg.font.SysFont(None, 32)
        self.running = True
        self.screen = pg.display.set_mode(WIN_SIZE)
        self.background = pg.image.load(MENU_BACKGROUND)
        self.background = pg.transform.scale(self.background, WIN_SIZE)
        self.choice = 0
        self.ending = False
        self.background = pg.transform.scale(self.background, WIN_SIZE)
        self.text = ['Нажмите "Пробел" для подтверждения выбора']
        self.game = Game()

        self.icon = pg.image.load(ICON)
        pg.display.set_icon(self.icon)

    def events(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.select()
                if event.key == pg.K_s:
                    self.choice = not self.choice
                if event.key == pg.K_w:
                    self.choice = not self.choice
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def select(self):
        if self.choice:
            self.running = False
        else:
            if self.ending:
                self.game = Game()
            self.game.run()
            if self.game.level > 6:
                self.ending_screen()
            else:
                self.running = False

    def ending_screen(self):
        self.ending = True
        if self.game.player.money > 10:
            self.text = ["Поздравляем, вы прошли игру!",
                        f"Вы собрали {self.game.player.money} монет за {str(int(self.game.played // 60)).zfill(2)}:{str(int(self.game.played % 60)).zfill(2)}."]
        else:
            self.text = ["Игра окончена.",
                        "К сожалению, вам не удалось собрать достаточно денег,",
                        "чтобы купить корм своему любимому коту.",
                        f"Время игры: {str(int(self.game.played // 60)).zfill(2)}:{str(int(self.game.played % 60)).zfill(2)}",
                        f"Собрано монет: {self.game.player.money}"]

    def render_text(self):
        text_coord = 0
        self.text_x = 150
        for line in self.text:
            string_rendered = self.font.render(line, 1, pg.Color('#ffe9b7ff'))
            intro_rect = string_rendered.get_rect()
            if line:
                text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = self.text_x
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

    def update(self):
        pg.display.set_caption("Stereoma Horizon")
        if self.ending:
            self.button_retry = pg.transform.scale(pg.image.load(
                BUTTONS["retry"][not self.choice]), (228, 53))
            self.button_quit = pg.transform.scale(
                pg.image.load(BUTTONS["exit"][self.choice]), (228, 53))
        else:
            self.button_play = pg.transform.scale(pg.image.load(
                BUTTONS["play"][not self.choice]), (228, 53))
            self.button_quit = pg.transform.scale(
                pg.image.load(BUTTONS["exit"][self.choice]), (228, 53))

    def render(self):
        self.screen.blit(self.background, (0, 0))
        if self.ending:
            self.screen.blit(self.button_retry, (294, 250))
        else:
            self.screen.blit(self.button_play, (294, 250))
        self.screen.blit(self.button_quit, (294, 350))
        self.render_text()
        pg.display.update()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()


if __name__ == '__main__':
    app = Menu()
    app.run()
    pg.quit()
