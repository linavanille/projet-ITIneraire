import numpy as np
import multiprocessing
import time

from filtres import *
from mesures import Mesures
# from IG
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

def get_donnees_imu (file_imu):
    rpi = Mesures()
    while True:
        file_imu.put(rpi.imu)
        time.sleep(0.1)

def get_donnees_gnss(file_gnss):
    rpi = Mesures()
    while True:
        file_gnss.put(rpi.gnss)
        time.sleep(1)

if __name__ == "__main__":
    filtre = initialisation()
    file_imu = multiprocessing.Queue()
    file_gnss = multiprocessing.Queue()

    p_imu = multiprocessing.Process(target=get_donnees_imu, args=(q_imu,))
    p_gnss = multiprocessing.Process(target=get_donnees_gnss, args=(q_gnss,))
    
    y_old = file_gnss.get()
    while True:
        try:
            if not file_imu.empty():
                u = file_imu.get()
            if not file_gnss.empty():
                y_new = file_gnss.get()
            
            if y_new == y_old:
                filtre(u)
            else:
                filtre(u, y_new)
                y_old = y_new

            #afficher(filtre.x)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    print("Exit...")
    print(dt)