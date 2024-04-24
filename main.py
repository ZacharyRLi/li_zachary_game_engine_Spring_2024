# This file was created by: Zachary Li
# My first source control edit
# import libraries
import pygame as pg
import sys
from settings import *
from sprites import *
from random import randint
from os import path

# Data types: Int, String, float, Boolean
# Adding Puzzle elements and dialogue


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
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'images')
        self.map_data = []
        self.bg_image = pg.image.load(path.join(self.img_folder, "cave_bg.png")).convert_alpha()
        self.bg_image = pg.transform.scale(self.bg_image, (1024, 768))
        self.wall_image = pg.image.load(path.join(self.img_folder, "wall.jpg")).convert_alpha()
        self.fireball_image = pg.image.load(path.join(self.img_folder, "fireball.png")).convert_alpha()
        self.healthboost_image = pg.image.load(path.join(self.img_folder,"healthboost.png")).convert_alpha()
        self.coin_image = pg.image.load(path.join(self.img_folder, "coin.png")).convert_alpha()
        self.mob_image = pg.image.load(path.join(self.img_folder, "mob.png")).convert_alpha()
        self.portal_closed_image = pg.image.load(path.join(self.img_folder, "portal_closed.png")).convert_alpha()
        self.portal_open_image = pg.image.load(path.join(self.img_folder, "portal_open.png")).convert_alpha()
        with open(path.join(self.game_folder, 'LEVEL1.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def change_level(self, lvl):
        # kill sprites
        for s in self.all_sprites:
            s.kill()
        # map data empties
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        # make new sprites on map
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'L':
                    Lava(self, col, row)
                if tile == 'H':
                    Healthboost(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'X':
                    Portal(self, col, row)
                

    def new(self):
        # initiate all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.lava = pg.sprite.Group()
        self.healthboost = pg.sprite.Group()
        self.coin = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        self.portal = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        # places sprites at map.
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'L':
                    Lava(self, col, row)
                if tile == 'H':
                    Healthboost(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'X':
                    Portal(self, col, row)
    # define run method in game engine
    def run(self):
        # run method. all important mechanics that need to be checked go here.
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            if self.player.health <= 0:
                print('You Died :(')
                self.quit()
            self.draw()
    
    def draw_text(self, surface, text, size, color, x, y):
        # draw text in pygame
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    def quit(self):
        # quit function calls all to quit
        pg.quit()
        sys.exit()

    def update(self):
        # updates all sprites
        self.all_sprites.update()
        if self.player.touch_change == True:
            self.change_level('LEVEL2.txt')
            self.player.touch_change == False

    def draw_grid(self):
        # draws the grid based on TILESIZE
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        # Draws the background first and then all the sprites, because it draws the sprites over the background making them visible.
        self.screen.blit(self.bg_image, (0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.player.health), 64, WHITE, 1, 1)
        self.draw_text(self.screen, str(self.player.money), 64, WHITE, 28, 1)
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
        # pauses all until input
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/1500, HEIGHT/1500)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the GO screen - press any key to play", 24, WHITE, WIDTH/1500, HEIGHT/1500)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
g.show_start_screen()
while True:
    # runs game in loop
    g.new()
    g.run()
    g.show_go_screen()

    