from states.gameplay1 import *
import math, time
SAMPLE_RATE = 22050 ## This many array entries == 1 second of sound.

class Gameplay2(Gameplay1):
    choices = [
        "Kuidas ekraan töötab? (lained)",
        "Kuidas ekraan töötab? (pikslid)"
    ]
    states = ["GAMEPLAY2a", "GAMEPLAY2b"]
    title_txt = "Kuidas ekraan töötab?"

class Gameplay2a(Gameplay1aa):
    title = "Kuidas ekraan töötab"
    text = ["Nagu sa juba tead, siis on igal värvil oma lainepikkus. Ühenda lained kolme põhivärviga ",
            "Kinnita oma valikut punase nupuga"]
    center = config.load("positions", "sidebyside", [[0, 0], [0, 0], [0, 0]])

    frequency = [2, 3, 4]
    amplitude = 25 # in px
    speed = 0.5
    aspeed = 2
    order = [0, 1, 2]
    rotary_step = 3


    def __init__(self):
        super(Gameplay2a, self).__init__()

    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS) - 1)]
        super(Gameplay2a, self).startup(persistent)
        dmx.send_rt(*self.center)
        dmx.send_rgb(*self.inensity)
        if "order" not in self.persist or self.persist["order"] is None:
            while self.order == [0, 1, 2]:
                self.order = random.sample([0, 1, 2],3)
            self.inensity = [self.order[i]*127 for i in range(3)]
        else:
            self.order = self.persist["order"]
            self.inensity = self.persist["inensity"]
            
        print(self.order)
        print(self.inensity)
        self.rgb_txt = [
            "",
            "",
            "",
        ]

    def update(self, dt):
        pass
        

    def chek_result(self):
        stdev = statistics.stdev([abs(i*127 - self.inensity[i]) for i in range(3)])
        print("stdev", stdev)
        result = stdev < 20

        self.next_state = "RESULT"
        self.persist["result"] = result
        self.persist["next_state"] = "GAMEPLAY2ab" if result else "GAMEPLAY2a"
        self.persist["inensity"] = None if result else self.inensity
        self.persist["order"] = None if result else self.order
        print("chek_result", self.persist)

    def draw(self, surface):


        for i, freq in enumerate(self.frequency):
            pg.draw.circle(surface, RGB[i][1], (200, 360 + i * 128), 40, 0)
            lines = []
            for xx in range(1, 400):
                x = xx * 2
                amplitude = self.amplitude * math.sin(self.aspeed*freq*time.time())
                y = int((200/2) + (amplitude)*math.sin(freq*((float(x)/800)*(2*math.pi) + (self.speed*freq*time.time()))))
                #surface.set_at((x+300, 250+y+self.inensity[i]), pg.Color("red"))
                #pg.draw.circle(surface, pg.Color("red"), (x+300, 250+y+i*100),2 )
                lines.append([x+300, 250+y+self.inensity[i]])
            pg.draw.aalines(surface, pg.Color("red"), False, lines, 2)




class Gameplay2ab(Gameplay2a):

    text = ["Inimese silmas tajuvad värve kolme tüüpi rakud, mida nimetatakse kolvikesteks.",
            "Neid on kolme tüüpi punase, rohelise ja sinise värvuse tajumise jaoks.",
            "Jätkamiseks ...."]
    next_state = "GAMEPLAY2"
    
    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS) - 1)]
        super(Gameplay2ab, self).startup(persistent)
        dmx.send_rt(*self.center)
        dmx.send_rgb(*self.inensity)
        self.inensity = [i*127 for i in range(3)]
        self.rgb_txt = [
            "",
            "",
            "",
        ]
        
    def draw(self, surface):
        surface.fill(pg.Color("darkgreen"))
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (300, 120), self.text[0])
        self.font.render_to(surface, (300, 160), self.text[1])

        for i, freq in enumerate(self.frequency):
            pg.draw.circle(surface, RGB[i][1], (200, 360 + i * 128), 40, 0)
            lines = []
            for xx in range(1, 400):
                x = xx * 2
                amplitude = self.amplitude * math.sin(self.aspeed*freq*time.time())
                y = int((200/2) + (amplitude)*math.sin(freq*((float(x)/800)*(2*math.pi) + (self.speed*freq*time.time()))))
                #surface.set_at((x+300, 250+y+self.inensity[i]), pg.Color("red"))
                #pg.draw.circle(surface, pg.Color("red"), (x+300, 250+y+i*100),2 )
                lines.append([x+300, 250+y+i*127])
            pg.draw.aalines(surface, RGB[i][1], False, lines, 2)
    def chek_result(self):
        pass

