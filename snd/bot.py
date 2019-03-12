# Bot classes
from settings import *
from scenes import *
import pygame as pg
from copy import copy, deepcopy

vec = pg.math.Vector2

class Bot(pg.sprite.Sprite):
    def __init__(self, x, y, player, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(WHITE)
        self.pos = vec(x,y)
        self.posScene = (int(x/32), int(y/32))
        self.dir = None
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.minDistance = 50
        self.botAcc = 0.5
        self.botFric = -0.12
        self.jumping = False
        self.onSearch = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.player = player
        self.game = game
        self.distanceToPlayer = 0
        self.vecToPlayer = vec(0,0)
        self.predict = (60 * self.botAcc)
        self.toDraw = True

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.distanceToPlayer = (self.pos.distance_to(self.player.pos))
        self.vecToPlayer = (self.pos - self.player.pos)

        if self.distanceToPlayer > self.minDistance:
            # control x bot accelerate
            if self.vecToPlayer.x < 0:
                self.acc.x = self.botAcc
                self.dir = "right"
            else:
                self.acc.x = -self.botAcc
                self.dir = "left"
            
            if self.player.pos.y < self.pos.y and self.distanceToPlayer < 150:
                self.jump()

        # check if hits platform
        self.rect.y += 1
        platforms_hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if platforms_hits:
            self.jumping = False
            if self.vel.y > 0:
                if self.pos.y < platforms_hits[0].rect.bottom:
                    self.posScene = (int(platforms_hits[0].rect.centerx / 32), int(platforms_hits[0].rect.centery / 32))
                    self.pos.y = platforms_hits[0].rect.top + 1
                    self.vel.y = 0
                    self.checkNearPos()
            if self.vel.y < 0:
                if self.pos.y > platforms_hits[0].rect.bottom:
                    if (self.pos.x < platforms_hits[0].rect.left or self.pos.x > platforms_hits[0].rect.right) and len(platforms_hits) == 1: pass
                    else: self.vel.y = 0
        # check if player hits a wall
        walls_hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if walls_hits:
            self.jump()
            self.pos.x -= self.vel.x
            self.vel.x = 0
        self.acc.x += (self.vel.x * self.botFric)
        self.vel += self.acc
        self.pos += self.vel
        self.rect.midbottom = self.pos
    
    def jump(self):
        # jump only if standing on a platform
        if not self.jumping and self.vel.y >= 0:
            self.rect.x += 1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 1
            if hits and self.pos.y < hits[0].rect.bottom:
                self.jumping = True
                self.vel.y -= 12

    def checkNearPos(self):
        try:
            if not self.jumping:
                if self.dir == "left":
                    diagonal = scene[self.posScene[1] + 1][self.posScene[0] - 1]
                    nextblock = scene[self.posScene[1]][self.posScene[0] - 2]
                    if diagonal == 0 or nextblock == 2:
                        self.jump()

                elif self.dir == "right":
                    diagonal = scene[self.posScene[1] + 1][self.posScene[0] + 1]
                    nextblock = scene[self.posScene[1]][self.posScene[0] + 2]
                    if diagonal == 0 or nextblock == 2:
                        self.jump()
        except IndexError:
            pass