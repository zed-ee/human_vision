import numpy as np 
from scipy.interpolate import interp1d
from dmx import dmx
import time

def interpolate(r, g, b):
    from config import config
    low = config.load("positions", "low", [[0,0], [0,0], [0,0]])
    center = config.load("positions", "center", [[0,0], [0,0], [0,0]])
    high = config.load("positions", "high", [[0,0], [0,0], [0,0]])

    xr = [0, r, 255] # low, center, high
    xg = [0, g, 255] # low, center, high
    xb = [0, b, 255] # low, center, high
    p = [ low, center, high ]
    print(p)
    rr = [p[0][0][0], p[1][0][0], p[2][0][0]]
    rt = [p[0][0][1], p[1][0][1], p[2][0][1]]
    gr = [p[0][1][0], p[1][1][0], p[2][1][0]]
    gt = [p[0][1][1], p[1][1][1], p[2][1][1]]
    br = [p[0][2][0], p[1][2][0], p[2][2][0]]
    bt = [p[0][2][1], p[1][2][1], p[2][2][1]]

    x_new =  np.linspace(0, 255, 256)

    frr = interp1d(xr, rr, kind='linear')
    frt = interp1d(xr, rt, kind='linear')
    fgr = interp1d(xg, gr, kind='linear')
    fgt = interp1d(xg, gt, kind='linear')
    fbr = interp1d(xb, br, kind='linear')
    fbt = interp1d(xb, bt, kind='linear')

    yr = [[int(round(r)),int(round(t))] for r,t in np.stack((frr(x_new), frt(x_new)), axis=-1)]
    yg = [[int(round(r)),int(round(t))] for r,t in np.stack((fgr(x_new), fgt(x_new)), axis=-1)]
    yb = [[int(round(r)),int(round(t))] for r,t in np.stack((fbr(x_new), fbt(x_new)), axis=-1)]

    return [[yr[i], yg[i], yb[i]] for i in range(0,256)]
    
if __name__ == "__main__":
    dmx.send_rgb(255,255,255)
    from colors import COLORS
    c = COLORS[32][1]
    print(COLORS[32])
    ip = interpolate(c.r, c.g, c.b)
    print(ip[c.r][0], ip[c.g][1], ip[c.b][2])
    dmx.send_rt(ip[0][0], ip[0][1], ip[0][2])
    time.sleep( 1 )
    dmx.send_rt(ip[c.r][0], ip[c.g][1], ip[c.b][2])
    time.sleep( 1 )
    dmx.send_rt(ip[255][0], ip[255][1], ip[255][2])
    time.sleep( 1 )
    
    for i in range(0,255):
        dmx.send_rt(*ip[i])
        time.sleep( 0.03 )
        
