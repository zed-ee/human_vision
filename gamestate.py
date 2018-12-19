# -*- coding: utf-8 -*-
import pygame as pg
import pygame.freetype  # Import the freetype module.
import os

def LOGO():pass
LOGO.WHITE = 0
LOGO.BLACK = 1

class GameState(object):
    """
    Parent class for individual game states to inherit from.
    """
    background = None
    title = None
    logo = LOGO.WHITE
    title_top = None
    help = None

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.freetype.Font("fonts/Ranchers-Regular.ttf", 26)
        self.font2 = pg.freetype.Font("fonts/Ranchers-Regular.ttf", 36)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass

    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass
