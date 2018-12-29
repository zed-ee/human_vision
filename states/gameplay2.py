from states.gameplay1 import *
import math, time
SAMPLE_RATE = 22050 ## This many array entries == 1 second of sound.


class Gameplay2a(Gameplay1aa):
    title = "Kuidas ekraan töötab"
    center = config.load("positions", "sidebyside", [[0, 0], [0, 0], [0, 0]])

    frequency = [2, 3, 4]
    amplitude = 25 # in px
    speed = 0.5
    aspeed = 2
    order = [0, 1, 2]
    rotary_step = 3
    positions = [30, 127, 225]
    help = "Liigutamiseks kasuta pöördnuppe, kinnita vastus punase nupuga"

    def __init__(self):
        super(Gameplay2a, self).__init__()
        self.ht = AnimatedSprite(position=(1026, 196), images=load_images("images/ht/up"))
        self.bubble = Sprite(position=(90, 216), image=load_image("images/bubbles/gameplay2a.png"))

        self.r = AnimatedSprite(position=(220, 260), images=load_images("images/waves/red_small"))
        self.g = AnimatedSprite(position=(220, 360), images=load_images("images/waves/green_small"))
        self.b = AnimatedSprite(position=(220, 460), images=load_images("images/waves/blue_small"))

    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS) - 1)]
        super(Gameplay2a, self).startup(persistent)
        dmx.send_rt(*self.center)
        dmx.send_rgb(*self.inensity)
        if "order" not in self.persist or self.persist["order"] is None:
            while self.order == [0, 1, 2]:
                self.order = random.sample([0, 1, 2],3)
            self.inensity = [x for x in self.positions]
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

    def intensity2pixel(self, i):
        (i_min, i_max) = (0, 255)
        (p_min, p_max) = (-20, 255)
        return 300 + (i / i_max) * (p_max - p_min) + p_min

    def update(self, dt):

        self.r.update(dt, None, self.intensity2pixel(self.inensity[self.order[0]]))
        self.g.update(dt, None, self.intensity2pixel(self.inensity[self.order[1]]))
        self.b.update(dt, None, self.intensity2pixel(self.inensity[self.order[2]]))


    def chek_result(self):
        print("positions", self.positions)
        print("intensity", self.inensity)
        print("order", self.order)
        print("intensity order", [self.inensity[self.order[i]] for i in range(3)])
        print("diff", [abs(self.inensity[self.order[i]] - self.positions[i]) for i in range(3)])
        stdev = statistics.stdev([abs(self.inensity[self.order[i]] - self.positions[i]) for i in range(3)])
        print("stdev", stdev)
        result = stdev < 20

        self.next_state = "RESULT"
        self.persist["result"] = result
        self.persist["next_state"] = "GAMEPLAY2b" if result else "GAMEPLAY2a"
        self.persist["inensity"] = None if result else self.inensity
        self.persist["order"] = None if result else self.order
        self.persist["title"] = self.title
        print("chek_result", self.persist)

    def draw(self, surface):

        self.bubble.draw(surface)
        self.ht.draw(surface)

        for i, freq in enumerate(self.frequency):

            pg.gfxdraw.filled_circle(surface, 142, 410 + i * 103, 40, RGB[i][1])
            pg.gfxdraw.aacircle(surface, 142, 410 + i * 103, 40, pg.Color("black"))
            # lines = []
            # for xx in range(1, 400):
            #     x = xx * 2
            #     amplitude = self.amplitude * math.sin(self.aspeed*freq*time.time())
            #     y = int((200/2) + (amplitude)*math.sin(freq*((float(x)/800)*(2*math.pi) + (self.speed*freq*time.time()))))
            #     #surface.set_at((x+300, 250+y+self.inensity[i]), pg.Color("red"))
            #     #pg.draw.circle(surface, pg.Color("red"), (x+300, 250+y+i*100),2 )
            #     lines.append([x+300, 250+y+self.inensity[i]])
            # pg.draw.aalines(surface, pg.Color("red"), False, lines, 2)

        self.r.draw(surface)
        self.g.draw(surface)
        self.b.draw(surface)


class Gameplay2(Gameplay2a):
    pass


