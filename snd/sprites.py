# Sprite classes
from settings import *
from classes import *
import pygame as pg
from copy import copy

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, name):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.name = name
        self.animator = Animator("Images/ceceil2.png", 16, 16, 4, 2)
        self.animator.setNewAnimation("idle", [0,1], [250,250])
        self.animator.setNewAnimation("walkRight", [6,7], [100,100])
        self.animator.setNewAnimation("walkLeft", [4,5], [100,100])

        self.image = (self.animator.animations[self.animator.currentAnimation][self.animator.currentSpriteNum])
        self.image.set_colorkey(CHROMACOLOR)

        self.rect = self.image.get_rect()
        self.rect.center = 0, 0
        self.currentMap = {"indice":0, "map":None}
        self.jumping = False
        self.onStair = False
        self.onTalk = False
        self.toDraw = True
        self.pos = vec(0,-64)
        self.posScene = vec(0,0)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def update(self):
        if self.pos.x > self.currentMap["map"].endx:
            self.currentMap["indice"] += 1
        elif self.pos.x < self.currentMap["map"].beginx:
            self.currentMap["indice"] -= 1
        self.currentMap["map"] = self.game.scenes[self.currentMap["indice"]]
        self.animator.update()
        self.image = (self.animator.animations[self.animator.currentAnimation][self.animator.currentSpriteNum])
        self.image.set_colorkey(CHROMACOLOR)
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if not self.onTalk:
            if keys[pg.K_UP]:
                self.jump()
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC
                if self.animator.currentAnimation != "walkLeft":
                    self.animator.setAnimation("walkLeft")
            elif keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
                if self.animator.currentAnimation != "walkRight":
                    self.animator.setAnimation("walkRight")
            else:
                if self.animator.currentAnimation != "idle":
                    self.animator.setAnimation("idle")
                    self.vel.x = 0
        self.acc.x += (self.vel.x * PLAYER_FRICTION)
        self.vel += self.acc
        self.pos += self.vel
        self.posScene = (int(self.pos.x / 32), int(self.pos.y / 32))
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
                self.vel.y -= 12

class PlayerOnline(pg.sprite.Sprite):
    def __init__(self, name, pos):
        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pg.Surface((30,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = pos.x, pos.y
        self.toDraw = True
        self.pos = vec(pos.x, pos.y)
        self.online = False
    
    def update(self):
        self.rect.midbottom = (self.pos.x, self.pos.y)
        

# -- Strutures --
class Platform(pg.sprite.Sprite):
    spritesheet = None
    def __init__(self, x, y, w, h, sprite):
        pg.sprite.Sprite.__init__(self)
        if sprite == 0:
            self.image = pg.Surface((32,32))
            self.image.fill(RED)
        else:
            self.image = self.spritesheet.get_image(sprite * 16, 0, 16, 16)
            self.image.set_colorkey(CHROMACOLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.toDraw = True
class Wall(pg.sprite.Sprite):
    spritesheet = None
    def __init__(self, x, y, w, h, sprite):
        pg.sprite.Sprite.__init__(self)
        if sprite == 0:
            self.image = pg.Surface((32,32))
            self.image.fill(BLACK)
        else:
            self.image = self.spritesheet.get_image(sprite * 16, 0, 16, 16)
            self.image.set_colorkey(CHROMACOLOR)
        #self.image.fill(YELLOW)
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
class ObjDraw(pg.sprite.Sprite):
    spritesheet = None
    def __init__(self, x, y, w, h, sprite):
        pg.sprite.Sprite.__init__(self)
        if sprite == 0:
            self.image = pg.Surface((32,32))
            self.image.fill(WHITE)
        else:
            self.image = self.spritesheet.get_image(sprite * 16, 0, 16, 16)
            self.image.set_colorkey(CHROMACOLOR)
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
        
class Collider(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, name, test):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (self.rect.x,self.rect.y)
        self.max_x = self.rect.right - 20
        self.name = name
        self.test = test
        self.toDraw = True 
    