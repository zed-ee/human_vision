# -*- coding: utf-8 -*-
from gamestate import GameState
import pygame as pg
from userevents import *
from animations import load_images, load_image
from sprite import *

class Help(GameState):
    text = "Kahjuks pole meil veel juhendit"
    title = "Mängu kasutusõpetus"

    def __init__(self):
        super(Help, self).__init__()
        self.next_state = "MAINMENU"
        self.background = pg.Color("white")
        self.anim = AnimatedSprite(position=(476, 280), images=load_images("images/help/anim"))
        self.labels = Sprite(position=(247, 348), image=load_image("images/help/labels.png"))

    def startup(self, persistent):
        self.persist = persistent

    def update(self, dt):
        self.anim.update(dt)

    def get_event(self, event):
        if event.type == PUSH_BUTTON or  event.type == pg.MOUSEBUTTONUP:
            self.done = True


    def draw(self, surface):
        self.anim.draw(surface)
        self.labels.draw(surface)


