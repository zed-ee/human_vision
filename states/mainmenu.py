# -*- coding: utf-8 -*-
import pygame as pg
from gamestate import GameState
from userevents import *
from dmx import dmx
DEV = True
from config import config

class MainMenu(GameState):
    choices_txt = [
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
        self.title = self.title_font.render(self.title_txt, True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center).move(0, -220)
        self.next_state = self.states[self.active_choice]
        self.backgrounds = [pg.image.load("images/intro_bg_"+color+".png") for color in ["red", "green", "blue", "grey"]]

        self.choices = [self.font.render(txt, True, pg.Color("white")) for txt in self.choices_txt]
        self.screen_color = pg.Color("grey")
        
    def startup(self, persistent):
        dmx.send_rgb(255,0,0)
        dmx.send_rt(*config.load("MAINMENU", "rt", [[0,0],[0,0], [0,0]]))
        
    def get_event(self, event):
        if (event.type == PUSH_BUTTON and event.button == BUTTONS.ENTER) or \
            (event.type == pg.MOUSEBUTTONUP and event.button == 1):
            self.next_state = self.states[self.active_choice]
            self.persist["state"] = self.next_state
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
           
        dmx.send_rgb(255 if self.active_choice > 0 else 0, 255 if self.active_choice > 1 else 0, 255 if self.active_choice > 2 else 0)
        
    def draw(self, surface):
        surface.fill(self.screen_color)

        #surface.blit(self.backgrounds[self.active_choice], (0, 0))
        surface.blit(self.title, self.title_rect)
        for i, choice in enumerate(self.choices):
            if self.states[i] == "":
                continue
            y_help = 0#100 if i == 4 else 0
            rect = pg.Rect((0, 96*i), (0, 96*i + 96)).move(200, 300 + y_help)
            surface.blit(choice, rect)
            if i == self.active_choice:
                pg.draw.circle(surface, pg.Color("red"), (120, 310+96*i + y_help), 20, 0);

