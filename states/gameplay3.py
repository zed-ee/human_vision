from states.gameplay1 import *
from states.mainmenu import *
import gc

things = ["VALGUS", "BANAAN", "ARBUUS", "PIMEDUS", "PORGAND", "VESI", "LUMI", "PEET", "MURU"]
pos = [(0, 0), (226, 250), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (-175, 248), (0, 0)]
colors = [find_color(color, ALL_COLORS) for color in ["Valge", "Kollane", "Punane", "Must", "Oranž", "Taevasinine", "Valge", "Ametüst", "Roheline"]]

try:
    from omxplayer.player import OMXPlayer
except Exception as e:
    OMXPlayer = None
    print(e)


class Gameplay3(Result):
    t = 0.0
    def __init__(self):
        super(Gameplay3, self).__init__()
        self.image = Sprite(position=(0, 0), image=load_image("images/things/intro.png"))
        self.next_state = "GAMEPLAY3a"

    def startup(self, persistent):
        self.rt = config.load("positions", "center", [[0, 0], [0, 0], [0, 0]])
        self.persist = persistent
        video = "images/things/intro.mp4"
        if OMXPlayer is not None and os.path.isfile(video):
            self.player = OMXPlayer(video, args=['--no-osd', '--loop'])
        else:
            self.player = None
        self.t = 0

    def update(self, dt):
        self.t += dt
        if self.t > 15000:
            self.done = True

    def draw(self, surface):
        self.image.draw(surface)

class Gameplay3a(Gameplay1a):

    states = ["GAMEPLAY3b" for i in range(0, 9)]

    title = None

    choices = range(9)

    def __init__(self):
        super(Gameplay3a, self).__init__()
        self.menu = Sprite(position=(0, 0), image=load_image("images/things/menu.png"))

    def startup(self, persistent):

        self.rt = config.load("positions", "center", [[0,0],[0,0], [0,0]])
        self.persist = persistent
        dmx.send_rt(*self.rt)

        self.persist["result"] = True
        self.persist["next_state"] = "GAMEPLAY3"

    def draw(self, surface):
        self.menu.draw(surface)
        for i in range(0, 3):
            for j in range(0, 3):
                color = colors[i*3+j]
                (x, y) = (157+j*278, 268+i*163)
                if i*3+j == self.active_choice:
                    pg.gfxdraw.aacircle(surface, x, y, 63, pg.Color("black"))
                    pg.gfxdraw.aacircle(surface, x, y, 64, pg.Color("black"))

    def update(self, dt):
        c = colors[self.active_choice][1]
        dmx.send_rgb(c.r, c.g, c.b)

class Gameplay3b(Result):
    animations = []
    animation = None
    invert = 0
    def __init__(self):
        super(Gameplay3b, self).__init__()
        self.images = [Sprite(position=(0, 0), image=load_image("images/things/"+x+".png")) for x in things]
        self.next_state = "GAMEPLAY3a"
        #for i, thing in enumerate(things):
        #    try:
        #        anim = AnimatedSprite(position=pos[i], images=load_images("images/things/"+thing.lower()+""))
        #        self.animations.append(anim)
        #    except Exception as e:
        #        self.animations.append(None)
        #        print(e)


    def startup(self, persistent):
        self.rt = config.load("positions", "center", [[0, 0], [0, 0], [0, 0]])
        self.persist = persistent
        i = self.persist["choice"] if "choice" in self.persist else 0
        self.image = self.images[i]
        self.invert = things[i] in ["LUMI", "MURU"]
        video = "images/things/" + things[i].lower() + ".mp4"
        if OMXPlayer is not None and os.path.isfile(video):
            self.player = OMXPlayer(video, args=['--no-osd', '--loop'])
        else:
            self.player = None

        #try:
        #    self.animation = None
        #    gc.collect()
        #    self.animation = AnimatedSprite(position=pos[i], images=load_images("images/things/" + things[i].lower() + "", False))
        #except Exception as e:
        #    self.animation = None
        #    print(e)

    def get_event(self, event):
        super(Gameplay3b, self).get_event(event)
        if self.done and self.player is not None:
            self.player.quit()
            self.player = None
        
    def draw(self, surface):
        if self.invert:
            if self.animation is not None:
                self.animation.draw(surface)
                self.image.draw(surface)
        else:
            self.image.draw(surface)
            if self.animation is not None:
                self.animation.draw(surface)

    def update(self, dt):
        if self.animation is not None:
            self.animation.update(dt)
