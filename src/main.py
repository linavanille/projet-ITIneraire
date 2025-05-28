from multiprocessing import Queue, Process
import time
import numpy as np
import pandas as pd
from datetime import datetime as dtime
from GPS.utils import CSVHandler

# import front
from filtres import *
from GPS.Button import Button
from mesures import Mesures

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
    record.create_csv_with_header(['TimeStamp',
                                   'Longitude',
                                   'Latitude',
                                   'Altitude',])

    df = pd.DataFrame(columns=['TimeStamp',
                               'Longitude',
                               'Latitude',
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
    y_new = 0
    y = np.zeros(3)
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

    b = Button(17)
    def press():
        file_arret.put("fin")
    time.sleep(1)
    b.on_press(press)
    #initialisation bouton

    j = 0
    #main
    while file_arret.empty():
        j+=1
        try:
            if not file_imu.empty():
                u = file_imu.get()
            if not file_gnss.empty():
                y_new = file_gnss.get()

            if y_old == y_new:
                filtre(u)
            else:
                filtre(u, y_new)
                y_old = y_new
                j = 0

            X = Mesures.to_spherique(*filtre.x)
            output.append_row([rpi.get_utc(), X[0], X[1], X[2]])
            result.loc[len(result)] = ({'TimeStamp': rpi.getutc(),
                                        'Latitude' : X[0],
                                        'Longitude' : X[1],
                                        'Altitude' : X[2],
                                        })
            time.sleep(0.1)
        except KeyboardInterrupt:
            b.cleanup()
            break

    print("Acquisitions finies !\n")
    return result

def bouton_preacquisition(com_bouton):
    b = Bouton(17)
    def press():
        com_bouton.put("debut")
    return b

if __name__ == "__main__":
    # app = Front()

    # choix = ''
    # while choix != "Q" :

    #     app.menu()

    #     choix = input("Menu : ").upper()

    #     if choix == "1" :
    #         app.historique
    #     elif choix == "2" :
    #         entree = ''
    #         com_bouton = multiprocessing.Queue()
    #         b = bouton_preacquisition(com_bouton)
    #         while entree != R :
    #             app.avant_acquisition



    #     elif choix == "C" :
    #         app.credit
    #     elif self.help == "H" :
    #         app.help
    csv_out = ""
    html_out = ""
    gpx_out = ""
    filtre = initialisation_Kalman(0.1)
    df = acquisition(filtre, csv_out)
    plot_gnss(csv_out, html_out)
    # csv_to_gpx.main(csv_out, gpx_out)
    print(df.describe())
