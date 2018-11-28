# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
import random
from states.mainmenu import *
import statistics
random.seed()
from colors import *
from interpolate import interpolate

class Gameplay1(MainMenu):
    choices = [
        "Leia õige lainepikkus",
        "Sega kokku oma lemmikvärv"
    ]
    states = ["GAMEPLAY1a", "GAMEPLAY1b"]
    title_txt = "Kuidas värve segada?"
    rts = [
        config.load("positions", "offset", [[0,0],[0,0], [0,0]]),
        config.load("positions", "sidebyside", [[0,0],[0,0], [0,0]])
    ]

    def update(self, dt):
        dmx.send_rt(*(self.rts[self.active_choice]))

class Gameplay1a(SubMenu):

    states = ["GAMEPLAY1aa" for i in range(0, 9)]

    title_txt = "Leia õige lainepikkus?"
    text = ["Värvid koosnevad erinevatest lainepikkustest. Vali värv, mida soovid kokku segada. ",
            "Kinnita oma valikut …. nupuga"]

    def startup(self, persistent):
        self.choices = random.sample(COLORS, 9)
        self.titles = [color[0] for color in self.choices]
        for c in self.choices:
            print(c)
        self.rt = config.load("positions", "center", [[0,0],[0,0], [0,0]])
        self.persist = persistent
        dmx.send_rt(*self.rt)

    def draw(self, surface):
        super(Gameplay1a, self).draw(surface)
        for i in range(0, 3):
            for j in range(0, 3):
                color = self.choices[i*3+j]
                xy1 = (240+j*400, 310+i*140)
                xy2 = (300+j*400, 300+i*140)
                if i*3+j == self.active_choice:
                    pg.draw.circle(surface, pg.Color(255, 255, 255 , 0) - color[1], xy1, 55, 7)
                pg.draw.circle(surface, color[1], xy1, 50, 0)
                self.font.render_to(surface, xy2, self.titles[i*3+j])

    def update(self, dt):
        c = self.choices[self.active_choice][1]
        dmx.send_rgb(c.r, c.g, c.b)

class Gameplay1aa(GamePlay):
       
    text = ["Värve saab kombineerida erinevatest lainepikkustest. Sega kolmes põhivärvist kokku valitud värv. ",
                 "Selleks tuleb sul prožektori valgused seadistada õigetele valgustugevustele, kasutades pöördnuppe."]
    title = "Leia õige lainepikkus"
    
    def __init__(self):
        super(Gameplay1aa, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128)).move(960, 420)
        self.x_velocity = 1
        self.next_state = "MAINMENU"

    def get_event(self, event):
        if event.type == ROTARY_BUTTON:
            if event.direction == 1:
               self.inensity[event.button] = min(255, self.inensity[event.button] + 1)
            else:
               self.inensity[event.button] = max(0, self.inensity[event.button] - 1)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.inensity[0] = min(255, self.inensity[0] + 1)
            elif event.button == 5:
                self.inensity[0] = max(0, self.inensity[0] - 1)
        else:
            super(Gameplay1aa, self).get_event(event)

    def startup(self, persistent):
        self.persist = persistent
        r = COLORS[random.randint(0, len(COLORS)-1)][1]
        self.color = self.persist["choice"]
        self.inensity = [r.r, r.g, r.b]
        self.rt = interpolate(self.color[1].r,self.color[1].g,self.color[1].b)

        self.rgb_txt = [
            "Lainepikkus "+ str(RGB[0][5]) + " nm, valgustugevus "+str(100*self.color[1].r // 255)+"%    [  hetke valgustugevus:              ]",
            "Lainepikkus "+ str(RGB[1][5]) + " nm, valgustugevus "+str(100*self.color[1].g // 255)+"%    [  hetke valgustugevus:              ]",
            "Lainepikkus "+ str(RGB[2][5]) + " nm, valgustugevus "+str(100*self.color[1].b // 255)+"%    [  hetke valgustugevus:              ]",
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

        surface.fill( pg.Color("darkgreen"))
        self.title_font.render_to(surface, (300, 40), self.title_with_color)

        self.font.render_to(surface, (300, 120), self.text[0])
        self.font.render_to(surface, (300, 160), self.text[1])

        #pg.draw.circle(surface, self.color[1], (1105, 280), 20, 0);
        for i in range(0, 3):
            pg.draw.circle(surface, RGB[i][1], (200, 310+i*100), 30, 0);
            self.font.render_to(surface, (300, 300+i*100), self.rgb_txt[i])
            self.font.render_to(surface,  (960, 300+i*100), str(round(self.inensity[i]/255*100))+"%")

        self.font.render_to(surface, (530, 350+0*100), "+")
        self.font.render_to(surface, (530, 350+1*100), "+")
        self.font.render_to(surface, (530, 350+2*100), "=")
        
        pg.draw.circle(surface, self.color[1], (200, 310+3*100), 33, 0)
        self.font.render_to(surface, (300, 300+3*100), self.color_txt)
        
        #pg.draw.rect(surface, pg.Color(self.inensity[0],self.inensity[1],self.inensity[2],255), self.rect)

    def chek_result(self):
        self.next_state = "RESULT"
        result = 10 > statistics.stdev([abs(self.color[1].r - self.inensity[0]), abs(self.color[1].g - self.inensity[1]), abs(self.color[1].b - self.inensity[2])])
        print("chek_result", result)
        self.persist["result"] = result
        self.persist["next_state"] = "MAINMENU" if result else "GAMEPLAY1aa"


class Gameplay1b(Gameplay1aa):
    title = "Sega kokku oma lemmikvärv"
    text = ["Sega ise värvid kokku. Selleks keera prožektori nupud õigetele valgustugevustele",
                 "Kinnita oma valikut punase nupuga"]
    center = config.load("positions", "center", [[0,0], [0,0], [0,0]])
    
    def __init__(self):
        super(Gameplay1b, self).__init__()
        
    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS)-1)]
        super(Gameplay1b, self).startup(persistent)
        dmx.send_rt(*self.center)
        self.rgb_txt = [
            "Lainepikkus "+ str(RGB[0][5]) + " nm, valgustugevus [            ]",
            "Lainepikkus "+ str(RGB[1][5]) + " nm, valgustugevus [            ]",
            "Lainepikkus "+ str(RGB[2][5]) + " nm, valgustugevus [            ]",
        ]
        
    def update(self, dt):
        dmx.send_rgb(*self.inensity)
        
    def chek_result(self):
        self.next_state = "GAMEPLAY1ba"
        self.persist["rgb"] = self.inensity
        print("chek_result", self.persist)
        
    def draw(self, surface):
        surface.fill( pg.Color("darkgreen"))
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (300, 120), self.text[0])
        self.font.render_to(surface, (300, 160), self.text[1])

        for i in range(0, 3):
            pg.draw.circle(surface, RGB[i][1], (200, 360+i*100), 20, 0)
            self.font.render_to(surface, (300, 350+i*100), self.rgb_txt[i])
            self.font.render_to(surface, (670, 350 + i * 100), str(round(self.inensity[i]/255*100))+"%", pg.Color("gray10"))


        
