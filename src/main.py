from filtres import *
from mesures import Mesures
# from IG
import numpy as np
from datetime import datetime as dtime

def F(dt:float, n:int=6):
    F_dt = np.eye(n)
    F_dt [0:n//2, n//2:]  = dt*np.eye(n//2)
    return F_dt

def G(dt:float, n:int=3):
    return np.block([[1/2*dt**2*np.eye(n)],
                     [dt*np.eye(n)]
                    ])

def initialisation():
    H = np.block([np.eye(3), np.zeros((3, 3))])
    filtre = FiltreKalman(F(0), H, G(0)) # Rajouter R et Q
    filtre.x = data.gnss

    return filtre

if __name__ == "__main__":
    global data = Mesures()
    filtre = initialisation()

    t0 = dtime.now()
    while True:
        y = data.gnss
        while data.gnss == y:
            u, ti = data.imu
            dt = dtime.now()-ti
            filtre.F = F(dt)
            filtre.G = G(dt)
            filtre(u)
            y = data.gnss
        u, ti = data.imu
        dt = dtime.now()-ti
        filtre.F = F(dt)
        filtre.G = G(dt)
        filtre(u, y)

        filtre.x
    
    print(dt)