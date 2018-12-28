# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
import random
from states.mainmenu import *
import statistics
random.seed()
from colors import *
from interpolate import interpolate
from animations import  load_image
from pygame import gfxdraw

class Gameplay1(SubMenu):
    choices = [
        "Leia õiged lainepikkused",
        "Sega kokku oma lemmikvärv"
    ]
    states = ["GAMEPLAY1a", "GAMEPLAY1b"]
    title = "Kuidas värve segada?"
    option_height = 230
    default_color = pg.Color(0, 0, 0)

    rts = [
        config.load("positions", "offset", [[0,0],[0,0], [0,0]]),
        config.load("positions", "sidebyside", [[0,0],[0,0], [0,0]])
    ]

    def __init__(self):
        super(Gameplay1, self).__init__()
        self.ht = AnimatedSprite(position=(930, 196), images=load_images("images/ht/color"))
        self.logo = LOGO.WHITE
        self.background = pg.Color("white")

    def startup(self, persistent):
        self.persist = {}
        
    def update(self, dt):
        dmx.send_rt(*(self.rts[self.active_choice]))

class Gameplay1a(SubMenu):

    states = ["GAMEPLAY1aa" for i in range(0, 9)]
    title = "Leia õiged lainepikkused"
    help = "Kinnita oma valikut punase nupuga"

    def __init__(self):
        super(Gameplay1a, self).__init__()
        self.ht = AnimatedSprite(position=(960, 196), images=load_images("images/ht/color"))
        self.bubble = Sprite(position=(247, 220), image=load_image("images/bubbles/gameplay1a.png"))

        self.logo = LOGO.WHITE
        self.background = pg.Color("white")

    def startup(self, persistent):
        self.choices = random.sample(COLORS, 9)
        self.titles = [color[0] for color in self.choices]
        for c in self.choices:
            print(c)
        self.rt = config.load("positions", "center", [[0,0],[0,0], [0,0]])
        self.persist = persistent
        dmx.send_rt(*self.rt)

    def draw(self, surface):
        # super(Gameplay1a, self).draw(surface)
        for i in range(0, 9):
            color = self.choices[i]
            (x, y) = (140+i*108, 522)
            if i == self.active_choice:
                #pg.gfxdraw.filled_circle(surface, x, y, 45, pg.Color("black"))
                pg.gfxdraw.aacircle(surface, x, y, 46, pg.Color("black"))
                pg.gfxdraw.aacircle(surface, x, y, 47, pg.Color("black"))
            pg.gfxdraw.filled_circle(surface, x, y, 42, color[1])
            pg.gfxdraw.aacircle(surface, x, y, 42, pg.Color(220, 98, 30))

        self.bubble.draw(surface)
        self.ht.draw(surface)

    def update(self, dt):
        c = self.choices[self.active_choice][1]
        dmx.send_rgb(c.r, c.g, c.b)

