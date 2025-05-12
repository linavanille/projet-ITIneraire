import numpy as np
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

    def _erreurs_en_metres(self, nom_donnee1, nom_donnee2):
        lat_long1 = list(zip(self.donnees[nom_donnee1+"_Latitude"], self.donnees[nom_donnee1+"_Longitude"]))
        lat_long2 = list(zip(self.donnees[nom_donnee2+"_Latitude"], self.donnees[nom_donnee2+"_Longitude"]))
        erreurs = [geodesic(lat_long1[i], lat_long2[i]).meters for i in range(len(lat_long1))]
        return erreurs 

    def _erreurs_en_degres(self, nom_donnee1, nom_donnee2) :
        lat_long1 = list(zip(self.donnees[nom_donnee1+"_Latitude"], self.donnees[nom_donnee1+"_Longitude"]))
        lat_long2 = list(zip(self.donnees[nom_donnee2+"_Latitude"], self.donnees[nom_donnee2+"_Longitude"]))
        erreurs = [(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])) for p1, p2 in zip(lat_long1, lat_long2)]
        return erreurs


    
    def test_des_rangs(self, nom_donnee1, nom_donnee2, type_analyse = "metres"):
        if type_analyse== "metres":
            return wilcoxon(self._erreurs_en_metres(nom_donnee1, nom_donnee2))
        elif type_analyse == "degres":
            return wilcoxon(self._erreurs_en_degres(nom_donnee1, nom_donnee2)[0]), \
            wilcoxon(self._erreurs_en_degres(nom_donnee1, nom_donnee2)[1])



    def boxplot_erreurs(self, nom_donnee1, nom_donnee2, type_analyse = "metres"):
        if type_analyse == "metres":
            plt.boxplot(self._erreurs_en_metres(nom_donnee1, nom_donnee2), vert=True, patch_artist=True)
            plt.title(f"Boxplot des erreurs : {nom_donnee1} vs {nom_donnee2}")
            plt.ylabel("Erreur (mètres)")
            plt.grid(True)
            plt.show()
        elif type_analyse == "degres":
            lat_errors, lon_errors = zip(*self._erreurs_en_degres(nom_donnee1, nom_donnee2))

            plt.figure(figsize=(8, 6))
            plt.boxplot([lat_errors, lon_errors], vert=True, patch_artist=True,
                        labels=["Latitude", "Longitude"])
            plt.title(f"Boxplot des erreurs en degrés : {nom_donnee1} vs {nom_donnee2}")
            plt.ylabel("Erreur (degrés)")
            plt.grid(True)
            plt.show()

    
    def moyenne_erreurs(self, nom_donnee1, nom_donnee2, type_analyse = "metres"):
        if type_analyse == "metres":
            return np.mean(self._erreurs_en_metres(nom_donnee1, nom_donnee2))
        elif type_analyse == "degres":
            return np.mean(self._erreurs_en_degres(nom_donnee1, nom_donnee2))

    def courbe_erreurs(self, nom_donnee1, nom_donnee2, type_analyse = "metres"):
        if type_analyse == "metres":
            plt.figure(figsize=(10, 5))
            plt.plot(self._erreurs_en_metres(nom_donnee1, nom_donnee2), marker='o', linestyle='-', color='blue')
            plt.title(f"Évolution des erreurs : {nom_donnee1} vs {nom_donnee2}")
            plt.xlabel("Index de mesure")
            plt.ylabel("Erreur (mètres)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        elif type_analyse == "degres":
            plt.figure(figsize=(10, 5))
            erreur_latitude = [x[0] for x in self._erreurs_en_degres(nom_donnee1, nom_donnee2)]
            erreur_longitude = [x[1] for x in self._erreurs_en_degres(nom_donnee1, nom_donnee2)]
            plt.plot(erreur_latitude, marker='o', linestyle='-', color='blue', label="Latitude")
            plt.plot(erreur_longitude, marker='o', linestyle='-', color='red', label="Longitude")
            plt.title(f"Évolution des erreurs : {nom_donnee1} vs {nom_donnee2}")
            plt.xlabel("Index de mesure")
            plt.ylabel("Erreur (mètres)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()


