from pandas import DataFrame
import numpy as np
from Struc_stat_gps import Donnees_gps
from scipy.stats import wilcoxon
from geopy.distance import geodesic
from matplotlib import pyplot as plt

class Stat():

    def __init__(self, donnees_gps):
        self.donnees = donnees_gps

    #Etapes pour faire le test des rangs
    #-recuper les couple (lat, long) des deux donées à tester
    #-calculer l'erreur à chaque temps i (on calcule ici la distance avec geodesic)
    #f-aire le test de wilcoxon (test des rangs) avec cette liste d'erreur

    def _erreurs(self, nom_donnee1, nom_donnee2):
        lat_long1 = list(zip(self.donnees[nom_donnee1+"_Latitude"], self.donnees[nom_donnee1+"_Longitude"]))
        lat_long2 = list(zip(self.donnees[nom_donnee2+"_Latitude"], self.donnees[nom_donnee2+"_Longitude"]))
        erreurs = [geodesic(lat_long1[i], lat_long2[i]).meters for i in range(len(lat_long1))]
        return erreurs  
    
    def test_des_rangs(self, nom_donnee1, nom_donnee2):
        return wilcoxon(self._erreurs(nom_donnee1, nom_donnee2))


    def boxplot_erreurs(self, nom_donnee1, nom_donnee2):
        
        plt.boxplot(self._erreurs(nom_donnee1, nom_donnee2), vert=True, patch_artist=True)
        plt.title(f"Boxplot des erreurs : {nom_donnee1} vs {nom_donnee2}")
        plt.ylabel("Erreur (mètres)")
        plt.grid(True)
        plt.show()
    
    def moyenne_erreurs(self, nom_donnee1, nom_donnee2):
        return np.mean(self._erreurs(nom_donnee1, nom_donnee2))

    def courbe_erreurs(self, nom_donnee1, nom_donnee2):

        plt.figure(figsize=(10, 5))
        plt.plot(self._erreurs(nom_donnee1, nom_donnee2), marker='o', linestyle='-', color='blue')
        plt.title(f"Évolution des erreurs : {nom_donnee1} vs {nom_donnee2}")
        plt.xlabel("Index de mesure")
        plt.ylabel("Erreur (mètres)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

