# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
from states.mainmenu import MainMenu
from states.help import Help
from userevents import *
from dmx import dmx
from config import config

class Calibrate(MainMenu):
    choices = ["Keskpunkt", "Keskpunkt, nihkega", "Kõrvuti", "Laiali 1", "Laiali 2"]
    states = ["CALIBRATE_CENTER", "CALIBRATE_OFFSET", "CALIBRATE_SIDEBYSIDE", "CALIBRATE_LOW", "CALIBRATE_HIGH"]
    title_txt = "KUIDAS ME MAAILMA NÄEME?"
    
    def __init__(self):
        super(Calibrate, self).__init__()
        self.title = self.title_font.render("Kalibreeri prozektorire asukohti", True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center).move(0, -220)
        
    def startup(self, persistent):
        dmx.send_rgb(255,255,255)
        dmx.send_rt([0,0],[0,0], [0,0])

    def update(self, dt):
        conf = self.states[self.active_choice][10:].lower()
        dmx.send_rt(*config.load("positions", conf, [[0,0],[0,0], [0,0]]))
        
class CalibrateBase(GameState):
    screen_color = pg.Color("dodgerblue")

    states = [
        "Liiguta punast", 
        "Liiguta rohelist", 
        "Liiguta sinist", 
        ]
    state = 0
    led = 0
    mode = 0
    title = ""
    rt = [[0,0],[0,0], [0,0]] # rotation & tilt
    conf = ""
    
    def __init__(self):
        super(CalibrateBase, self).__init__()
        self.next_state = "MAINMENU"
        self.texts = [self.title_font.render(text, True, pg.Color("purple")) for text in self.states]
        self.texts_rect = [text.get_rect(center=self.screen_rect.center) for text in self.texts]
        self.help_text = self.font.render("Punane - pööra, Roheline - kalluta, Enter - salvesta", True, pg.Color("purple"))
        self.help_rect = self.help_text.get_rect(center=self.screen_rect.center).move(0,200)
        self.title_text = self.font.render(self.title, True, pg.Color("purple"))
        self.title_rect = self.title_text.get_rect(center=self.screen_rect.center).move(0,-200)
        
    def startup(self, persistent):
        self.rt = config.load("positions", self.conf, [[0,0],[0,0], [0,0]]) # rotation & tilt
        dmx.send_rgb(255,255,255)
        dmx.send_rt(*self.rt)
        self.back = "CALIBRATE"
        
    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            config.save("positions", self.conf, self.rt)
            self.state = (self.state + 1) % len(self.states)
            self.led = self.state % 3
            self.mode = self.state // 3
        elif (event.type == PUSH_BUTTON and event.button == BUTTONS.BACK) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 2):
            self.persist["state"] = "MAINMENU"
            self.next_state = self.back
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
        surface.blit(self.help_text, self.help_rect)
        surface.blit(self.title_text, self.title_rect)
        
        
     
class CalibrateCenter(CalibrateBase):
    title = "Liiguta prozektorid keskele, valge värvi saamiseks"
    conf = "center"    

class CalibrateOffset(CalibrateBase):
    conf = "offset"
    title = "Liiguta prozektorid keskele, üksteise suhtes veidi nihkesse"

class CalibrateSideBySide(CalibrateBase):
    title = "Liiguta prozektorid keskele, üksteise kõrvale"
    conf = "sidebyside"
    
class CalibrateLow(CalibrateBase):
    title = "Liiguta prozektorid ühte äärmusse"
    conf = "low"

class CalibrateHigh(CalibrateBase):
    title = "Liiguta prozektorid teise äärmusse"
    conf = "high"
