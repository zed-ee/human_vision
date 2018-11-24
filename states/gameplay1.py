# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
import random
from states.mainmenu import *
import statistics
random.seed()
from colors import *

class Gameplay1(MainMenu):
    choices = [
        "Leia õige lainepikkus",
        "Sega kokku oma lemmikvärv"
    ]
    states = ["GAMEPLAY1a", "GAMEPLAY1b"]
    title_txt = "Kuidas värve segada?"


class Gameplay1a(SubMenu):

    states = ["GAMEPLAY1aa" for i in range(0, 9)]

    title_txt = "Kuidas värve segada?"

    def startup(self, persistent):
        self.choices = random.sample(COLORS, 9)

    def draw(self, surface):
        super(Gameplay1a, self).draw(surface)
        for i in range(0, 3):
            for j in range(0, 3):
                color = self.choices[i*3+j]
                xy = (250+j*400, 300+i*140)
                if i*3+j == self.active_choice:
                    pg.draw.circle(surface, pg.Color(255, 255, 255 , 0) - color[1], xy, 55, 7)
                pg.draw.circle(surface, color[1], xy, 50, 0)


class Gameplay1aa(GameState):
    def __init__(self):
        super(Gameplay1aa, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128)).move(960, 420)
        self.x_velocity = 1
        self.next_state = "GAMEPLAY1"
        text = ["Värve saab kombineerida erinevatest lainepikkustest. Sega kolmes põhivärvist soovitud        kokku. ",
                     "Selleks tuleb sul prožektori valgused seadistades õigetele valgustugevustele kasutades pöördnuppe."]

        text_txt = [self.font.render(text, True, pg.Color("gray10")) for text in text ]
        title_rect = [title.get_rect(center=self.screen_rect.center).move(0, -i*70-100) for i, title in enumerate(text_txt)]
        self.titles = list(zip(text_txt, title_rect))
        rgb = [
            "Lainepikkus "+ str(color[5]) + "nm, hetke valgustugevus: [           ]" for color in RGB
        ]
        self.rgb_txt = [self.font.render(text, True, pg.Color("gray10")) for text in rgb ]


    def startup(self, persistent):
        self.persist = persistent
        print(self.persist)
        self.color = self.persist["choice"]
        r = COLORS[random.randint(0, len(COLORS)-1)][1]
        self.inensity = [r.r, r.g, r.b]
        dmx.send_rgb(*self.inensity)


    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                self.done = True

    def draw(self, surface):
        # move to update
        intensities = [self.font.render(str(round(ii/255*100))+"%", True, pg.Color("gray10")) for ii in self.inensity]
        surface.fill( pg.Color("darkgreen"))

        surface.blit(self.titles[0][0], self.titles[0][1])
        surface.blit(self.titles[1][0], self.titles[1][1])

        pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)
        pg.draw.circle(surface, self.color[1], (1105, 280), 20, 0);
        for i in range(0, 3):

            pg.draw.circle(surface, RGB[i][1], (200, 410+i*100), 20, 0);
            surface.blit(self.rgb_txt[i], (300, 400+i*100))
            surface.blit(intensities[i], (760, 400+i*100))
        pg.draw.rect(surface, pg.Color(self.inensity[0],self.inensity[1],self.inensity[2],255), self.rect)


