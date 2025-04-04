from pandas import DataFrame
import numpy as np
from Struc_stat_gps import Donnees_gps
from scipy.stats import wilcoxon
from geopy.distance import geodesic as distance

class Stat :

    def __init__(self, donnees_gps):
        self._donnees = donnees_gps


    #Etapes pour faire le test des rangs
    #-recuper les couple (lat, long) des deux donées à tester
    #-calculer l'erreur à chaque temps i (on calcule ici la distance avec geodesic)
    #f-aire le test de wilcoxon (test des rangs) avec cette liste d'erreur
    
    def test_des_rangs(self, nom_donnee1, nom_donnee2):
        lat_long1 = list(zip(self._donnees[nom_donnee1 + "_Latitude"], self._donnees[nom_donnee1 + "_Longitude"]))
        lat_long2 = list(zip(self._donnees[nom_donnee2 + "_Latitude"], self._donnees[nom_donnee2 + "_Longitude"]))
        erreurs = [geodesic(lat_long1[i], lat_long2[i]).meters for i in range(len(lat_long1))]
        return wilcoxon(erreurs)

    #analyser le résultat
    #donne des infos sur le biais