class Gameplay1aa(GamePlay):
       
    text = ["Värve saab kombineerida erinevatest lainepikkustest. Sega kolmes põhivärvist kokku valitud värv. ",
                 "Selleks tuleb sul prožektori valgused seadistada õigetele valgustugevustele, kasutades pöördnuppe."]
    title = "Leia õige lainepikkus"
    rotary_step = 1
    mousebutton = 0
    def __init__(self):
        super(Gameplay1aa, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128)).move(960, 420)
        self.x_velocity = 1
        self.next_state = "MAINMENU"
        self.ht = AnimatedSprite(position=(980, 196), images=load_images("images/ht/color"))
        self.bubble = Sprite(position=(106, 216), image=load_image("images/bubbles/gameplay1aa.png"))
        self.background = pg.Color("white")

    def get_event(self, event):
        if event.type == ROTARY_BUTTON:
            if event.direction == 1:
               self.inensity[event.button] = min(255, self.inensity[event.button] + self.rotary_step)
            else:
               self.inensity[event.button] = max(0, self.inensity[event.button] - self.rotary_step)
        elif event.type == pg.MOUSEBUTTONDOWN:
            print("event", event)
            if event.button == 4:
                self.inensity[self.mousebutton] = min(255, self.inensity[self.mousebutton] + self.rotary_step)
            elif event.button == 5:
                self.inensity[self.mousebutton] = max(0, self.inensity[self.mousebutton] - self.rotary_step)
            else:
                super(Gameplay1aa, self).get_event(event)

        elif event.type == pg.KEYDOWN:
            if event.unicode == 'r':
                self.mousebutton = 0
            elif event.unicode == 'g':
                self.mousebutton = 1
            elif event.unicode == 'b':
                self.mousebutton = 2
            else:
                super(Gameplay1aa, self).get_event(event)
        else:
            super(Gameplay1aa, self).get_event(event)

    def startup(self, persistent):
        self.persist = persistent
        self.color = self.persist["choice"] if "choice" in self.persist else COLORS[random.randint(0, len(COLORS)-1)]
        if "random" in self.persist:
            self.inensity = self.persist["random"]
        else:
            r = COLORS[random.randint(0, len(COLORS) - 1)][1]
            self.inensity = [r.r, r.g, r.b]
        self.rt = interpolate(self.color[1].r,self.color[1].g,self.color[1].b)

        self.rgb_txt = [
            "Lainepikkus "+ str(RGB[0][5]) + " nm, valgustugevus "+str(100*self.color[1].r // 255)+"%    [  hetke valgustugevus:                   ]",
            "Lainepikkus "+ str(RGB[1][5]) + " nm, valgustugevus "+str(100*self.color[1].g // 255)+"%    [  hetke valgustugevus:                   ]",
            "Lainepikkus "+ str(RGB[2][5]) + " nm, valgustugevus "+str(100*self.color[1].b // 255)+"%    [  hetke valgustugevus:                   ]",
        ]
        #self.rgb_txt = [
        #    "Lainepikkus "+ str(RGB[0][5]) + " nm, valgustugevus [            ]",
        #    "Lainepikkus "+ str(RGB[1][5]) + " nm, valgustugevus [            ]",
        #    "Lainepikkus "+ str(RGB[2][5]) + " nm, valgustugevus [            ]",
        #]

        self.color_txt = "Domineeriv lainepikkus "+ str(self.color[5]) + " nm, valgustugevus "+str(self.color[4])+"%"

        self.title_with_color = self.title + " - " + self.color[0]


    def update(self, dt):
        dmx.send_rgb(*self.inensity)
        dmx.send_rt(self.rt[self.inensity[0]][0], self.rt[self.inensity[1]][1], self.rt[self.inensity[2]][2])


    def draw(self, surface):

        self.bubble.draw(surface)
        self.ht.draw(surface)


        #pg.draw.circle(surface, self.color[1], (1105, 280), 20, 0);
        for i in range(0, 3):
            pg.gfxdraw.filled_circle(surface, 140, 380 + i * 80, 33, RGB[i][1])
            pg.gfxdraw.aacircle(surface, 140, 380 + i * 80, 33, RGB[i][1])

            self.font.render_to(surface, (240, 370+i*80), self.rgb_txt[i])
            self.font.render_to(surface,  (910, 370+i*80), str(round(self.inensity[i]/255*100))+"%")

        self.font.render_to(surface, (570, 420+0*80), "+")
        self.font.render_to(surface, (570, 420+1*80), "+")
        self.font.render_to(surface, (570, 430+2*80), "=")
        
        pg.gfxdraw.filled_circle(surface, 140, 400+3*80, 33, self.color[1])
        pg.gfxdraw.aacircle(surface, 140, 400+3*80, 33, self.color[1])
        self.font.render_to(surface, (240, 390+3*80), self.color_txt)
        
        #pg.draw.rect(surface, pg.Color(self.inensity[0],self.inensity[1],self.inensity[2],255), self.rect)

    def chek_result(self):
        self.next_state = "RESULT"
        result = 10 > statistics.stdev([abs(self.color[1].r - self.inensity[0]), abs(self.color[1].g - self.inensity[1]), abs(self.color[1].b - self.inensity[2])])
        print("chek_result", result)
        self.persist["result"] = result
        self.persist["next_state"] = "GAMEPLAY1" if result else "GAMEPLAY1aa"
        self.persist["title"] = self.title
        self.persist["random"] = self.inensity



class Gameplay1b(Gameplay1aa):
    title = "Sega kokku oma lemmikvärv"
    text = ["Sega ise värvid kokku. Selleks keera prožektori nupud õigetele valgustugevustele",
                 "Kinnita oma valikut punase nupuga"]
    center = config.load("positions", "center", [[0,0], [0,0], [0,0]])
    
    def __init__(self):
        super(Gameplay1b, self).__init__()
        self.ht = AnimatedSprite(position=(980, 196), images=load_images("images/ht/color"))
        self.bubble = Sprite(position=(106, 216), image=load_image("images/bubbles/gameplay1b.png"))

    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS)-1)]
        super(Gameplay1b, self).startup(persistent)
        dmx.send_rt(*self.center)
        self.rgb_txt = [
            "Lainepikkus "+ str(RGB[0][5]) + " nm, valgustugevus [                ]",
            "Lainepikkus "+ str(RGB[1][5]) + " nm, valgustugevus [                ]",
            "Lainepikkus "+ str(RGB[2][5]) + " nm, valgustugevus [                ]",
        ]
        
    def update(self, dt):
        dmx.send_rgb(*self.inensity)
        
    def chek_result(self):
        self.next_state = "GAMEPLAY1ba"
        self.persist["rgb"] = self.inensity
        print("chek_result", self.persist)
        
    def draw(self, surface):
        self.bubble.draw(surface)
        self.ht.draw(surface)


        for i in range(0, 3):
            pg.gfxdraw.filled_circle(surface, 140, 380 + i * 110, 33, RGB[i][1])
            pg.gfxdraw.aacircle(surface, 140, 380 + i * 110, 33, RGB[i][1])

            self.font.render_to(surface, (230, 370+i*110), self.rgb_txt[i])
            self.font.render_to(surface, (600, 370 + i * 110), str(round(self.inensity[i]/255*100))+"%", pg.Color("gray10"))


        
