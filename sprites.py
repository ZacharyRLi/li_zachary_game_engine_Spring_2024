# This file was created by: Zachary Li

# import modules

from settings import *
import pygame as pg
from pygame.sprite import Sprite
import math

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
        self.image = pg.image.load("player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.money = 0
        self.touch_change = False

    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy
    
    def get_keys(self):
        # gets all the key functions and changes the velocity based on it.
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
        # checks for collision with anything, and runs things based on what is colliding
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Lava":
                self.health -= 1
            if str(hits[0].__class__.__name__) == "Mob":
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
            if str(hits[0].__class__.__name__) == "Portal" and self.money >= 5:
                self.touch_change = True
                

    def collide_with_walls(self, dir):
        # collides with walls in x and y
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
        self.collide_with_group(self.game.lava, False)
        self.collide_with_group(self.game.healthboost, True)
        self.collide_with_group(self.game.coin, True)
        self.collide_with_group(self.game.mob, False)
        self.collide_with_group(self.game.portal, False)


class Wall(Sprite):
    def __init__(self, game, x, y):
        # initialize wall class
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("wall.jpg").convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Lava(Sprite):
    # initiate lava
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.lava
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/image
        self.image = pg.image.load("fireball.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 25))
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, 0

    def collide_with_walls(self):
        # detects for collide with walls, and orients itself.
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            self.image = pg.transform.rotate(self.image, 180)
            self.vx *= -1
            self.rect.x = self.x

    def update(self):
        # updates the entire lava under all sprites
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls()
        self.rect.y = self.y

class Healthboost(Sprite):
    def __init__(self, game, x, y):
        # initialises the function
        self.groups = game.all_sprites, game.healthboost
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("healthboost.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    # coin just stays there until someone catches it.
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coin
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("coin.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Mob(Sprite):
    # initiate player 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/colour
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("mob.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.vx, self.vy = 0, 0
    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        # Find direction vector (dx, dy) between enemy and player.
        # it also has a radius of 200, so if the player goes to far, it will stop tracking.
        dx, dy = self.game.player.rect.x - self.rect.x, self.game.player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx += dx * MOB_SPEED
            self.vy += dy * MOB_SPEED
        elif dist >= 200:
            pass
        else:   
            dx, dy = dx / dist, dy / dist  # Normalize.
            self.vx += dx * MOB_SPEED
            self.vy += dy * MOB_SPEED
    def collide_with_walls(self, dir):
        # the mob needs to collide with walls to not be op so we ported it
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
        self.vx = 0
        self.vy = 0
        self.move_towards_player(Player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Portal(Sprite):
    def __init__(self, game, x, y):
        # portal with closed image
        self.groups = game.all_sprites, game.portal
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.image.load("portal_closed.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (175, 75))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def portal_update(self):
        # opens when money >= 5
        if self.game.player.money >= 5:
            self.image = pg.image.load("portal_open.png").convert_alpha()
            self.image = pg.transform.scale(self.image, (175, 75))

    def update(self):
        self.portal_update()
        