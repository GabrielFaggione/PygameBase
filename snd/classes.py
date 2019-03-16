import pygame as pg

class SpriteSheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        return image

class Animator(SpriteSheet):
    def __init__(self, filename, width, height, numcol, numrow):
        SpriteSheet.__init__(self, filename)
        self.img_width = width
        self.img_height = height
        self.numcol = numcol
        self.numrow = numrow
        self.images = []
        for y in range(0, numrow):
            for x in range(0, numcol):
                self.images.append(self.get_image(width*x, height*y, width, height))
        self.currentAnimation = "idle"
        self.currentSpriteNum = 0
        self.animations = {}
        self.animationsTime = {}
        self.call = 0
        self.repeat = True
        self.canCancell = False
    
    def setNewAnimation(self, name, numList, time):
        self.animations[name] = []
        self.animationsTime[name] = []
        for i in range(0, len(numList)):
            self.animations[name].append(self.images[numList[i]])
            self.animationsTime[name].append(time[i])
    
    def setAnimation(self, name):
        self.currentSpriteNum = 0
        self.currentAnimation = name
    
    def update(self):
        if pg.time.get_ticks() - self.call >= self.animationsTime[self.currentAnimation][self.currentSpriteNum]:
            if self.currentSpriteNum == len(self.animations[self.currentAnimation]) - 1: # completed animation
                self.currentSpriteNum = 0
                if self.repeat == False:
                    self.currentAnimation = "idle"
            else:
                self.currentSpriteNum += 1
            self.call = pg.time.get_ticks()

class Scene():
    padding = 0
    def __init__(self, name, tiledmap):
        self.map = tiledmap
        self.height = len(self.map)*32
        self.width = len(self.map[0])*32
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.padding += self.width
        print (self.width)
        
