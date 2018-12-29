#!/usr/bin/env python3

try:
    import pigpio
except Exception as e:
    pigpio = None
    print(e)

import pygame as pg
from userevents import *


class RotaryEncoder:

    RGB_MIN = 0
    RGB_MAX = 255

    """Class to decode mechanical rotary encoder pulses."""

    def __init__(self):
        self.pi = pigpio.pi()
        self.lastClick = 0
        self.gpioA = [20, 6, 27] # clk
        self.gpioB =  [19, 26, 17] #data
        self.buttons = {13: BUTTONS.ENTER, 21: BUTTONS.BACK, 4: BUTTONS.CALIBRATE }

        self.levA = [0, 0, 0]
        self.levB = [0, 0, 0]

        self.lastGpio = [None, None, None]

        for pin in self.gpioA:
            self.pi.set_mode(pin, pigpio.INPUT)
        for pin in self.gpioB:
            self.pi.set_mode(pin, pigpio.INPUT)

        for pin in self.buttons.keys():
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.set_pull_up_down(pin, pigpio.PUD_UP)
            

        self.cbA = [self.pi.callback(pin, pigpio.EITHER_EDGE, self.pulse(i)) for i, pin in enumerate(self.gpioA)]
        self.cbB = [self.pi.callback(pin, pigpio.EITHER_EDGE, self.pulse(i)) for i, pin in enumerate(self.gpioB)]
        
        
        self.cbButton = [self.pi.callback(pin, pigpio.EITHER_EDGE, self.button) for event, pin in enumerate(self.buttons.keys())]
        
        self.draw()

    def draw(self):
        pass
        
    def button(self, gpio, level, tick):
        if (level == 0 and tick - self.lastClick > 300000): # 300ms
            print("select", gpio, level, tick, tick - self.lastClick)
            pg.event.post(pg.event.Event(PUSH_BUTTON, {"button": self.buttons[gpio]}))
        self.lastClick = tick
        
        
    def pulse(self, i):
        def _pulse(gpio, level, tick):
            # print("pulse",gpio, level, tick)
            """
            Decode the rotary encoder pulse.

                      +---------+         +---------+      0
                      |         |         |         |
            A         |         |         |         |
                      |         |         |         |
            +---------+         +---------+         +----- 1

                +---------+         +---------+            0
                |         |         |         |
            B   |         |         |         |
                |         |         |         |
            ----+         +---------+         +---------+  1
            """

            if gpio == self.gpioA[i]:
                self.levA[i] = level
            else:
                self.levB[i] = level;

            if gpio != self.lastGpio[i]: # debounce
                self.lastGpio[i] = gpio

                if gpio == self.gpioA[i] and level == 1:
                    if self.levB[i] == 1:
                        print("rotary", i, 1)
                        pg.event.post(pg.event.Event(ROTARY_BUTTON, {"button": i, "direction": 1}))
                elif gpio == self.gpioB[i] and level == 1:
                    if self.levA[i] == 1:   
                        print("rotary", i, -1)                    
                        pg.event.post(pg.event.Event(ROTARY_BUTTON, {"button": i, "direction": -1}))

        return _pulse

    def cancel(self):
        """
        Cancel the rotary encoder decoder.
        """
        for cb in self.cbA:
            cb.cancel()
        for cb in self.cbB:
            cb.cancel()
        for cb in self.cbButton:
            cb.cancel()            
            
       
encoder = RotaryEncoder() if pigpio else None

    
if __name__ == "__main__":

    import time
    import pigpio
    from pyudmx import pyudmx

    pg.init()

    pos = [0,0,0]
    dmx = [2, 3, 4]
    dev = None

    pi = pigpio.pi()
    dev = pyudmx.uDMXDevice()

    if not dev.open():
        raise "Unable to find and open uDMX interface"
    for ch in [1, 2, 3, 4,8]:
        dev.send_single_value(ch, 255)
        
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                break
            print(event)
            
    encoder.cancel()

    pi.stop()
    for ch in dmx:
        dev.send_single_value(ch, 255)
    dev.close()

    print("done...")