# -*- coding: utf-8 -*-
import pygame as pg
from gamestate import GameState

class MainMenu(GameState):
    choices_txt = ["Kuidas värve segada?", "Kuidas ekraan töötab?", "Miks paistavad asjad nii nagu nad paistavad?", "Mängu kasutusõpetus"]
    states = ["GAMEPLAY1","GAMEPLAY2","GAMEPLAY3","HELP"]
    title_txt = "KUIDAS ME MAAILMA NÄEME?"
    active_choice = 0

    def __init__(self):
        super(MainMenu, self).__init__()
        self.title = self.title_font.render(self.title_txt, True, pg.Color("white"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center).move(0, -220)
        self.next_state = self.states[self.active_choice]
        self.backgrounds = [pg.image.load("images/intro_bg_"+color+".png") for color in ["red", "green", "blue", "grey"]]

        self.choices = [self.font.render(txt, True, pg.Color("white")) for txt in self.choices_txt]


    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            self.next_state = self.states[self.active_choice]
            self.persist["state"] = self.next_state
            if event.button == 1:
                self.done = True
        elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.active_choice = (self.active_choice - 1) % 4
                if event.button == 5:
                    self.active_choice = (self.active_choice + 1) % 4

    def draw(self, surface):
        surface.blit(self.backgrounds[self.active_choice], (0, 0))
        surface.blit(self.title, self.title_rect)
        for i, choice in enumerate(self.choices):
            y_help = 100 if i == 3 else 0
            rect = pg.Rect((0, 96*i), (0, 96*i + 96)).move(200, 300 + y_help)
            surface.blit(choice, rect)
            if i == self.active_choice:
                pg.draw.circle(surface, pg.Color("red"), (120, 310+96*i + y_help), 20, 0);