class Gameplay1ba(GamePlay):
    title = "Sega kokku oma lemmikvärv"
    text = ["Mulle meeldib ka see värv väga!",
            "See meenutab mulle värvi nimega 'x'"]

    rt = config.load("positions", "offset", [[0,0], [0,0], [0,0]])

    def __init__(self):
        super(Gameplay1ba, self).__init__()
        self.next_state = "MAINMENU"

    def startup(self, persistent):
        self.persist = persistent
        dmx.send_rt(*self.rt)
        self.closest = None
        self.intensity = self.persist["rgb"];
        min_stdev = 10
        min_index = 0
        for i,color in enumerate(ALL_COLORS):
            stdev = statistics.stdev([abs(color[1].r - self.intensity[0]), abs(color[1].g - self.intensity[1]), abs(color[1].b - self.intensity[2])])
            if stdev < min_stdev:
                min_stdev = stdev
                min_index = i
        self.closest = ALL_COLORS[min_index]



    def draw(self, surface):
        surface.fill( pg.Color("darkgreen"))
        pg.draw.circle(surface, self.intensity, self.screen_rect.center, 160, 0);
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (400, 620), self.text[0])
        if self.closest is not None:
            self.font.render_to(surface, (400, 660), self.text[1].replace("x", self.closest[0]))


class Gameplay1ba(GamePlay):
    title = "Sega kokku oma lemmikvärv"
    text = ["Mulle meeldib ka see värv väga!",
            "See meenutab mulle värvi nimega 'x'"]

    rt = config.load("positions", "offset", [[0, 0], [0, 0], [0, 0]])

    def __init__(self):
        super(Gameplay1ba, self).__init__()
        self.next_state = "MAINMENU"

    def startup(self, persistent):
        self.persist = persistent
        dmx.send_rt(*self.rt)
        self.closest = None
        self.intensity = self.persist["rgb"];
        min_stdev = 10
        min_index = 0
        for i, color in enumerate(ALL_COLORS):
            stdev = statistics.stdev([abs(color[1].r - self.intensity[0]), abs(color[1].g - self.intensity[1]),
                                      abs(color[1].b - self.intensity[2])])
            if stdev < min_stdev:
                min_stdev = stdev
                min_index = i
        self.closest = ALL_COLORS[min_index]

    def draw(self, surface):
        surface.fill(pg.Color("darkgreen"))
        pg.draw.circle(surface, self.intensity, self.screen_rect.center, 160, 0);
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (400, 620), self.text[0])
        if self.closest is not None:
            self.font.render_to(surface, (400, 660), self.text[1].replace("x", self.closest[0]))


