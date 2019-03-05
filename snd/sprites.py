# Sprite classes
from settings import *
import pygame as pg
from copy import copy

vec = pg.math.Vector2

class SpriteSheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = 0, 0
        self.jumping = False
        self.onTalk = False
        self.toDraw = True
        self.pos = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if not self.onTalk:
            if keys[pg.K_UP]:
                hits = pg.sprite.spritecollide(self, self.game.stairs, False)
                if hits:
                    pass
                self.jump()
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC
            elif keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
            else:
                self.vel.x = 0
        self.acc.x += (self.vel.x * PLAYER_FRICTION)
        self.vel += self.acc
        self.pos += self.vel
        self.rect.midbottom = self.pos
        #print ("player pos", self.pos)
    
    def searchMove(self):
        first = pg.key.name(self.queue[0])
        if first == 'down':
            if self.queue in self.downList:
                pass
        
    def checkCall(self):
        self.time = pg.time.get_ticks()
        if self.time - self.call > 250:
            self.queue = []
        elif len(self.queue) > 5:
            self.queue.remove(self.queue[0])
    
    def jump(self):
        # jump only if standing on a platform
        if not self.jumping and self.vel.y == 0:
            self.rect.x += 1
            hits = pg.sprite.spritecollide(self, self.game.platforms, False)
            self.rect.x -= 1
            if hits and self.pos.y < hits[0].rect.bottom:
                self.jumping = True
                self.vel.y -= 10

# -- Strutures --
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.toDraw = True
class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (x,y)
        self.toDraw = True
class Stair(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (x,y)
        self.toDraw = True
# -- End of Strutures


class Mark(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.rect.midbottom = (0,0)
        self.toDraw = False

class Npc(pg.sprite.Sprite):
    def __init__(self, name, x, y, posts):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pg.Surface((30,40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (x,y)
        self.posts = posts
        self.postnum = 0
        self.toDraw = True
    
    def talk(self):
        msg = (self.posts[self.postnum])
        self.postnum += 1
        if self.postnum >= len(self.posts):
            self.postnum = 0
        return msg

class TextBlock(pg.sprite.Sprite):
    def __init__(self, player, screen):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((800,200))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 700
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.max_x = self.rect.right - 20
        self.player = player
        self.screen = screen
        self.toDraw = False
        self.message = ""
        self.font_name = pg.font.match_font(FONT_NAME)
        self.index = 0
    
    def update(self):
        if self.player.onTalk: self.toDraw = True
        else: self.toDraw = False
    
    def setMessage(self, msg):
        self.message = msg
        

    