# Bot classes
from settings import *
import pygame as pg

vec = pg.math.Vector2

class Bot(pg.sprite.Sprite):
    def __init__(self, x, y, player, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.image.fill(WHITE)
        self.pos = vec(x,y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.minDistance = 50
        self.botAcc = 0.5
        self.botFric = -0.12
        self.jumping = False
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
        #print ("pos bot", self.pos)
        #print ("pos player", self.player.pos)
        self.acc = vec(0,PLAYER_GRAV)
        self.distanceToPlayer = (self.pos.distance_to(self.player.pos))
        self.vecToPlayer = (self.pos - self.player.pos)

        if self.distanceToPlayer > self.minDistance:
            # control x bot accelerate
            if self.vecToPlayer.x < 0:
                self.acc.x = self.botAcc
            else:
                self.acc.x = -self.botAcc
            
            # check if player is near to jump
            if self.distanceToPlayer < (self.vel.x * self.predict * 2):
                self.jump()

        # check if hits platform
        self.rect.y += 1
        platforms_hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if platforms_hits:
            self.jumping = False
            if self.vel.y > 0:
                if self.pos.y < platforms_hits[0].rect.bottom:
                    self.pos.y = platforms_hits[0].rect.top + 1
                    self.vel.y = 0
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


class BotShadowWall(pg.sprite.Sprite):
    def __init__(self, bot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((bot.rect.width,bot.rect.height))
        self.image.fill(SOMECOLOR)
        self.bot = bot
        self.pos = vec(bot.pos.x,bot.pos.y)
        self.rect = self.image.get_rect()
        self.rect.x = bot.rect.x
        self.rect.y = bot.rect.y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.toDraw = False # change this
    
    def update(self):
        self.pos = self.bot.pos + ((self.bot.vel.x * self.bot.predict, self.bot.vel.y))
        self.rect.midbottom = self.pos
        hit_wall = pg.sprite.spritecollide(self, self.bot.game.walls, False)
        if hit_wall:
            if self.bot.pos.y > self.bot.player.pos.y:
                self.bot.jump()

class BotShadowPlatform(pg.sprite.Sprite):
    def __init__(self, bot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((bot.rect.width,bot.rect.height))
        self.image.fill(SOMECOLOR)
        self.bot = bot
        self.pos = vec(bot.pos.x,bot.pos.y)
        self.rect = self.image.get_rect()
        self.rect.x = bot.rect.x
        self.rect.y = bot.rect.y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.platform = None
        self.toDraw = False # change this
    
    def update(self):
        if self.bot.jumping:
            hit_plat = pg.sprite.spritecollide(self.bot, self.bot.game.platforms, False)
            if hit_plat:
                if self.bot.vel.y < 0 and self.bot.pos.y > hit_plat[0].rect.bottom:
                    self.platform = hit_plat[0]


    

