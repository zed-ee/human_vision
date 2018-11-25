try:
    from pyudmx import pyudmx
except Exception as e:
    pyudmx = None
    print(e)

CHANNEL_ROTATION = 1
CHANNEL_TILT = 2
CHANNEL_MASTER = 5

COLOR_WHITE = 0
COLOR_RED = 11
COLOR_GREEN = 44
COLOR_BLUE = 55

COLOR_WHEEL = [COLOR_RED, COLOR_GREEN, COLOR_BLUE]

class uDMX(object):
    channels = [0, 10, 20]
    


    def __init__(self):
        self.dmx = pyudmx.uDMXDevice()
        self.dmx.open()

    def __del__(self):
        self.dmx.close()
        
    def reset(self):
        self.set_mode(COLOR_RED, COLOR_GREEN, COLOR_BLUE)
        
    def set_mode(self, r, g, b):
        self.dmx.send_single_value(self.channels[0]+4, r)
        self.dmx.send_single_value(self.channels[1]+4, g)
        self.dmx.send_single_value(self.channels[2]+4, b)
        
    def send_rgb(self, r, g, b):        
        self.dmx.send_single_value(self.channels[0]+5, r)
        self.dmx.send_single_value(self.channels[1]+5, g)
        self.dmx.send_single_value(self.channels[2]+5, b)

    def send_rt(self, r, g, b):
        #print("send_rt", r, b, g)

        self.dmx.send_single_value(self.channels[0]+1, r[0])
        self.dmx.send_single_value(self.channels[1]+1, g[0])
        self.dmx.send_single_value(self.channels[2]+1, b[0])

        self.dmx.send_single_value(self.channels[0]+2, r[1])
        self.dmx.send_single_value(self.channels[1]+2, g[1])
        self.dmx.send_single_value(self.channels[2]+2, b[1])


class uDMXDummy(object):
    def send_rgb(self, r, g, b):
        pass

    def send_rt(self, r, g, b):
        pass


dmx = uDMX() if pyudmx else uDMXDummy()

if __name__ == "__main__":
    dmx.send_rgb(255,155,255)
