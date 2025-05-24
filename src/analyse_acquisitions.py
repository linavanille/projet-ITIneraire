#!/usr/bin/env python 3
"""Module pour générer tous les CSV et les HTML des acquisitions"""

import numpy as np

from filtres import FiltreKalman, filtrage_csv
from GPS.plot_gnss import *

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

def generation_fichiers(outputfile:str, dt:float, Q:np.array=None, R:np.array=None)->None:
    """fonction de génération des fichiers"""

    root_source = "./output/"

    if not outputfile.endswith("/"):
        outputfile+="/"
    root_destination = "./output/"+outputfile

    nos_acquisitions = {
        "parking" : (root_source+'gnss_acq', root_destination+'parking'),
        # "leclerc_RPI" : (root_source+'leclerc/GPS_leclerc_RPI', root_destination+'leclerc_RPI'),
        # "leclerc_Tho" : (root_source+'leclerc/GPS_leclerc_Thomas', root_destination+'leclerc_Tho'),
        # "leclerc_Chl" : (root_source+'leclerc/GPS_leclerc_Chloe', root_destination+'leclerc_Chl'),
        # "parasol_RPI" : (root_source+'parasol/GPS_parasol_RPI', root_destination+'parasol_RPI'),
        # "parasol_Tho" : (root_source+'parasol/GPS_parasol_Thomas', root_destination+'parasol_Tho'),
        # "parasol_Chl" : (root_source+'parasol/GPS_parasol_Chloe', root_destination+'parasol_Chl'),
    }

    root_groupes = "./pi-itineraire-data/2024_2025/GR"
    acquisitions_des_groupes = {}

    # initialisation du filtre
    F_t = F(dt)
    G_t = F(dt)
    H = np.block([np.eye(3), np.zeros((3, 3))])
    filtre = FiltreKalman(F_t, H, G_t, Q, R)

    # generation des fichiers
    for k, v in nos_acquisitions:
        print(f'filtrage de {k}')
        filtrage_csv(v[0], v[1], filtre)
        print(f'generation du fichier html de {k}')
        plot_GNSS(v[1])
        print("\n")

if __name__ == "main":
    print("lancement")
    generation_fichiers("testfonction", 1)
