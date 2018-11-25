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
    title_txt = "Kalibreeri prozektorire asukohti"
    
    def __init__(self):
        super(Calibrate, self).__init__()

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
    help = "Punane - pööra, Roheline - kalluta, Enter - salvesta"

    def __init__(self):
        super(CalibrateBase, self).__init__()
        self.next_state = "MAINMENU"

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

        self.title_font.render_to(surface, (240, 40), self.title)
        self.font.render_to(surface, (300, 320), self.help)
        self.title_font.render_to(surface, (400, 260), self.states[self.state])

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
