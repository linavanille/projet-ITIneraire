import multiprocessing
import time
import numpy as np
from GPS.Button import Button
from GPS import get_position
from IMU import get_imu_data
import front
from filtres import *
from mesures import Mesures
# from IG
from datetime import datetime as dtime

def F(dt:float, n:int=6):
    """Definition dynamique de la matrice F"""
    F_dt = np.eye(n)
    F_dt [0:n//2, n//2:]  = dt*np.eye(n//2)
    return F_dt

def G(dt:float, n:int=3):
    """Definition dynamique de la matrice G"""
    return np.block([[1/2*dt**2*np.eye(n)],
                     [dt*np.eye(n)]
                    ])

def initialisation_Kalman():
    """Initialisation du filtre de Kalman"""
    H = np.block([np.eye(3), np.zeros((3, 3))])
    filtre = FiltreKalman(F(0), H, G(0)) # Rajouter R et Q
    filtre.x = Mesures().gnss

    return filtre

def get_donnees_imu (file_imu:Queue, arret:Queue):
    """Processus de récupération des données de l'IMU"""
    rpi = Mesures()
    while arret.empty():
        file_imu.put(rpi.imu)
        file_imu.put(i)
        time.sleep(0.1)

def get_donnees_gnss(file_gnss:Queue, arret:Queue):
    """Processus de récupération des données GPS"""
    rpi = Mesures()
    while arret.empty():
        file_gnss.put(rpi.gnss)
        time.sleep(1)

def acquisition_directe(filtre:FiltreKalman)->None:
    """Fonction d'acquisition en directe des données de la RPi"""
    #initialisation multiprocess
    file_imu = multiprocessing.Queue()
    file_gnss = multiprocessing.Queue()
    file_arret = multiprocessing.Queue()
    
    #initialisation des differents processus qui tourneront en parallèle
    p_imu = multiprocessing.Process(target=get_donnees_imu, args=(file_imu,file_arret,))
    p_gnss = multiprocessing.Process(target=get_imu_data, args=(file_gnss,file_arret,))
    
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

def bouton_preacquisition(com_bouton):
    b = Bouton(17)
    def press():
        com_bouton.put("debut")
    return b

def acquisition_csv(filtre:FiltreKalman)->None:
    """Fonction d'écriture des acquisitions RPi dans des csv"""

    path_donnees_gps = "output/GPS/acquisition"
    path_donnees_imu = "output/IMU/acquisition"

    #initialisation des differents processus qui tourneront en parallèle
    p_imu = multiprocessing.Process(target=get_position, args=(path_donnees_gps,))
    p_gnss = multiprocessing.Process(target=get_donnees_gnss, args=(path_donnees_gps,))
    print("Acquisitions en cours...")

    #initialisation bouton
    b = Button(17)
    def press():
        file_arret.put("fin")
    b.on_press(press)
    
    #attente de la fin des acquisitions
    p_imu.join()
    p_gnss.join()
    print("Acquisitions finies !\n")

    #Recuperation des donnees IMU et GPS
    print("Traitement en cours...")
    j = 0
    y = donnees_gps[0]
    for i in range(len(donnees_imu)):
        u = donnees_imu[i]
        if y[0] >= u[0]:
            filtre(u[1:], y[:1])
            j += 1
            y = donnees_gps[j]
        else:
            filtre(u[:1])
    print("Fin du traitement\n")

if __name__ == "__main__":
    app = Front()

    choix = ''	
    while choix != "Q" :
    
        app.menu()
                    
        choix = input("Menu : ").upper()
    
        if choix == "1" :
            app.historique
        elif choix == "2" :
            entree = ''
            com_bouton = multiprocessing.Queue()
            b = bouton_preacquisition(com_bouton)
            while entree != R :
                app.avant_acquisition
                                


        elif choix == "C" :
            app.credit
        elif self.help == "H" : 
            app.help
