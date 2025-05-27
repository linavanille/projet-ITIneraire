#!/usr/bin/env python 3
"""Module pour générer tous les CSV et les HTML des acquisitions"""

import numpy as np
import argparse
from typing import Callable


from filtres import FiltreKalman, filtrage_csv, filtrage_cartesien
from GPS.plot_gnss import *

RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"

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

def get_acquisitions(type:str):
    """selection du dictionnaire d'acquisition"""

    root_source = "./output/"

    if type == "filtre":
        root_destination = "./output/CSV_Filtre/"
    elif type == "filtre_preciction":
        root_destination = "./output/TestFiltrePrediction"
    elif type == "raw":
        root_destination = ""

    return {root_source+'gnss_acq': root_destination+'parking',
            root_source+'leclerc/GPS_leclerc_RPI': root_destination+'leclerc_RPI',
            root_source+'leclerc/GPS_leclerc_Thomas': root_destination+'leclerc_Tho',
            root_source+'leclerc/GPS_leclerc_Chloe': root_destination+'leclerc_Chl',
            root_source+'parasol/GPS_parasol_RPI': root_destination+'parasol_RPI',
            root_source+'parasol/GPS_parasol_Thomas': root_destination+'parasol_Tho',
            root_source+'parasol/GPS_parasol_Chloe': root_destination+'parasol_Chl',
        }

def generation_fichiers(type_data_input:str,
                                    filtrage:Callable[str,str]=filtrage_csv,
                                    Q:np.array=None,
                                    R:np.array=None)->None:
    """fonction de génération des fichiers

        type_data_input: str
            Permet de choisir si on souhaite générer les fichiers bruts ou bien les fichiers filtres.
            Permet egalement de préciser la methode de filtrage.
            Choix possible : 'filtre', 'filtre_prediction' 'raw'

        filtrage: Callable(csv_source:str, csv_destination:str)
            Fonction de filtrage, différent selon les types de données en entrées.
            Default : filtrage classique de spherique en spherique sans prediction

        Q: Matrice de covariance de l'IMU
            default None pour les premiers tests

        R: Matrice de covariance du GNSS
            default None pour les premiers tests
    """

    if type_data_input == "filtre":
        acquisitions_gps = get_acquisitions(type_data_input)
        acquisition_imu = None
        out_path = "./output/HTML/plot_data_filtrees/"

    elif type_data_input == "filtre_prediction":
        acquisition_imu, acquisitions_gps = get_acquisitions(type_data_input)
        out_path = "./output/HTML/plot_data_filtrees/"

    elif type_data_input == "raw":
        acquisitions_gps = get_acquisitions(type_data_input)
        out_path = "./output/HTML/plot_raw_data/"

    else:
        raise ParametreIncorrectErreur(f"{type_data_input} inconnu, parametre acceptés:\n\t ('filtre', 'filtre_prediction', 'raw')")

    # initialisation du filtre
    dt = 1. if type_data_input !='filtre_prediction' else 0.1
    F_t = F(dt)
    G_t = G(dt)
    H = np.block([np.eye(3), np.zeros((3, 3))])
    filtre = FiltreKalman(F_t, H, G_t, Q, R)

    # generation des fichiers
    if type_data_input != 'filtre_prediction':
        for k, v in acquisitions_gps.items():

            if type_data_input == 'filtre':
                print(f'Filtrage de {BLUE}{k}{RESET} dans {GREEN}{v}{RESET}')
                filtrage(k, v, filtre)

                print(f'Génération du fichier html de {GREEN}{v}{RESET}')
                plot_GNSS(v+".csv", out_path)
            else:
                print(f'Génération de la carte de {GREEN}{v}{RESET}')
                plot_GNSS(k+".csv", out_path)
            print("\n")
    # TODO faire le cas avec un fichier de prediction
    # else:
    #     filtrage()

class ParametreIncorrectErreur (Exception):
    """Erreur de saisie de parametre formel"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('output',
                        choices=['raw', 'filtre', 'all'],
                        help='output : raw pour generer seulement les html des données brutes. \
                                       filtre pour filtrer les données et generer les html. \
                                        all pour faire les deux')
    parser.add_argument('-s', '--spherique',
                        action='store_true',
                        help='change les coordonnées de FiltreKalamn.x en sphérique')
    args = parser.parse_args()

    f = filtrage_csv if args.spherique else filtrage_cartesien

    if args.output == '--filtre':
        generation_fichiers("filtre", filtrage=f)
    elif args.output == '--raw':
        generation_fichiers("raw", filtrage=f)
    else:
        generation_fichiers("raw", filtrage=f)
        generation_fichiers("filtre", filtrage=f)