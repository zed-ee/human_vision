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

    title_txt = "Kuidas värve segada?"

    def startup(self, persistent):
        self.choices = random.sample(COLORS, 9)
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
                xy = (250+j*400, 300+i*140)
                if i*3+j == self.active_choice:
                    pg.draw.circle(surface, pg.Color(255, 255, 255 , 0) - color[1], xy, 55, 7)
                pg.draw.circle(surface, color[1], xy, 50, 0)

    def update(self, dt):
        c = self.choices[self.active_choice][1]
        dmx.send_rgb(c.r, c.g, c.b)

class Gameplay1aa(GamePlay):
       
    text = ["Värve saab kombineerida erinevatest lainepikkustest. Sega kolmes põhivärvist soovitud        kokku. ",
                 "Selleks tuleb sul prožektori valgused seadistades õigetele valgustugevustele kasutades pöördnuppe."]
    title = "Leia õige lainepikkus"
    
    def __init__(self):
        super(Gameplay1aa, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128)).move(960, 420)
        self.x_velocity = 1
        self.next_state = "RESULT"


        text_txt = [self.font.render(text, True, pg.Color("gray10")) for text in self.text ]
        title_rect = [title.get_rect(center=self.screen_rect.center).move(0, -i*70-100) for i, title in enumerate(text_txt)]
        self.titles = list(zip(text_txt, title_rect))
        self.plus_txt = self.title_font.render("+", True, pg.Color("gray10"))
        self.equals_txt = self.title_font.render("=", True, pg.Color("gray10"))

        self.title_txt = self.title_font.render(self.title, True, pg.Color("gray10"))
        self.title_rect = self.title_txt.get_rect(center=self.screen_rect.center).move(0, -220)

    def get_event(self, event):
        if event.type == ROTARY_BUTTON:
            if event.direction == 1:
               self.inensity[event.button] = min(255, self.inensity[event.button] + 1)
            else:
               self.inensity[event.button] = max(0, self.inensity[event.button] - 1)
        else:
            super(Gameplay1aa, self).get_event(event)

    def startup(self, persistent):
        print("startup", persistent)
        self.persist = persistent
        print(self.persist)
        r = COLORS[random.randint(0, len(COLORS)-1)][1]
        self.color = self.persist["choice"]
        self.inensity = [r.r, r.g, r.b]
        print("startup", self.color[1].r,self.color[1].g,self.color[1].b)
        self.rt = interpolate(self.color[1].r,self.color[1].g,self.color[1].b)
        
        #rgb = [
        #    "Lainepikkus "+ str(RGB[0][5]) + "nm, valgustugevus "+str(100*self.color[1].r // 255)+"% [hetke valgustugevus:            ]",
        #    "Lainepikkus "+ str(RGB[1][5]) + "nm, valgustugevus "+str(100*self.color[1].g // 255)+"% [hetke valgustugevus:            ]",
        #    "Lainepikkus "+ str(RGB[2][5]) + "nm, valgustugevus "+str(100*self.color[1].b // 255)+"% [hetke valgustugevus:            ]",
        #]
        rgb = [
            "Lainepikkus "+ str(RGB[0][5]) + "nm, valgustugevus [            ]",
            "Lainepikkus "+ str(RGB[1][5]) + "nm, valgustugevus [            ]",
            "Lainepikkus "+ str(RGB[2][5]) + "nm, valgustugevus [            ]",
        ]        
        c = "Domineeriv lainepikkus "+ str(self.color[5]) + "nm, valgustugevus "+str(self.color[4])+"%"
        self.rgb_txt = [self.font.render(text, True, pg.Color("gray10")) for text in rgb ]
        self.color_txt = self.font.render(c, True, pg.Color("gray10"))

    def update(self, dt):
        dmx.send_rgb(*self.inensity)
        dmx.send_rt(self.rt[self.inensity[0]][0], self.rt[self.inensity[1]][1], self.rt[self.inensity[2]][2])
        result = statistics.stdev([abs(self.color[1].r - self.inensity[0]), abs(self.color[1].g - self.inensity[1]), abs(self.color[1].b - self.inensity[2])])
        print(result)

    def draw(self, surface):
        # move to update
        intensities = [self.font.render(str(round(ii/255*100))+"%", True, pg.Color("gray10")) for ii in self.inensity]
        surface.fill( pg.Color("darkgreen"))
        surface.blit(self.title_txt, self.title_rect)

        surface.blit(self.titles[0][0], self.titles[0][1])
        surface.blit(self.titles[1][0], self.titles[1][1])

        pg.draw.circle(surface, self.color[1], (1105, 280), 20, 0);
        for i in range(0, 3):
            pg.draw.circle(surface, RGB[i][1], (200, 410+i*100), 20, 0);
            surface.blit(self.rgb_txt[i], (300, 400+i*100))
            surface.blit(intensities[i], (700, 400+i*100))
            
        surface.blit(self.plus_txt, (530, 430+0*100))
        surface.blit(self.plus_txt, (530, 430+1*100))
        surface.blit(self.equals_txt, (530, 430+2*100))
        
        pg.draw.circle(surface, self.color[1], (200, 410+3*100), 23, 0);
        surface.blit(self.color_txt, (300, 400+3*100))
        
        #pg.draw.rect(surface, pg.Color(self.inensity[0],self.inensity[1],self.inensity[2],255), self.rect)

    def chek_result(self):
        self.next_state = "RESULT"
        result = 10 > statistics.stdev([abs(self.color[1].r - self.inensity[0]), abs(self.color[1].g - self.inensity[1]), abs(self.color[1].b - self.inensity[2])])
        print("chek_result", result)
        self.persist["result"] = result
        self.persist["next_state"] = "MAINMENU" if result else "GAMEPLAY1aa"


