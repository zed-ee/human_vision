#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pygame as pg
from states.help import Help
from states.mainmenu import MainMenu
from states.gameplay1 import Gameplay1
import transitions

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
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)
        if next_state == "MAINMENU":
            transitions.run("fadeOutDown", 0.6)
        else:
            transitions.run("fadeOutUp", 0.6)

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
        if self.state.background is not None:
            screen.blit(self.state.background, (0, 0))
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
            if transitions.updateScreen() == False:
                self.draw()
            pg.display.update()



if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((1366, 768))
    transitions.init(screen, 1366, 768)

    states = {"MAINMENU": MainMenu(),
                   "GAMEPLAY1": Gameplay1(),
                    "GAMEPLAY2": Gameplay1(),
                    "GAMEPLAY3": Gameplay1(),
                    "HELP": Help()}
    game = Game(screen, states, "MAINMENU")
    game.run()
    pg.quit()
    sys.exit()