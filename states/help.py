# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg

class Help(GameState):
    def __init__(self):
        super(Help, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.next_state = "MAINMENU"

    def startup(self, persistent):
        self.persist = persistent
        self.screen_color = pg.Color("dodgerblue")
        text = "Kahjuks pole meil veel juhendit"

        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        self.done = True

    def update(self, dt):
        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
                or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.title, self.title_rect)
        pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)