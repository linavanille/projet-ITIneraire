#!/usr/bin/env python 3 
"""Module permettant de calculer les performances de l'utilisateur""" 

import numpy as np 
import matplotlib.pyplot as plt

data = np.loadtxt("test.csv", delimiter=",", dtype=str, skiprows=1)
timestamps = data[:,0]
latitudes = data[:,1]
longitudes = data[:,2]
altitudes = np.char.replace(data[:, 3], ',', '.').astype(float)

dates = np.array([ts.split(" - ")[0].replace("/", "-") for ts in timestamps])
heures = np.array([ts.split(" - ")[1] for ts in timestamps])

def conversion_heures_secondes(heures):
    secondes = []
    for h in heures:
        h, m, s = map(int, h.split(":"))
        secondes.append(h * 3600 + m * 60 + s)
    return np.array(secondes)

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
    
def distance_totale():
    """Calcule la distance totale parcourue en sommant les distances entre tous les points GPS consécutifs."""
    #total = 0
    #for i in range(len(latitudes) - 1):
    #    total += distance_entre_2_points(latitudes[i], longitudes[i], latitudes[i+1], longitudes[i+1])
    #return total
    pass 
    
    
def duree_totale_secondes():
    """Calcule la durée totale de l'acquisition en secondes."""
    secondes = conversion_heures_secondes(heures)
    debut = secondes[0]
    fin = secondes[-1] 
    duree_totale_secondes = fin - debut 
    return duree_totale_secondes
    
def duree_totale_minutes():
    """Calcule la durée totale de l'acquisition en minutes."""
    duree_totale_secondes() 
    duree_totale_minutes = duree_totale_secondes() / 60
    return duree_totale_minutes
    
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

def vitesse_moyenne(temps, distance):
    temps = duree_totale_minutes()
    distance = distance_totale()
    vitesse_moyenne = distance / temps 
    return vitesse_moyenne
    
def vitesse_minimale():
    """
    Calcule la vitesse minimale (en m/s) entre tous les points consécutifs,
    en utilisant la fonction vitesse_instantanee().
    """
    vitesses = []
    for i in range(1, len(latitudes)):
        v = vitesse_instantanee(i)
        vitesses.append(v)
    return min(vitesses) if vitesses else 0
    
def altitude_max(): 
    """Retourne l'altitude maximale atteinte durant le trajet (en mètres)."""
    return np.max(altitudes)
	#renvoie 202.4 pour test.csv alors que c'est mm pas une altitude atteinte, va savoir...

def altitude_en_fonction_du_temps():
    """
    Trace l'altitude en fonction du temps écoulé depuis le début.
    """
    temps_sec = conversion_heures_secondes(heures)
    temps_depuis_debut = temps_sec - temps_sec[0]  # même longueur que altitudes

    plt.figure()
    plt.plot(temps_depuis_debut, altitudes, marker='o', linestyle='-')
    plt.title("Profil Altimétrique")
    plt.xlabel("Temps écoulé (s)")
    plt.ylabel("Altitude (m)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def main():
    print("Point de départ:", point_depart())
    print("Point d'arrivée:", point_arrivee())
    print("Durée totale en secondes:", duree_totale_secondes())
    print("Durée totale en minutes:", duree_totale_minutes())
    print("IMC Lina:", calcul_imc(49, 1.63))
    print("Altitude maximale:", altitude_max())
    altitude_en_fonction_du_temps()
    
if __name__ == "__main__":
    main()
