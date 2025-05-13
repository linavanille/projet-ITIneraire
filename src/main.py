import multiprocessing
import time
import numpy as np
from GPS.Button import Button

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
    filtre.x = Mesures().gnss

    return filtre

def get_donnees_imu (file_imu,arret):
    rpi = Mesures()
    i = 1
    while arret.empty():
        i += 1
        #file_imu.put(rpi.imu)
        file_imu.put(i)
        time.sleep(0.1)

def get_donnees_gnss(file_gnss,arret):
    rpi = Mesures()
    i = 1
    while arret.empty():
        i += 1
        #file_gnss.put(rpi.gnss)
        file_gnss.put(i)
        time.sleep(1)
        


if __name__ == "__main__":
    filtre = initialisation()
    
    #initialisation multiprocess
    file_imu = multiprocessing.Queue()
    file_gnss = multiprocessing.Queue()
    file_arret = multiprocessing.Queue()
    
    p_imu = multiprocessing.Process(target=get_donnees_imu, args=(file_imu,file_arret,))
    p_gnss = multiprocessing.Process(target=get_donnees_gnss, args=(file_gnss,file_arret,))
    
    p_imu.start()
    p_gnss.start()
    
    #initialisation du l'IMU et GNSS
    #y_old = file_gnss.get()
    y_old = 0
    y_new = 0
    u = 0
    #y_new = y_old
    
    #initialisation bouton
    b = Button(17)
    def press():
        file_arret.put("fin")
    b.on_press(press)
    
    #main
    while file_arret.empty():

        try:            
            if not file_imu.empty():
                u = file_imu.get()
            if not file_gnss.empty():
                y_new = file_gnss.get()
            
            if y_new == y_old:
                #filtre(u)
                print(u)
            else:
                #filtre(u, y_new)
                print(u, y_new)
                y_old = y_new
                

            #afficher(filtre.x)
            time.sleep(0.1)
        except KeyboardInterrupt:
            b.cleanup()
            break

    print("Exit...")
