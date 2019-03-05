
import pygame as pg
from settings import *
from sprites import *
from scenes import *

class Game:
    vec = pg.math.Vector2
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.cam = vec(WIDTH/2,HEIGHT/2)
        self.camMarge = 10.0
        self.font_name = pg.font.match_font(FONT_NAME)
    
    def new(self):
        # start a new game
        self.all_obj_scene = []
        self.all_obj_ui = []
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        
        self.p = Platform(512, 100, 1024, 20)
        self.all_sprites.add(self.p)
        self.platforms.add(self.p)
        self.all_obj_scene.append(self.p)
        self.w = Wall(380, 100, 20, 100)
        self.all_sprites.add(self.w)
        self.walls.add(self.w)
        self.all_obj_scene.append(self.w)
        self.pp = Platform(340, 5, 100, 20)
        self.all_sprites.add(self.pp)
        self.platforms.add(self.pp)
        self.all_obj_scene.append(self.pp)
        self.st = Stair(100, 80, 200, 150)
        self.all_sprites.add(self.st)
        self.stairs.add(self.st)
        self.all_obj_scene.append(self.st)

        teste = ["oi Goxtoso como vc vai?\nVc vem sempre aqui seu lindo cheiroso\nQue belo programador vc é", "uau\nnao é que funcionou mesmo?\nquem diria"]
        self.npc = Npc("Roberto", 300, 80, teste)
        self.all_sprites.add(self.npc)
        self.npcs.add(self.npc)
        self.all_obj_scene.append(self.npc)

        #spawner game objs das scenes
        #for obj in scene["objType"]:
        #    obj =  objType(parameters, gameref)
        #    self.all_sprites.add(obj)
        #    self.objType.add(obj)

        self.mark = Mark()
        self.all_obj_scene.append(self.mark)

        self.player = Player(self)
        self.all_obj_scene.append(self.player)
        self.all_sprites.add(self.player)

        self.msgbox = TextBlock(self.player, self.screen)
        self.all_sprites.add(self.msgbox)
        self.all_obj_ui.append(self.msgbox)

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
        # check if player hits a platform
        self.player.rect.y += 1
        platforms_hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        self.player.rect.y -= 1
        if platforms_hits:
            self.player.jumping = False
            if self.player.vel.y > 0:
                if self.player.pos.y < platforms_hits[0].rect.bottom:
                    self.player.pos.y = platforms_hits[0].rect.top + 1
                    self.player.vel.y = 0
            if self.player.vel.y < 0:
                if self.player.pos.y > platforms_hits[0].rect.bottom:
                    if self.player.pos.x < platforms_hits[0].rect.left or self.player.pos.x > platforms_hits[0].rect.right: pass
                    else: self.player.vel.y = 0
        
        # check if player hits a wall
        walls_hits = pg.sprite.spritecollide(self.player, self.walls, False)
        if walls_hits:
            self.player.pos.x -= self.player.vel.x
            self.player.vel.x = 0
        
        # check if player hits a npc
        npcs_hits = pg.sprite.spritecollide(self.player, self.npcs, False)
        if npcs_hits:
            self.mark.toDraw = True
            self.mark.rect.x = npcs_hits[0].rect.centerx
            self.mark.rect.y = npcs_hits[0].rect.top - 10
            self.mark.rect.midbottom = (self.mark.rect.x, self.mark.rect.y)
        else:
            self.mark.toDraw = False

        self.cam.x -= self.player.vel.x
        self.cam.y = (WIDTH/3 - self.player.pos.y)
    
    def events(self):
        # Game loop - Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing: self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    hits = pg.sprite.spritecollide(self.player, self.npcs, False)
                    if hits and not self.player.onTalk:
                        self.player.onTalk = True
                        self.msgbox.index = 0
                        self.msgbox.setMessage(hits[0].talk())
                        self.msgbox.message = self.msgbox.message.splitlines()
                    elif self.player.onTalk:
                        if (self.msgbox.index + 1) < len(self.msgbox.message):
                            self.msgbox.index += 1
                        else:
                            self.player.onTalk = False
                            self.msgbox.index = 0

    def draw(self):
        #Game Loop - Draw
        self.screen.fill(BLACK)
        #self.all_sprites.draw(self.screen)
        for i in self.all_obj_scene:
            if i.toDraw:
                self.screen.blit(i.image, (i.rect.x + self.cam.x , i.rect.y + self.cam.y))
        for i in self.all_obj_ui:
            if i.toDraw:
                self.screen.blit(i.image, (i.rect.x, i.rect.y))
        if self.player.onTalk:
            self.drawLine(self.npc.name, 36, BLACK, self.msgbox.rect.topleft[0], self.msgbox.rect.topleft[1]+25)
            self.drawMessage(22, RED, self.msgbox.rect.topleft[0], self.msgbox.rect.topleft[1])
        pg.display.flip()
    
    def show_start_screen(self):
        # game splash/start screen
        pass
    
    def show_go_screen(self):
        pass

    def drawLine(self, message, size, color, x, y):
        font = pg.font.Font(FONT_NAME, size)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x,y)
        self.screen.blit(text_surface, text_rect)

    def drawMessage(self, size, color, x, y):
        font = pg.font.Font(FONT_NAME, size)
        space = font.size(' ')[0]
        paddingName = 25
        margin = 50
        x += margin
        y += margin + paddingName
        initX = x
        for word in self.msgbox.message[self.msgbox.index].split(" "):
            for i in range(0, len(word)):
                text_surface = font.render(word[i], True, color)
                width, height = text_surface.get_size()
                text_rect = text_surface.get_rect()
                if x > self.msgbox.rect.right - margin:
                    x = initX
                    y += height + space
                text_rect.midleft = (x,y)
                self.screen.blit(text_surface, text_rect)
                x += width
            x += space

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()
pg.quit()


