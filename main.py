import pygame as pg

from Game import Game

pg.init()
screen = pg.display.set_mode((1280, 720), pg.RESIZABLE)
screen_size = pg.display.get_window_size()
clock = pg.time.Clock()
running = True
dt = 0


game = Game(screen, screen_size)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            game.on_display_resize()
    screen_size = pg.display.get_window_size()
    screen.fill("black")
    game.update()

    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()