class Gameplay1b(Gameplay1aa):
    title = "Sega kokku oma lemmikvärv"
    text = ["Sega ise värvid kokku. Selleks keera prožektori nupud õigetele pikkustele",
                 "Kinnita oma valikut punase nupuga"]
    center = config.load("positions", "center", [[0,0], [0,0], [0,0]])
    
    def __init__(self):
        super(Gameplay1b, self).__init__()
        
    def startup(self, persistent):
        persistent["choice"] = COLORS[random.randint(0, len(COLORS)-1)]
        super(Gameplay1b, self).startup(persistent)
        dmx.send_rt(*self.center)

        
    def update(self, dt):
        pass
        
    def chek_result(self):
        self.next_state = "GAMEPLAY1ba"
        self.persist["rgb"] = self.inensity
        print("chek_result", self.persist)
        
    def draw(self, surface):
        # move to update
        intensities = [self.font.render(str(round(ii/255*100))+"%", True, pg.Color("gray10")) for ii in self.inensity]
        surface.fill( pg.Color("darkgreen"))
        surface.blit(self.title_txt, self.title_rect)

        surface.blit(self.titles[0][0], self.titles[0][1])
        surface.blit(self.titles[1][0], self.titles[1][1])

        for i in range(0, 3):
            pg.draw.circle(surface, RGB[i][1], (200, 410+i*100), 20, 0);
            surface.blit(self.rgb_txt[i], (300, 400+i*100))
            surface.blit(intensities[i], (700, 400+i*100))
            

        
class Gameplay1ba(GamePlay):
    title = "Sega kokku oma lemmikvärv"
    text = "Mulle meeldib ka see värv väga!"
    
    sidebyside = config.load("positions", "sidebyside", [[0,0], [0,0], [0,0]])
    
    def __init__(self):
        super(Gameplay1ba, self).__init__()
   
    def startup(self, persistent):
        self.persist = persistent
        dmx.send_rt(*self.sidebyside)

             
    def draw(self, surface):
        pg.draw.circle(surface, self.persist["rgb"], self.screen_rect.center, 160, 0);
        self.title_font.render_to(surface, (40, 350), "Hello World!", (0, 0, 255))

    
        