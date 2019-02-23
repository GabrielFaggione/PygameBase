
import pygame as pg
from settings import *
from sprites import *
from scenes import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # start a new game
        self.all_obj_scene = []
        self.all_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.background = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        
        self.p = Platform(0, 600, 1024, 10)
        self.all_sprites.add(self.p)
        self.platforms.add(self.p)
        self.all_obj_scene.append(self.p)
        #spawner game objs das scenes
        #for obj in scene["objType"]:
        #    obj =  objType(parameters, gameref)
        #    self.all_sprites.add(obj)
        #    self.objType.add(obj)

        self.player = Player(self)
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        self.run()
    
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only in falling
        self.player.rect.y += 1
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        self.player.rect.y -= 1
        if hits:
            self.player.pos.y = hits[0].rect.top + 1
            self.player.vel.y = 0
        
        #for i in self.all_obj_scene:
        #    i.rect.x -= self.player.vel.x
        #    i.rect.y -= self.player.vel.y
    
    def events(self):
        # Game loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing: self.playing = False
                self.running = False

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        pg.display.flip()
    
    def show_start_screen(self):
        # game splash/start screen
        pass
    
    def show_go_screen(self):
        pass


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()
pg.quit()


