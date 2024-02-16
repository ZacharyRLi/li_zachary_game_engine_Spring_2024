# This file was created by: Zachary Li

# import libraries
import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path

# Data types: Int, String, float, Boolean


# creating the game class
class Game:
    # initialize the game window
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
    # load save game data
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initiate all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    self.enemy = Enemy(self, col, row)
    # define run method in game engine
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # updates all sprites
        self.all_sprites.update()

    def draw_grid(self):
        # draws the grid based on TILESIZE
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        # Draws the background first and then all the sprites, because it draws the sprites over the background making them visible.
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    # player input
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     keys
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=+1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=+1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()


g.run()

    