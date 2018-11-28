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
    aspeed = 5
    order = [0, 1, 2]

    def __init__(self):
        super(Gameplay2a, self).__init__()

    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS) - 1)]
        super(Gameplay2a, self).startup(persistent)
        dmx.send_rt(*self.center)
        dmx.send_rgb(*self.inensity)
        while self.order == [0, 1, 2]:
            self.order = random.sample([0, 1, 2],3)
        self.inensity = [self.order[i]*127 for i in self.order]
        print(self.order)
        self.rgb_txt = [
            "",
            "",
            "",
        ]

    def update(self, dt):
        result = statistics.stdev([abs(self.order[i]*127 - self.inensity[i]) for i in range(3)])
        print(result)
        pass

    def chek_result(self):
        self.next_state = "RESULT"
        self.persist["rgb"] = self.inensity
        print("chek_result", self.persist)

    def draw(self, surface):
        surface.fill(pg.Color("darkgreen"))
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (300, 120), self.text[0])
        self.font.render_to(surface, (300, 160), self.text[1])

        for i, freq in enumerate(self.frequency):
            pg.draw.circle(surface, RGB[i][1], (200, 360 + i * 128), 40, 0)
            for x in range(0, 800):
                amplitude = self.amplitude * math.sin(self.aspeed*freq*time.time())
                y = int((200/2) + (amplitude)*math.sin(freq*((float(x)/800)*(2*math.pi) + (self.speed*freq*time.time()))))
                surface.set_at((x+300, 250+y+self.inensity[i]), pg.Color("red"))
                #pg.draw.circle(surface, pg.Color("red"), (x+300, 250+y+i*100),2 )


class Gameplay2b(Gameplay2):

    text = ["Inimese silmas tajuvad värve kolme tüüpi rakud, mida nimetatakse kolvikesteks. Neid on kolme tüüpi punase, rohelise ja sinise värvuse tajumise jaoks.",
            "Jätkamiseks ...."]
    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS) - 1)]
        super(Gameplay2a, self).startup(persistent)
        dmx.send_rt(*self.center)
        dmx.send_rgb(*self.inensity)
        self.inensity = [self.order[i]*127 for i in self.order]
        self.rgb_txt = [
            "",
            "",
            "",
        ]


class Gameplay2ba(GameState):
    pass