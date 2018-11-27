from states.gameplay1 import *
from states.mainmenu import *

class Gameplay3(Gameplay1a):

    states = ["GAMEPLAY3a" for i in range(0, 9)]

    title_txt = "Miks paistavad asjad nii nagu nad paistavad?"
    text = ["Siin saad teada, miks porgand on oranž või lumi on valge. Avasta ja uuri! ",
            "Kinnita oma valikut …. nupuga"]

    choices = [find_color(color, ALL_COLORS) for color in ["Valge", "Kollane", "Punane", "Must", "Oranž", "Taevasinine", "Valge", "Ametüst", "Roheline"]]
    titles = ["Valgus","Banaan","Arbuus","Pimedus","Porgand","Vesi","Lumi","Peet","Muru"]

    def startup(self, persistent):
        for c in self.choices:
            print(c)
        self.rt = config.load("positions", "center", [[0,0],[0,0], [0,0]])
        self.persist = persistent
        dmx.send_rt(*self.rt)
        self.persist["result"] = True
        self.persist["next_state"] = "GAMEPLAY3"

class Gameplay3a(Result):
    pass
