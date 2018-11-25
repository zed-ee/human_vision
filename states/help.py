# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg

class Help(GameState):
    text = "Kahjuks pole meil veel juhendit"
    title = "Mängu kasutusjuhend"

    def __init__(self):
        super(Help, self).__init__()
        self.next_state = "MAINMENU"

    def startup(self, persistent):
        self.persist = persistent
        self.screen_color = pg.Color("dodgerblue")



    def get_event(self, event):
        self.done = True


    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.fill(self.screen_color)
        self.title_font.render_to(surface, (300, 40), self.title)
        self.font.render_to(surface, (300, 120), self.text)
