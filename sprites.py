# This file was created by: Zachary Li

# import modules

from settings import *
import pygame as pg
from pygame.sprite import Sprite

# create a player class

# create a wall class

# player is in sprite class now.
class Player(Sprite):
    # initiate player 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/colour
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUEGREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.money = 0

    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            # sqrt2/2
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Enemy":
                self.health -= 1
            if str(hits[0].__class__.__name__) == "Healthboost":
                if self.health == 100:
                    pass
                elif self.health < 100 and self.health >= 80:
                    self.health += 100-self.health
                else:
                    self.health += 20
            if str(hits[0].__class__.__name__) == "Coin":
                self.money += 1

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.width
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y colllision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.enemy, False)
        self.collide_with_group(self.game.healthboost, True)
        self.collide_with_group(self.game.coin, True)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(TURQUOISE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Enemy(Sprite):
    # initiate player 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/colour
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ROSE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0

    def collide_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.vx *= -1
            self.rect.x = self.x

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls()
        self.rect.y = self.y

class Healthboost(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.healthboost
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coin
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    
