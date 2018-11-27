from states.gameplay1 import *

class Gameplay2(Gameplay1):
    choices = [
        "Kuidas ekraan töötab? (lained)",
        "Kuidas ekraan töötab? (pikslid)"
    ]
    states = ["GAMEPLAY2a", "GAMEPLAY2b"]
    title_txt = "Kuidas ekraan töötab?"

class Gameplay2a(Gameplay1aa):
    pass


class Gameplay2b(GameState):
    pass

class Gameplay2ba(GameState):
    pass