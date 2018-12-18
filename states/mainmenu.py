# -*- coding: utf-8 -*-
import pygame as pg
from gamestate import *
from userevents import *
from dmx import dmx, COLOR_WHEEL
DEV = True
from config import config
from colors import *
from sprite import *
from animations import load_images

class MainMenu(GameState):
    choices = [
        "Kuidas värve segada?", 
        "Kuidas ekraan töötab?", 
        "Miks paistavad asjad nii nagu nad paistavad?", 
        "*Mängu kasutusõpetus"
    ]
    states = ["GAMEPLAY1", "GAMEPLAY2", "GAMEPLAY3", "HELP"]
    title = "Kuidas me maailma näeme?"
    active_choice = 0
    title_top = 78
    option_height = 115
    active_color = pg.Color(220, 98, 30)
    default_color = pg.Color(255, 255, 255)

    def __init__(self):
        super(MainMenu, self).__init__()
        self.next_state = self.states[self.active_choice]
        self.backgrounds = load_images('images/intro_bg')
        self.menu_font = pg.freetype.Font("fonts/Ranchers-Regular.ttf", 48)
        self.submenu_font = pg.freetype.Font("fonts/Ranchers-Regular.ttf", 36)
        self.ht = AnimatedSprite(position=(930, 196), images=load_images("images/ht/up"))

        self.screen_color = pg.Color("grey")
        self.previous_state = "MAINMENU"
        self.logo = LOGO.BLACK

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


    def update(self, dt):
        self.background = self.backgrounds[self.active_choice % len(self.backgrounds)]
        dmx.set_mode(COLOR_WHEEL[self.active_choice % 3], COLOR_WHEEL[(self.active_choice+1) % 3], COLOR_WHEEL[(self.active_choice+2) % 3])
        self.ht.update(dt)

        
    def draw(self, surface):
        for i, choice in enumerate(self.choices):
            if self.states[i] == "":
                continue
            h = self.option_height
            rect = pg.Rect((0, h*i), (0, h*i + h)).move(100, 286)
            color = self.active_color if i == self.active_choice else self.default_color
            if choice[0] == "*":
                rect.move_ip(150, 20)
                self.submenu_font.render_to(surface, rect, choice[1:], color)
            else:
                self.menu_font.render_to(surface, rect, choice, color)

        self.ht.draw(surface)

class GamePlay(GameState):
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
    default_color = pg.Color(0, 0, 0)

    rts = [
        config.load("positions", "offset", [[0,0],[0,0], [0,0]]),
        config.load("positions", "sidebyside", [[0,0],[0,0], [0,0]])
    ]

    def __init__(self):
        super(SubMenu, self).__init__()
        self.logo = LOGO.WHITE
        self.background = pg.Color("white")

        
class Result(GameState):
    texts = ["PROOVI VEEL", "ÕIGE"]
    image = pg.image.load("images/ht_result.jpg")
    next_state = "MAINMENU"
    
    def __init__(self):
        super(Result, self).__init__()

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
        self.title_font.render_to(surface, (550, 700), self.texts[self.persist["result"]] )

    
