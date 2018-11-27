import pygame as pg

# color name, (R, G, B, A), H, S, L, wavelength
COLORS = [
    ("Alisariinpunane", pg.Color(227, 38, 54, 255), 355, 83, 89, 452),
    ("Ametüst", pg.Color(153, 102, 204, 255), 270, 50, 80, 492),
    ("Aprikoos", pg.Color(251, 206, 117, 255), 30, 25, 87, 606),
    #("Beebisinine", pg.Color(111, 255, 255, 255), 180, 12, 100, 535),
    #("Beež", pg.Color(245, 245, 220, 255), 60, 10, 96, 592),
    #("Berliini sinine", pg.Color(0, 49, 83, 255), 205, 100, 33, 523),
    #("Heleroheline", pg.Color(102, 255, 0, 255), 96, 100, 100, 575),
    #("Hele türkiis", pg.Color(8, 232, 222, 255), 177, 97, 91, 536),
    #("Kahvatu rukkilillesinine", pg.Color(171, 205, 239, 255), 210, 28, 94, 521),
    #("Kahvatu roosa", pg.Color(250, 218, 221, 255), 354, 13, 98, 453),
    ("Kastanpruun", pg.Color(113, 47, 44, 255), 7, 66, 44, 617),
    #("Kinaverpunane", pg.Color(255, 77, 0, 255), 18, 100, 100, 612),
    #("Kollane", pg.Color(255, 255, 0, 255), 60, 100, 100, 592),
    #("Meresinine", pg.Color(0, 0, 128, 255), 240, 100, 50, 507),
    #("Merevaik", pg.Color(255, 191, 0, 255), 45, 100, 100, 599),
    ("Messing", pg.Color(181, 166, 66, 255), 52, 47, 48, 603),
    #("Punane", pg.Color(255, 0, 0, 255), 0, 100, 100, 620),
    #("Pruun", pg.Color(150, 75, 0, 255), 30, 100, 59, 606),
    #("Rohekassinine", pg.Color(0, 255, 255, 255), 180, 100, 100, 535),
    #("Roheline", pg.Color(0, 128, 0, 255), 120, 100, 25, 563),
    #("Sinine", pg.Color(0, 0, 255, 255), 240, 100, 100, 507),
    ("Särav roosa", pg.Color(255, 85, 163, 255), 330, 75, 84, 464),
    #("Taevasinine", pg.Color(0, 127, 255, 255), 210, 100, 100, 521),
    #("Tsinvaldiit", pg.Color(235, 194, 175, 255), 19, 25, 92, 611),
    #("Tsüaan", pg.Color(0, 255, 255, 255), 180, 100, 100, 535),
    #("Tulipunane", pg.Color(255, 36, 0, 255), 8, 100, 100, 616),
    ("Ultramariin", pg.Color(18, 10, 143, 255), 244, 93, 56, 505),
    ("Terrakota", pg.Color(226, 114, 91, 255), 10, 70, 62, 615),
    ("Türkiis", pg.Color(48, 213, 200, 255), 175, 77, 84, 537),
    #("Tüürose purpur", pg.Color(102, 2, 60, 255), 277, 67, 44, 489),
    #("Sinakasroheline", pg.Color(0, 128, 128, 255), 180, 100, 50, 535),
    #("Pruunikashall", pg.Color(72, 60, 50, 255), 30, 17, 34, 606),
    #("Oranž", pg.Color(255, 128, 0, 255), 30, 100, 100, 606),
    #("Safran", pg.Color(244, 196, 48, 255), 45, 80, 96, 599),
    #("Kahvatusinine", pg.Color(175, 238, 238, 255), 180, 26, 93, 535),
    ("Pärsia sinine", pg.Color(28, 57, 187, 255), 248, 75, 50, 503),
    #("Oliiviroheline", pg.Color(128, 128, 0, 255), 60, 100, 50, 592),
    ("Sinepikollane", pg.Color(255, 219, 88, 255), 47, 65, 100, 598)
]

