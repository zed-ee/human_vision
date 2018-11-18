# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg

class Gameplay1(GameState):
    def __init__(self):
        super(Gameplay1, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.next_state = "MAINMENU"

    def startup(self, persistent):
        self.persist = persistent
        color = "dodgerblue"
        self.screen_color = pg.Color(color)
        text = self.persist["state"]

        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                self.done = True
            else:
                self.title_rect.center = event.pos

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