#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame as pg
from states.help import Help
from states.mainmenu import MainMenu
from states.gameplay1 import *
from states.gameplay2 import *
from states.gameplay3 import *
from states.calibrate import *
import transitions
import username
import rotary
from dmx import dmx
import pygame.freetype  # Import the freetype module.
import animations
RASPBERRY = username() == "pi"

def to_center(rect, top, shift=0):
    return rect.move((screen.get_width() - rect.width)//2 + shift, top)

class Game(object):
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """

    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state
        """
        
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.load_state()

        

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                break
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        self.load_state()

    def load_state(self):
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)


    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


class VisionGame(Game):
    layer = None
    def __init__(self, screen, states, start_state):
        self.title_font = pg.freetype.Font("fonts/Ranchers-Regular.ttf", 66)
        self.logos = [pg.image.load("images/logo_white.png").convert(), pg.image.load("images/logo_black.png").convert()]
        self.title_colors = [pg.Color(220, 98, 30), pg.Color("white")]

        super(VisionGame, self).__init__(screen, states, start_state)
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/avakuva_v03_paigutamise_võrgustik.jpg")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_slaid_02_skeem_v05_paigutamise_võrgustikuga.jpg")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_slaid_03_v04_paigutamise_võrgustikuga.jpg")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_slaid_04_v03_paigutamise_võrgustikuga.jpg")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_slaid_05_v03_paigutamise_võrgustikuga.jpg")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_õige_paigutamise_võrgustikuga.png")
        #self.layer = pg.image.load("../human__vision_elemendid/Kujundus/HT_slaid_11_v02_paigutamise_võrgustik.jpg")



    def load_state(self):
        super(VisionGame, self).load_state()
        dmx.reset()
        if self.state.title is not None:
            self.title = self.title_font.render(self.state.title,  self.title_colors[self.state.logo] )

    def draw(self):
        """Pass display surface to active state for drawing."""
        if self.state.background is not None:
            if isinstance(self.state.background, pg.Surface):
                screen.blit(self.state.background, (0, 0))
            else:
                screen.fill(self.state.background)

        if self.layer is not None:
            screen.blit(self.layer, (-13, -13))

        if self.state.title is not None:
            screen.blit(self.title[0], to_center(self.title[1], self.state.title_top or 50, 0))

        if self.state.logo is not None:
            screen.blit(self.logos[self.state.logo], (0, 0))


        self.state.draw(self.screen)


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1360, 768), pg.FULLSCREEN if RASPBERRY else 0)
    #transitions.init(screen, 1360, 768)

    states = {
        "MAINMENU": MainMenu(),
        "RESULT": Result(),
        "GAMEPLAY1": Gameplay1(),
        
        "GAMEPLAY1a": Gameplay1a(),
        "GAMEPLAY1aa": Gameplay1aa(),
#        "GAMEPLAY1ab": Gameplay1ab(),
        
        "GAMEPLAY1b": Gameplay1b(),
        "GAMEPLAY1ba": Gameplay1ba(),
        
        "GAMEPLAY2": Gameplay2(),
        "GAMEPLAY2a": Gameplay2a(),
        "GAMEPLAY2ab": Gameplay2ab(),
        "GAMEPLAY2b": Gameplay2b(),
        "GAMEPLAY2ba": Gameplay2ba(),

        "GAMEPLAY3": Gameplay3(),
        "GAMEPLAY3a": Gameplay3a(),

        "CALIBRATE": Calibrate(),
        "CALIBRATE_CENTER": CalibrateCenter(),
        "CALIBRATE_OFFSET": CalibrateOffset(),
        "CALIBRATE_SIDEBYSIDE": CalibrateSideBySide(),
        "CALIBRATE_LOW": CalibrateLow(),
        "CALIBRATE_HIGH": CalibrateHigh(),
                    
         "HELP": Help()}

    game = VisionGame(screen, states, "MAINMENU" if len(sys.argv) == 1 else sys.argv[1])
    game.run()
    pg.quit()
    sys.exit()