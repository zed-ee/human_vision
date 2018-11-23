# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
from states.mainmenu import MainMenu
from states.help import Help
from userevents import *
from dmx import dmx
from config import config

class Calibrate(MainMenu):
    choices_txt = ["Peamenüü", "Kuidas värve segada?", "Kuidas ekraan töötab?", "Miks paistavad asjad nii nagu nad paistavad?", "Tagasi"]
    states = ["CALIBRATE0", "CALIBRATE1", "CALIBRATE2", "CALIBRATE3", "MAINMENU"]
    title_txt = "KUIDAS ME MAAILMA NÄEME?"
    
    def __init__(self):
        super(Calibrate, self).__init__()
        self.title = self.title_font.render("Kalibreeri prozektorire asukohti", True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center).move(0, -220)
        
    def startup(self, persistent):
        dmx.send_rgb(80,80,80)
        dmx.send_rt([0,0],[0,0], [0,0])

class Calibrate0(GameState):
    screen_color = pg.Color("dodgerblue")

    states = [
        "Liiguta punane keskele", 
        "Liiguta roheline keskele", 
        "Liiguta sinine keskele", 
        ]
    state = 0
    led = 0
    mode = 0
    rt = config.load("MAINMENU", "rt", [[0,0],[0,0], [0,0]]) # rotation & tilt
        
    def __init__(self):
        super(Calibrate0, self).__init__()
        self.next_state = "MAINMENU"
        self.texts = [self.title_font.render(text, True, pg.Color("purple")) for text in self.states]
        self.texts_rect = [text.get_rect(center=self.screen_rect.center) for text in self.texts]
        self.help = self.font.render("Punane - pööra, Roheline - kalluta, Enter - salvesta", True, pg.Color("purple"))
        
    def startup(self, persistent):
        dmx.send_rgb(255,255,255)
        dmx.send_rt(*self.rt)
        
    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            config.save("MAINMENU", "rt", self.rt)
            self.state = (self.state + 1) % len(self.states)
            self.led = self.state % 3
            self.mode = self.state // 3
        elif (event.type == PUSH_BUTTON and event.button == BUTTONS.BACK) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 2):
            self.persist["state"] = "MAINMENU"
            self.done = True
        elif event.type == ROTARY_BUTTON and event.button != 2:
            if event.direction == 1:
                self.rt[self.led][event.button] = (self.rt[self.led][event.button] + 1) % 255
            else:
                self.rt[self.led][event.button] = (self.rt[self.led][event.button] - 1) % 255
                
            dmx.send_rt(*self.rt)

    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.texts[self.state], self.texts_rect[self.state])
        
        
        
class Calibrate1(Calibrate0):

    states = [
        "Liiguta punane keskele", 
        "Liiguta roheline keskele", 
        "Liiguta sinine keskele", 

        "Liiguta punane ühte äärde", 
        "Liiguta roheline ühte äärde", 
        "Liiguta sinine ühte äärde", 

        "Liiguta punane teise äärde",
        "Liiguta roheline teise äärde",
        "Liiguta sinine teise äärde"
        ]
    modes = ["center", "conrner1", "conrner1"]
    