class Gameplay1ba(Result):
    title = "Sega kokku oma lemmikvärv"
    title_orig = "Sega kokku oma lemmikvärv"

    rt = config.load("positions", "offset", [[0,0], [0,0], [0,0]])

    def __init__(self):
        super(Gameplay1ba, self).__init__()
        self.next_state = "GAMEPLAY1"
        self.bubbles = [Sprite(position=(125, 224), image=load_image("images/bubbles/gameplay1ba.png"))]
        self.result = 0

    def startup(self, persistent):
        self.persist = persistent
        dmx.send_rt(*self.rt)
        self.closest = None
        self.intensity = self.persist["rgb"] if "rgb" in self.persist else [243,43,34];
        print("intensiry", self.intensity)
        min_stdev = 10
        min_index = 0
        for i,color in enumerate(ALL_COLORS):
            stdev = statistics.stdev([abs(color[1].r - self.intensity[0]), abs(color[1].g - self.intensity[1]), abs(color[1].b - self.intensity[2])])
            if stdev < min_stdev:
                min_stdev = stdev
                min_index = i
        self.closest = ALL_COLORS[min_index]
        #if min_stdev < 5:
        #    self.title = ALL_COLORS[min_index][0]
        #else:
        #    self.title = self.title_orig
        print("stdev", min_stdev, self.closest)




    def draw(self, surface):
        super(Gameplay1ba, self).draw(surface)
        (x, y) = self.screen_rect.center

        pg.gfxdraw.filled_circle(surface, x-100, y+130, 100, self.intensity)
        pg.gfxdraw.aacircle(surface, x-100, y+130, 100, pg.Color("black"))

