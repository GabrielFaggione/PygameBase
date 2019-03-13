
import pygame as pg
import queue
from settings import *
from sprites import *
from scenes import *
from bot import *
from mythread import *
from client import *

class Game:
    vec = pg.math.Vector2
    def __init__(self, queue):
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
        self.q = queue
    
    def new(self):
        # start a new game
        self.all_obj_scene = []
        self.all_obj_ui = []
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.players = {}

        self.player = Player(self, "Gabriel")
        self.all_obj_scene.append(self.player)
        self.all_sprites.add(self.player)
        
        for y in range(0,len(scene)):
            for x in range(0, len(scene[y])):
                if scene[y][x] == 0:
                    pass
                elif scene[y][x] == 1:
                    self.p = Platform((32*x),(32*y), 32, 32)
                    self.all_sprites.add(self.p)
                    self.platforms.add(self.p)
                    self.all_obj_scene.append(self.p)
                elif scene[y][x] == 2:
                    self.w = Wall((32*x),(32*y), 32, 32)
                    self.all_sprites.add(self.w)
                    self.walls.add(self.w)
                    self.all_obj_scene.append(self.w)

        #self.bot = Bot(100, 1000, self.player, self)
        #self.all_sprites.add(self.bot)
        #self.all_obj_scene.append(self.bot)

        teste = ["Ola, tudo bem?\n:3", "Peidei"]
        self.npc = Npc("Roberto", 300, 80, teste)
        self.all_sprites.add(self.npc)
        self.npcs.add(self.npc)
        self.all_obj_scene.append(self.npc)

        self.mark = Mark()
        self.all_obj_scene.append(self.mark)

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
        pg.quit()
    
    def update(self):
        # recv all players pos
        if not self.q["client"].empty():
            data = pickle.loads(self.q["client"].get())
            for addr in data:
                player = data[addr] # pick player
                if player["name"] not in self.players:
                    if player["name"] != self.player.name:
                        self.players[player["name"]] = PlayerOnline(player["name"], player["pos"])
                        self.all_obj_scene.append(self.players[player["name"]])
                        self.all_sprites.add(self.players[player["name"]])
                else:
                    self.players[player["name"]].pos = player["pos"]
                    print (self.players[player["name"]].pos)
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
                    if (self.player.pos.x < platforms_hits[0].rect.left or self.player.pos.x > platforms_hits[0].rect.right) and len(platforms_hits) == 1: pass
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
        
        # send to serv player pos and attributes
        self.q["game"].put([self.player.name, self.player.pos])

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
                        self.player.vel.x, self.player.vel.y = 0,0
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

if __name__ == "__main__":
    gameQueue = queue.Queue(3)
    clientQueue = queue.Queue(3)
    q = {"game":gameQueue, "client": clientQueue}
    client = Client(q)
    game = Game(q)
    threadClient = Thread(1, "client thread", client.startClient)

    threadClient.start()

    game.show_start_screen()
    while game.running:
        game.new()
        game.show_go_screen()
    pg.quit()