RGB = [
    ("Punane", pg.Color(255, 0, 0, 255), 0, 100, 100, 660),
    ("Roheline", pg.Color(0, 128, 0, 255), 120, 100, 25, 550),
    ("Sinine", pg.Color(0, 0, 255, 255), 240, 100, 100, 480),

]

OTHER_COLORS = [
    ("Beebisinine", pg.Color(111, 255, 255, 255), 180, 12, 100, 535),
    ("Beež", pg.Color(245, 245, 220, 255), 60, 10, 96, 592),
    ("Berliini sinine", pg.Color(0, 49, 83, 255), 205, 100, 33, 523),
    ("Heleroheline", pg.Color(102, 255, 0, 255), 96, 100, 100, 575),
    ("Hele türkiis", pg.Color(8, 232, 222, 255), 177, 97, 91, 536),
    ("Kahvatu rukkilillesinine", pg.Color(171, 205, 239, 255), 210, 28, 94, 521),
    ("Kahvatu roosa", pg.Color(250, 218, 221, 255), 354, 13, 98, 453),
    ("Kinaverpunane", pg.Color(255, 77, 0, 255), 18, 100, 100, 612),
    ("Kollane", pg.Color(255, 255, 0, 255), 60, 100, 100, 592),
    ("Meresinine", pg.Color(0, 0, 128, 255), 240, 100, 50, 507),
    ("Merevaik", pg.Color(255, 191, 0, 255), 45, 100, 100, 599),
    ("Punane", pg.Color(255, 0, 0, 255), 0, 100, 100, 620),
    ("Pruun", pg.Color(150, 75, 0, 255), 30, 100, 59, 606),
    ("Rohekassinine", pg.Color(0, 255, 255, 255), 180, 100, 100, 535),
    ("Roheline", pg.Color(0, 128, 0, 255), 120, 100, 25, 563),
    ("Sinine", pg.Color(0, 0, 255, 255), 240, 100, 100, 507),
    ("Taevasinine", pg.Color(0, 127, 255, 255), 210, 100, 100, 521),
    ("Tsinvaldiit", pg.Color(235, 194, 175, 255), 19, 25, 92, 611),
    ("Tsüaan", pg.Color(0, 255, 255, 255), 180, 100, 100, 535),
    ("Tulipunane", pg.Color(255, 36, 0, 255), 8, 100, 100, 616),
    ("Tüürose purpur", pg.Color(102, 2, 60, 255), 277, 67, 44, 489),
    ("Sinakasroheline", pg.Color(0, 128, 128, 255), 180, 100, 50, 535),
    ("Pruunikashall", pg.Color(72, 60, 50, 255), 30, 17, 34, 606),
    ("Oranž", pg.Color(255, 128, 0, 255), 30, 100, 100, 606),
    ("Safran", pg.Color(244, 196, 48, 255), 45, 80, 96, 599),
    ("Kahvatusinine", pg.Color(175, 238, 238, 255), 180, 26, 93, 535),
    ("Oliiviroheline", pg.Color(128, 128, 0, 255), 60, 100, 50, 592),
]

ALL_COLORS = COLORS + OTHER_COLORS + RGB + [
("Valge", pg.Color(255, 255, 255, 255), 0, 0, 0, 0),
("Must", pg.Color(0, 0, 0, 0), 0, 0, 0, 0),
]


def find_color(name, list):
    for i in range(len(list)):
        if list[i][0] == name:
            return list[i]
    return None


def get_wavelength(color):
    return  650 - 170 / 360 * color[2];

if __name__ == "__main__":
    for c in COLORS:
        w = round(get_wavelength(c))
        print("(\""+ str(c[0])+"\", "+str(c[1].r)+", "+str(c[1].g)+", "+str(c[1].b)+", "+str(c[2])+", "+str(c[3])+", "+str(c[4])+", "+str(w)+"),")