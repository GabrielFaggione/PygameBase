# Sprite classes
from settings import *
import pygame as pg

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
        self.rect.center = 0 + CAMERAWIDTH, 0 + CAMERAHEIGHT
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.jump()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_LSHIFT]:
            # apply friction
            self.acc.x += (self.vel.x * PLAYER_FRICTION) * 2
        else:
            self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)
        self.rect.midbottom = self.pos
    
    def searchMove(self):
        first = pg.key.name(self.queue[0])
        if first == 'down':
            if self.queue in self.downList:
                print ('oi')

        
    def checkCall(self):
        self.time = pg.time.get_ticks()
        if self.time - self.call > 250:
            self.queue = []
        elif len(self.queue) > 5:
            self.queue.remove(self.queue[0])
    
    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y -= 10


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x + CAMERAWIDTH
        self.rect.y = y
        self.rect.midbottom = (self.rect.x,self.rect.y)


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.midbottom = (x,y)
