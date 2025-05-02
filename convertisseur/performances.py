#!/usr/bin/env python 3 
"""Module permettant de calculer les performances de l'utilisateur""" 

import numpy as np 
import matplotlib.pyplot as plt

data = np.loadtxt("./historique/test.csv", delimiter=",", dtype=str, skiprows=1)
timestamps = data[:,0]
latitudes = data[:,1]
longitudes = data[:,2]
altitudes = np.char.replace(data[:, 3], ',', '.').astype(float)

dates = np.array([ts.split(" - ")[0].replace("/", "-") for ts in timestamps])
heures = np.array([ts.split(" - ")[1] for ts in timestamps])

class Performances () :
	
    def __init__(self,chemin):
    	self.data = np.loadtxt(chemin, delimiter=",", dtype=str, skiprows=1)
    	self.timestamps = self.data[:,0]
	self.latitudes = self.data[:,1]
	self.longitudes = self.data[:,2]
	self.altitudes = np.char.replace(self.data[:, 3], ',', '.').astype(float)

	self.dates = np.array([ts.split(" - ")[0].replace("/", "-") for ts in self.timestamps])
	self.heures = np.array([ts.split(" - ")[1] for ts in selF.timestamps])

	def conversion_heures_secondes(heures):
	    secondes = []
	    for h in heures:
		h, m, s = map(int, h.split(":"))
		secondes.append(h * 3600 + m * 60 + s)
	    return np.array(secondes)

	def point_depart(self): 
	    """Retourne les coordonnées et l'altitude du premier point"""
	    return {
		"Date": self.dates[0],
		"Heure": self.heures[0],
		"Latitude": self.latitudes[0],
		"Longitude": self.longitudes[0],
		"Altitude": self.altitudes[0],
	    }

	def point_arrivee(self): 
	    """Retourne les coordonnées et l'altitude du dernier point"""
	    return {
		"Date": self.dates[-1],
		"Heure": self.heures[-1],
		"Latitude": self.latitudes[-1],
		"Longitude": self.longitudes[-1],
		"Altitude": self.altitudes[-1],
	    }
    
	def distance_totale(self):
	    """Calcule la distance totale parcourue en sommant les distances entre tous les points GPS consécutifs."""
	    #total = 0
	    #for i in range(len(latitudes) - 1):
	    #    total += distance_entre_2_points(latitudes[i], longitudes[i], latitudes[i+1], longitudes[i+1])
	    #return total
	    pass 
    
    
	def duree_totale_secondes(self.):
	    """Calcule la durée totale de l'acquisition en secondes."""
	    secondes = Performances.conversion_heures_secondes(self.heures)
	    debut = secondes[0]
	    fin = secondes[-1] 
	    duree_totale_secondes = fin - debut 
	    return duree_totale_secondes
    
	def duree_totale_minutes(self):
	    """Calcule la durée totale de l'acquisition en minutes.""" 
	    return self.duree_totale_secondes() / 60
    
	def calcul_imc(poids_kg, taille_m):
	    """Calcule l'IMC à partir du poids (kg) et de la taille (m)."""
	    imc = poids_kg / (taille_m ** 2)
	    
	    if imc < 18.5:
		interpretation = "Insuffisance pondérale"
	    elif imc < 25:
		interpretation = "Corpulence normale"
	    elif imc < 30:
		interpretation = "Surpoids"
	    else:
		interpretation = "Obésité"

	    return round(imc, 2), interpretation

	def vitesse_moyenne(self):
	    temps_min = self.duree_totale_minutes()
	    distance = self.distance_totale()  
	    return distance / temps_min
    
	def vitesse_minimale(self):
	    """
	    Calcule la vitesse minimale (en m/s) entre tous les points consécutifs,
	    en utilisant la fonction vitesse_instantanee().
	    """
	    vitesses = []
	    for i in range(1, len(self.latitudes)):
		v = vitesse_instantanee(i)
		vitesses.append(v)
	    return min(vitesses) 
    
	def altitude_max(self): 
	    """Retourne l'altitude maximale atteinte durant le trajet (en mètres)."""
	    return np.max(self.altitudes)

	def altitude_en_fonction_du_temps(self):
	    """
	    Trace l'altitude en fonction du temps écoulé depuis le début.
	    """
	    temps_sec = Performances.conversion_heures_secondes(self.heures)
	    temps_depuis_debut = temps_sec - temps_sec[0]  # même longueur que altitudes

	    plt.figure()
	    plt.plot(temps_depuis_debut, self.altitudes, marker='o', linestyle='-')
	    plt.title("Profil Altimétrique")
	    plt.xlabel("Temps écoulé (s)")
	    plt.ylabel("Altitude (m)")
	    plt.grid(True)
	    plt.tight_layout()
	    plt.show()
    
	def detecter_pauses(self,seuil=0.2):
	    """
	    Détecte les pauses pendant le trajet.
	    Retourne une liste d'indices où la vitesse instantanée est inférieure au seuil.
	    """
	    pauses = []
	    for i in range(1, len(self.latitudes)):
		v = self.vitesse_instantanee(i)
		if v < seuil:
		    pauses.append(i)
	    return pauses
    
	def vitesse_instantanee(self,i):
	    """
	    Calcule la vitesse instantanée entre le point i-1 et i (en m/s).
	    """
	    temps_sec = Performances.conversion_heures_secondes(heures)
	    dt = temps_sec[i] - temps_sec[i - 1]
	    if dt <= 0:
		return 0
	    d = Performances.distance_entre_2_points(self.latitudes[i - 1], self.longitudes[i - 1],
		                         self.latitudes[i], self.longitudes[i])
	    return d / dt

	def distance_entre_2_points(lat1, lon1, lat2, lon2):
	    from math import radians, sin, cos, sqrt, atan2
	    R = 6371000  # rayon Terre en m
	    phi1, phi2 = radians(lat1), radians(lat2)
	    dphi = radians(lat2 - lat1)
	    dlambda = radians(lon2 - lon1)
	    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
	    c = 2 * atan2(sqrt(a), sqrt(1 - a))
	    return R * c

def main():
    test = Performances("./historique/test.csv")
    print("Point de départ:", test.point_depart())
    print("Point d'arrivée:", test.point_arrivee())
    print("Durée totale en secondes:", test.duree_totale_secondes())
    print("Durée totale en minutes:", test.duree_totale_minutes())
    print("IMC Lina:", test.calcul_imc(49, 1.63))
    print("Altitude maximale:", test.altitude_max())
    test.altitude_en_fonction_du_temps()
    pauses = detecter_pauses()
    print(f"Nombre de pauses détectées : {len(pauses)}")
    for i in pauses:
        print(f"Pause vers {heures[i]} à la position ({latitudes[i]}, {longitudes[i]})")
    
if __name__ == "__main__":
    main()