class Gameplay2ab(Gameplay2a):

    text = ["Inimese silmas tajuvad värve kolme tüüpi rakud, mida nimetatakse kolvikesteks.",
            "Neid on kolme tüüpi punase, rohelise ja sinise värvuse tajumise jaoks.",
            "Jätkamiseks ...."]
    next_state = "GAMEPLAY2"

    def __init__(self):
        super(Gameplay2a, self).__init__()
        self.ht = AnimatedSprite(position=(1026, 196), images=load_images("images/ht/up"))
        self.bubble = Sprite(position=(90, 216), image=load_image("images/bubbles/gameplay2a.png"))

    def update(self, dt):
        pass

class Gameplay2b(Result):
    help = "Jätkamiseks vajuta punast nuppu"

    pixels_spec = [(1, 1, 14, 14, 14, 14, 148, 472, 0),
                   (2, 2, 7, 7, 7, 7, 74, 236, 5000),
                   (5, 4, 3, 3, 3, 3, 37, 119, 2000),
                   (9, 9, 2, 2, 2, 2, 18, 58, 2000),
                   (19, 19, 2, 2, 1, 1, 8, 29, 2000),
                   (39, 39, 1, 1, 0, 0, 4, 12, 2000),
                   (89, 79, 0, 1, 0, 0, 2, 6, 5000),
                   (159, 139, 0, 0, 0, 0, 1, 1, 5000)#,
                   #(1, 1, 14, 14, 14, 14, (148+14)*3, 472, 2000)
                   ]
    spec = pixels_spec[0]

    def __init__(self):
        super(Gameplay2b, self).__init__()
        self.image = Sprite(position=(0, 0), image=load_image("images/pixel/PIKSEL_1.png"))
        self.next_state = "GAMEPLAY2ba"
        #self.pixels = AnimatedSprite(position=(0, 0), images=load_images("images/pixel/anim"))
        self.surface2 = pg.Surface([500, 500])

    def startup(self, persistent):
        self.rt = config.load("positions", "center", [[0, 0], [0, 0], [0, 0]])
        self.persist = persistent
        self.persist["choice"] = 0
        self.t = 0.0

    def update(self, dt):
        #self.pixels.update(dt / 50)
        self.t += dt
        ct = 0
        for i in range(1, len(self.pixels_spec)):
            ct += self.pixels_spec[i][8]
            if ct > self.t:
                self.spec = self.pixels_spec[i-1]
                return

        print("reset", self.t, ct)
        self.t = 0

    def draw(self, surface):
        self.image.draw(surface)

        #self.pixels.draw(self.surface2)
        self.surface2.fill(pg.Color("black"))
        self.draw_pixels(self.surface2)
        surface.blit(self.surface2, [800, 186])

    def draw_pixels(self, surface2 ):

        s = self.spec;
        dim = pg.Rect(s[4:8])
        if dim.height == 1:
            rect = pg.Rect(self.pixels_spec[-1][4:8])
            pg.draw.rect(surface2, pg.Color(230, 230, 230), rect)
        else:
            for x in range(s[0]):
                for y in range(s[1]):
                    rect = dim.move((dim.right) * 3 * x + s[2] * x, (dim.bottom + s[3]) * y)
                    pg.draw.rect(surface2, pg.Color("red"), rect)
                    pg.draw.rect(surface2, pg.Color("green"), rect.move(dim.right,0))
                    pg.draw.rect(surface2, pg.Color("blue"), rect.move(2*dim.right,0))


class Gameplay2ba(SubMenu):
    answer = 25
    help = "Vastuse sisestamiseks pööra nuppe, kinnita vastus punase nuppuga"

    def __init__(self):
        super(Gameplay2ba, self).__init__()
        self.image = Sprite(position=(0, 0), image=load_image("images/pixel/PIKSEL_3.png"))
        self.next_state = "RESULT"
        self.choices = range(100)

    def startup(self, persistent):
        self.rt = config.load("positions", "center", [[0, 0], [0, 0], [0, 0]])
        self.persist = persistent
        self.active_choice = self.persist["choice"]

    def get_selection(self):
        result = self.active_choice == self.answer
        self.next_state = "RESULT"
        self.persist["choice"] = self.choices[self.active_choice]
        self.persist["result"] = result
        self.persist["next_state"] = "MAINMENU" if result else "GAMEPLAY2ba"
        self.persist["back"] = result
        print("check_result", self.persist)



    def draw(self, surface):
        self.image.draw(surface)
        self.font2.render_to(surface, (240, 620), str(self.active_choice), pg.Color(220, 98, 30))



class Gameplay2b_old(GameState):
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
        # self.size = [0.9, 3]
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