class Gameplay2b(GameState):
    size = [454.0, 760.0]
    shift = 0
    t = 1.0

    def startup(self, persistent):
        self.persist = persistent
        self.t = 2.0
        self.step = 3

    def update(self, dt):
        if self.t > 13000:
            self.size[0] = self.size[0] - self.step / math.log(self.t)
            self.size[1] = self.size[0] * 760.0 / 454.0
        # self.size = [21, 49]
        # self.size = [13, 34]
        self.size = [0.9, 3]
        self.t += dt

    def draw_rgb(self, surface, size, screen, shift, intensity = 1):
        surface2 = pg.Surface(screen)
        surface2.fill(pg.Color("black"))
        spacingx = 0.9 if size[0] > 2 else 1
        for y in range(screen[1] // size[1] + 1):
            for x in range(screen[0] // size[0]):
                for i, c in enumerate(RGB):
                    color = pg.Color(int(c[1][0] * intensity),int(c[1][1] * intensity),int(c[1][2] * intensity))
                    pg.draw.rect(surface2, color, pg.Rect([0, 0, int(size[0] * spacingx), int(size[1] * 0.9)])
                                 .move(x * size[0] * 3 + i * size[0], y * size[1])
                                 .move(int(size[0] * 0.05), int(size[1] * 0.05))
                                 , 0)

                    # else:
                    #    surface.set_at((x*size[0]*3+i*size[0], y*size[1]), c[1])

                    # print(pg.Rect([0, 0, 20, 20]).move(i*x*20, y*20))
        surface.blit(surface2, shift)

    def draw(self, surface):
        size = [int(x) for x in self.size]
        screen = [surface.get_width(), surface.get_height()]

        if size[0] > 60:
            self.draw_rgb(surface, size, screen, (0, 0))
        elif size[0] > 20:
            self.draw_rgb(surface, [60, 118], screen, (0, 0), 0.7)
            self.draw_rgb(surface, size, [60*18, 118*5], (120, 118))
            self.step = 2
        elif size[0] > 10:
            self.draw_rgb(surface, [60, 118], screen, (0, 0), 0.5)
            self.draw_rgb(surface, [20, 47], [120*9, 118*5], (120, 118), 0.7)
            self.draw_rgb(surface, size, [20*30, 47*5], (20*9, 47*9))
            self.step = 1.6
        elif size[0] >= 3:
            self.draw_rgb(surface, [60, 118], screen, (0, 0), 0.3)
            self.draw_rgb(surface, [20, 47], [120*9, 118*5], (120, 118), 0.5)
            self.draw_rgb(surface, [10, 18], [20*30, 47*5], (20*9, 47*9), 0.7)
            self.draw_rgb(surface, size, [10*30, 18*5], (20*9+10*3, 47*9+18*7))
            self.step = 1.4
        elif size[0] >= 1:
            self.draw_rgb(surface, [60, 118], screen, (0, 0), 0.2)
            self.draw_rgb(surface, [20, 47], [120*9, 118*5], (120, 118), 0.3)
            self.draw_rgb(surface, [10, 18], [20*30, 47*5], (20*9, 47*9), 0.5)
            self.draw_rgb(surface, [3, 6], [10*30, 18*5], (20*9+10*3, 47*9+18*7), 0.7)
            self.draw_rgb(surface, size, [5*30, 9*5], (5*4+20*9+10*3, 9*4+47*9+18*7))
            self.step = 1.2

        else:
            self.draw_rgb(surface, [60, 118], screen, (0, 0), 0.2)
            self.draw_rgb(surface, [20, 47], [120*9, 118*5], (120, 118), 0.3)
            self.draw_rgb(surface, [10, 18], [20*30, 47*5], (20*9, 47*9), 0.5)
            self.draw_rgb(surface, [3, 6], [300, 18*5], (210, 549), 0.7)
            self.draw_rgb(surface, [1, 3], [150, 45], (230, 585))
            pg.draw.rect(surface, pg.Color("white"), (240, 600, 26, 26), 0)
            self.step = 1
            print(size)


class Gameplay2ba(GameState):
    pass