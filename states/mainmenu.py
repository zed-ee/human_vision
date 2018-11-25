# -*- coding: utf-8 -*-
import pygame as pg
from gamestate import GameState
from userevents import *
from dmx import dmx, COLOR_WHEEL
DEV = True
from config import config

class MainMenu(GameState):
    choices = [
        "Kuidas värve segada?", 
        "Kuidas ekraan töötab?", 
        "Miks paistavad asjad nii nagu nad paistavad?", 
        "Kalibreeri",
        "Mängu kasutusõpetus"
    ]
    states = ["GAMEPLAY1", "GAMEPLAY2", "GAMEPLAY3", "CALIBRATE", "HELP"]
    title_txt = "KUIDAS ME MAAILMA NÄEME?"
    active_choice = 0

    def __init__(self):
        super(MainMenu, self).__init__()
        self.next_state = self.states[self.active_choice]
        self.backgrounds = [pg.image.load("images/intro_bg_"+color+".png") for color in ["red", "green", "blue", "grey"]]

        self.screen_color = pg.Color("grey")
        self.previous_state = "MAINMENU"

    def startup(self, persistent):
        self.rt = config.load("positions", "offset", [[[0,0],[0,0], [0,0]]])
        self.persist = persistent
        dmx.send_rgb(255, 255, 255)
        dmx.send_rt(*self.rt)
        self.active_choice = 0

    def get_selection(self):
        self.next_state = self.states[self.active_choice]
        self.persist["state"] = self.next_state
        self.persist["choice"] = self.choices[self.active_choice]

    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            self.get_selection()
            self.done = True
        elif (event.type == PUSH_BUTTON and event.button == BUTTONS.BACK) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 2):
            self.next_state = self.previous_state
            self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.active_choice = (self.active_choice - 1) % len(self.choices)
            if event.button == 5:
                self.active_choice = (self.active_choice + 1) % len(self.choices)
        elif event.type == ROTARY_BUTTON:
            if event.direction == 1:
                self.active_choice = (self.active_choice + 1) % len(self.choices)
            else:
                self.active_choice = (self.active_choice - 1) % len(self.choices)

        if self.states[self.active_choice] == "": #skip event if no state
            self.get_event(event)
            return;
           
    def update(self, dt):
        dmx.set_mode(COLOR_WHEEL[self.active_choice % 3], COLOR_WHEEL[(self.active_choice+1) % 3], COLOR_WHEEL[(self.active_choice+2) % 3])
        

        
    def draw(self, surface):
        #surface.fill(self.screen_color)

        surface.blit(self.backgrounds[self.active_choice % len(self.backgrounds)], (0, 0))
        self.title_font.render_to(self.title, (0,0))
        for i, choice in enumerate(self.choices_txt):
            if self.states[i] == "":
                continue
            y_help = 0#100 if i == 4 else 0
            rect = pg.Rect((0, 96*i), (0, 96*i + 96)).move(200, 300 + y_help)
            surface.blit(choice, rect)
            if i == self.active_choice:
                pg.draw.circle(surface, pg.Color("red"), (120, 310+96*i + y_help), 20, 0);

class GamePlay(GameState):
    back = "MAINMENU"
    def chek_result(self):
        pass
        
    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.BACK) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 2):
            self.done = True        
        elif (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            self.chek_result()
            self.done = True
            
class SubMenu(MainMenu):
    choices = []

    def __init__(self):
        super(SubMenu, self).__init__()

    def draw(self, surface):
        surface.fill(self.screen_color)
        
        
class Result(GameState):
    texts = ["PROOVI VEEL", "ÕIGE"]
    image = pg.image.load("images/ht_result.jpg")
    next_state = "MAINMENU"
    
    def __init__(self):
        super(Result, self).__init__()
        self.title = [self.title_font.render(title, pg.Color("darkblue")) for title in self.texts]
    
    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            self.next_state = self.persist["next_state"]
            print("self.next_state", self.next_state)
            self.done = True
        elif (event.type == PUSH_BUTTON and event.button == BUTTONS.BACK) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 2):
            self.done = True
            
    def draw(self, surface):
        surface.fill( pg.Color("darkgreen"))
        surface.blit(self.image, (500, 30))
        surface.blit(self.title[self.persist["result"]], self.title_rects[self.persist["result"]])
    
