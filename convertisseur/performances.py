#!/usr/bin/env python 3 
"""Module permettant de calculer les performances de l'utilisateur""" 

import numpy as np 

data = np.loadtxt("nom_fichier.csv", delimeter=",")
timestamps = data[:,0]
latitudes = data[:,1]
longitudes = data[:,2]
altitudes = data[:,3]

dates = np.array([ts.decode("utf-8").split(" - ")[0].replace("/", "-") for ts in timestamps])  # YYYY-MM-DD
heures = np.array([ts.decode("utf-8").split(" - ")[1] for ts in timestamps])

def conversion_heures_secondes(heures)

def temps_ecoule_entre_deux_points():

def point_depart(): 
    """Retourne les coordonnées et l'altitude du premier point"""
    return {
        "Date": dates[0],
        "Heure": heures[0],
        "Latitude": latitudes[0],
        "Longitude": longitudes[0],
        "Altitude": altitudes[0],
    }

def point_arrivee(): 
    """Retourne les coordonnées et l'altitude du dernier point"""
    return {
        "Date": dates[-1],
        "Heure": heures[-1],
        "Latitude": latitudes[-1],
        "Longitude": longitudes[-1],
        "Altitude": altitudes[-1],
    }


if __name__ == "__main__":
    main()