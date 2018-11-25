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
        self.gpioA = [19, 27, 13] # clk
        self.gpioB =  [26, 17, 22] #data
        self.btnEnter = 6
        self.btnBack = 5

        self.levA = [0, 0, 0]
        self.levB =[0, 0, 0]

        self.lastGpio = [None, None, None]

        for pin in self.gpioA:
            self.pi.set_mode(pin, pigpio.INPUT)
        for pin in self.gpioB:
            self.pi.set_mode(pin, pigpio.INPUT)

        self.pi.set_mode(self.btnEnter, pigpio.INPUT)
        self.pi.set_mode(self.btnBack, pigpio.INPUT)

        self.pi.set_pull_up_down(self.btnEnter, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.btnBack, pigpio.PUD_UP)

        self.cbA = [self.pi.callback(pin, pigpio.EITHER_EDGE, self.pulse(i)) for i, pin in enumerate(self.gpioA)]
        self.cbB = [self.pi.callback(pin, pigpio.EITHER_EDGE, self.pulse(i)) for i, pin in enumerate(self.gpioB)]
        
        self.cbEnter = self.pi.callback(self.btnEnter, pigpio.RISING_EDGE , self.button)
        self.cbBack = self.pi.callback(self.btnBack, pigpio.RISING_EDGE , self.button)
        self.draw()

    def draw(self):
        pass
        
    def button(self, gpio, level, tick):
        if level and (tick - self.lastClick > 300000) : # 300ms
            print("select", gpio, level, tick, tick - self.lastClick)
            pg.event.post(pg.event.Event(PUSH_BUTTON, {"button": gpio}))
        self.lastClick = tick
        
        
    def pulse(self, i):
        def _pulse(gpio, level, tick):

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
                        pg.event.post(pg.event.Event(ROTARY_BUTTON, {"button": i, "direction": 1}))
                elif gpio == self.gpioB[i] and level == 1:
                    if self.levA[i] == 1:                    
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
            
        self.cbEnter.cancel()            
        self.cbBack.cancel()
       
encoder = RotaryEncoder() if pigpio else None

    
if __name__ == "__main__":

    import time
    import pigpio

    pos = [0,0,0]
    dmx = [2, 3, 4]
    dev = None

    def callback(i, way):

        global pos, dmx, dev

        pos[i] += way
        if pos[i] < 0: 
            pos[i] = 0
        if pos[i] > 16:
            pos[i] = 16
            
        n = dev.send_single_value(dmx[i], min(255, pos[i]**2))
        print (n, dmx[i], pos)

    pi = pigpio.pi()
    dev = pyudmx.uDMXDevice()

    if not dev.open():
        raise "Unable to find and open uDMX interface"
    for ch in [1, 2, 3, 4,8]:
        dev.send_single_value(ch, 255)
        
    decoder = RotaryEncoder(pi, callback)
    try:
        mainloop()
    except:
        pass

    decoder.cancel()

    pi.stop()
    for ch in dmx:
        dev.send_single_value(ch, 255)
    dev.close()

    print("done...")