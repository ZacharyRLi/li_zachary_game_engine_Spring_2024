# This file was created by: Zachary Li

# import modules

from settings import *
import pygame as pg
from pygame.sprite import Sprite
import math
from os import path

# create a player class

# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

# player is in sprite class now.
class Player(Sprite):
    # initiate player 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/colour
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, "anim_player.png"))
        # needed for animated sprite
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.health = 100
        self.money = 0
        self.touch_change = False
        # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False

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
            if str(hits[0].__class__.__name__) == "Portal" and self.game.button.down == True:
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
    def collide_with_pushable(self, dir):
        # collides with pushable and pushes it.
        hits = pg.sprite.spritecollide(self, self.game.pushable, False)
        for hit in hits:
            if dir == 'x':
                if self.vx > 0:  # Moving right
                    while pg.sprite.spritecollide(self, self.game.pushable, False):
                        hit.rect.left += 1
                elif self.vx < 0:  # Moving left
                    while pg.sprite.spritecollide(self, self.game.pushable, False):
                        hit.rect.right -= 1
            if dir == 'y':
                if self.vy > 0:  # Moving down
                    while pg.sprite.spritecollide(self, self.game.pushable, False):
                        hit.rect.top += 1
                elif self.vy < 0:  # Moving up
                    while pg.sprite.spritecollide(self, self.game.pushable, False):
                        hit.rect.bottom -= 1

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 900:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.image.set_colorkey(pg.Color(245, 233, 12))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def update(self):
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.animate()
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y colllision later
        self.collide_with_walls('y')
        self.collide_with_pushable('x')
        self.collide_with_pushable('y')
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
        self.image = self.game.wall_image
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
        self.image = self.game.fireball_image
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
        self.image = self.game.healthboost_image
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
        self.spritesheet = Spritesheet(path.join(img_folder, "anim_coin.png"))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
    
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32), 
                                self.spritesheet.get_image(32, 0, 32, 32),
                                self.spritesheet.get_image(64, 0, 32, 32),
                                self.spritesheet.get_image(96, 0, 32, 32),
                                self.spritesheet.get_image(0, 32, 32, 32),
                                self.spritesheet.get_image(32, 32, 32, 32),
                                self.spritesheet.get_image(64, 32, 32, 32),
                                self.spritesheet.get_image(96, 32, 32, 32),
                                self.spritesheet.get_image(0, 64, 32, 32),
                                self.spritesheet.get_image(32, 64, 32, 32),
                                self.spritesheet.get_image(64,64, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.image.set_colorkey(pg.Color(245, 233, 12))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    def update(self):
        self.animate()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
class Mob(Sprite):
    # initiate player 
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mob
        Sprite.__init__(self, self.groups)
        self.game = game
        # defining coordinates/colour
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.mob_image
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
        self.image = self.game.portal_closed_image
        self.image = pg.transform.scale(self.image, (175, 75))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
    def portal_update(self):
        # opens when money >= 5
        if self.game.button.down:
            self.image = self.game.portal_open_image
            self.image = pg.transform.scale(self.image, (175, 75))
        else:
            self.image = self.game.portal_closed_image
            self.image = pg.transform.scale(self.image, (175, 75))
    def update(self):
        self.portal_update()

class Button(Sprite):
    def __init__(self, game, x, y):
        # initialises the function
        self.groups = game.all_sprites, game.button
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, "button.png"))
        self.load_images()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        bottom = self.rect.bottom
        self.image = self.button[0]
        self.image.set_colorkey(pg.Color(245, 233, 12))
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.down = False
    def load_images(self):
        self.button = [self.spritesheet.get_image(32, 96, 32, 32), 
                        self.spritesheet.get_image(32,224, 32, 32)]
    def collide_with_group(self, group, kill):
        # checks for collision with anything, and runs things based on what is colliding
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Pushable":
                self.down = True
                bottom = self.rect.bottom
                self.image = self.button[1]
                self.image.set_colorkey(pg.Color(245, 233, 12))
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        else:
            self.down = False
            bottom = self.rect.bottom
            self.image = self.button[0]
            self.image.set_colorkey(pg.Color(245, 233, 12))
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def update(self):
        self.collide_with_group(self.game.pushable, False)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Pushable(Sprite):
    def __init__(self, game, x, y):
        # initialises the function
        self.groups = game.all_sprites, game.pushable
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.pushable_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
        