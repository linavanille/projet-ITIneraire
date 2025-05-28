from multiprocessing import Queue, Process
import time
import numpy as np
import pandas as pd
from datetime import datetime as dtime
from GPS.utils import CSVHandler

# from performances import front
from performances.valeurs_aberrantes import nettoyer_csv_gps

from filtres import *
from GPS.Button import Button

RED = "\033[31m"
RESET = "\033[0m"

def F(dt:float, n:int=6):
    """Definition dynamique de la matrice F"""
    F_dt = np.eye(n)
    F_dt [0:n//2, n//2:]  = dt*np.eye(n//2)
    return F_dt

def G(dt:float, n:int=3):
    """Definition dynamique de la matrice G"""
    g = np.block([[1/2*dt**2*np.eye(n)],
                     [dt*np.eye(n)]
                    ])
    return g

def initialisation_Kalman(dt:float)->FiltreKalman:
    """Initialisation du filtre de Kalman"""
    H = np.block([np.eye(3), np.zeros((3, 3))])
    # R = None
    # Q = None
    filtre = FiltreKalman(F(dt), H, G(dt)) # Rajouter R et Q
    filtre.x = np.zeros(6)

    return filtre

def initialisation_resultats(csv_out)->pd.DataFrame:
    record = CSVHandler(csv_out)
    record.create_csv_with_header(['UTC',
                                   'Latitude',
                                   'Longitude',
                                   'Altitude',])

    df = pd.DataFrame(columns=['UTC',
                               'Latitude',
                               'Longitude',
                               'Altitude'])
    return record, df

def get_donnees_imu(rpi:Mesures, file_imu:Queue, arret:Queue)->None:
    """Processus de récupération des données de l'IMU"""
    # rpi = Mesures()
    while arret.empty():
        file_imu.put(rpi.imu)
        time.sleep(0.1)

def get_donnees_gnss(rpi:Mesures, file_gnss:Queue, arret:Queue)->None:
    """Processus de récupération des données GPS"""
    # rpi = Mesures()
    while arret.empty():
        file_gnss.put(rpi.gnss)
        time.sleep(1)

def acquisition(filtre:FiltreKalman, csv_out:str)->pd.DataFrame:
    """Fonction d'acquisition en directe des données de la RPi"""

    output, result = initialisation_resultats(csv_out)

    #initialisation des mesures
    rpi = Mesures()
    y_old = np.zeros(3)
    y_new = np.zeros(3)
    # y = np.zeros(3)
    u = 0
    filtre.x = np.block([rpi.origine, np.zeros(3)])

    #initialisation multiprocess
    file_imu = Queue()
    file_gnss = Queue()
    file_arret = Queue()

    #initialisation des differents processus qui tourneront en parallèle
    p_imu = Process(target=get_donnees_imu, args=(rpi, file_imu,file_arret,))
    p_gnss = Process(target=get_donnees_gnss, args=(rpi,file_gnss,file_arret,))

    p_imu.start()
    p_gnss.start()
    print("Acquisitions en cours...")
    print(f"Pressez le {RED}bouton{RESET} pour stopper la machine")

    #initialisation bouton
    b = Button(17)
    def press():
        file_arret.put("fin")
    time.sleep(1)
    b.on_press(press)

    #main
    while file_arret.empty():
        try:
            if not file_imu.empty():
                u = file_imu.get()
            if not file_gnss.empty():
                y_new = file_gnss.get()


            if all(y_old == y_new):
                filtre(u)
            else:
                filtre(u, y_new)
                y_old = y_new


            X = Mesures.to_spherique(*filtre.x[:3])

            output.append_row([rpi.get_utc(), X[0], X[1], X[2]])
            result.loc[len(result)] = ({'TimeStamp': rpi.get_utc(),
                                        'Latitude' : X[0],
                                        'Longitude' : X[1],
                                        'Altitude' : X[2],
                                        })
            time.sleep(0.1)
        except KeyboardInterrupt:
            b.cleanup()
            break

    p_imu.join()
    p_gnss.join()
    print("Acquisitions finies !\n")
    return result

def get_data(csv_destination:str)->None:
    """Main fonction d'acquisition des données"""
    filtre = initialisation_Kalman(0.1)
    df = acquisition(filtre, csv_destination)
    nettoyer_csv_gps(csv_destination)

if __name__ == "__main__":

    csv_out = "./output/Soutenance/acquisition.csv"
    get_data(csv_out)

    # html_out = "./output/HTML/Soutenance/carte.html"
    # gpx_out = "./output/GPX/Soutenance/carte.gpx"
    # filtre = initialisation_Kalman(0.1)
    # df = acquisition(filtre, csv_out)
    # nettoyer_csv_gps(csv_out)

    # print("En Attente...")
    # while True:
    #     time.sleep(1)