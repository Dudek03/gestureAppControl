import pygame as pg

from Game import Game
from Screen_helper import Screen_helper

pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
screen_size = pg.display.get_window_size()
Screen_helper.set_screen(screen)
Screen_helper.set_screen_size(screen_size)
clock = pg.time.Clock()
running = True
dt = 0


game = Game()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            screen_size = pg.display.get_window_size()
            Screen_helper.set_screen_size(screen_size)
            game.on_display_resize()
    screen.fill("black")
    game.update()

    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
