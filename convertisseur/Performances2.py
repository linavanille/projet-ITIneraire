#!/usr/bin/env python3
"""Module permettant de calculer les performances de l'utilisateur"""

import numpy as np
import matplotlib.pyplot as plt

class Performances2:

    def __init__(self, chemin):
        self.data = np.loadtxt(chemin, delimiter=",", dtype=str, skiprows=1)
        self.timestamps = self.data[:, 0]
        self.latitudes = self.data[:, 1].astype(float)
        self.longitudes = self.data[:, 2].astype(float)
        self.altitudes = np.char.replace(self.data[:, 3], ',', '.').astype(float)

        self.dates = np.array([ts.split(" - ")[0].replace("/", "-") for ts in self.timestamps])
        self.heures = np.array([ts.split(" - ")[1] for ts in self.timestamps])

    def conversion_heures_secondes(self, heures):
        secondes = []
        for h in heures:
            h, m, s = map(int, h.split(":"))
            secondes.append(h * 3600 + m * 60 + s)
        return np.array(secondes)

    def point_depart(self):
        return {
            "Date": self.dates[0],
            "Heure": self.heures[0],
            "Latitude": self.latitudes[0],
            "Longitude": self.longitudes[0],
            "Altitude": self.altitudes[0],
        }

    def distance_entre_2_points(self, lat1, lon1, lat2, lon2):
        R = 6371000  # Rayon de la Terre en m
        lat1_rad, lon1_rad = np.radians([float(lat1), float(lon1)])
        lat2_rad, lon2_rad = np.radians([float(lat2), float(lon2)])
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return R * c

    def distances_parcours(self):
        distances = []
        for i in range(len(self.latitudes) - 1):
            d = self.distance_entre_2_points(
                self.latitudes[i], self.longitudes[i],
                self.latitudes[i + 1], self.longitudes[i + 1]
            )
            distances.append(d)
        return np.array(distances)

    def temps_ecoule_secondes(self):
        secondes = self.conversion_heures_secondes(self.heures)
        delta_secondes = np.diff(secondes)
        return delta_secondes

    def temps_entre_deux_points(self, h1, h2):
        s1 = self.conversion_heures_secondes([h1])[0]
        s2 = self.conversion_heures_secondes([h2])[0]
        delta = s2 - s1
        return delta

    def vitesse_entre_deux_points(self, lat1, lon1, h1, lat2, lon2, h2):
        distance = self.distance_entre_2_points(lat1, lon1, lat2, lon2)
        temps = self.temps_entre_deux_points(h1, h2)
        if temps == 0:
            return 0.0
        return round(distance / temps, 3)

    def vitesses_parcours(self):
        vitesses = []
        for i in range(len(self.latitudes) - 1):
            v = self.vitesse_entre_deux_points(
                self.latitudes[i], self.longitudes[i], self.heures[i],
                self.latitudes[i + 1], self.longitudes[i + 1], self.heures[i + 1]
            )
            vitesses.append(v)
        return np.round(np.array(vitesses), 3)

    def calories_brulees(self, poids, taille):
        vitesses = self.vitesses_parcours()
        calories = 0
        for v, t in zip(vitesses, self.temps_ecoule_secondes()):
            # MET = Metabolic Equivalent of Task
            # estimation simple selon vitesse : marche rapide ~ 5 km/h = MET 3.5, course 8 km/h = MET 8
            v_kmh = v * 3.6
            if v_kmh < 5:
                met = 2.5
            elif v_kmh < 8:
                met = 5
            else:
                met = 8
            kcal = (met * poids * t) / 3600
            calories += kcal
        return round(calories, 2)

    def vitesse_max(self):
        """Renvoie la vitesse maximale (en m/s) sur le parcours"""
        vitesses = self.vitesses_parcours()
        return np.max(vitesses) if vitesses.size > 0 else None

    def altitude_moyenne(self):
        """Renvoie l'altitude moyenne (en m)"""
        return np.mean(self.altitudes) if self.altitudes.size > 0 else None

    def altitude_min(self):
        """Renvoie l'altitude minimale (en m)"""
        return np.min(self.altitudes) if self.altitudes.size > 0 else None

    def tracer_vitesse(self):
        """Trace l'évolution de la vitesse (en m/s) au cours du temps"""
        vitesses = self.vitesses_parcours()
        temps = self.temps_ecoule_secondes()

        # Calcul du temps cumulé depuis le départ
        temps_cumule = np.cumsum(temps)

        # Moyenne des temps entre chaque paire de points pour aligner avec les vitesses
        temps_milieu = (temps_cumule[:-1] + temps_cumule[1:]) / 2
        temps_milieu = np.insert(temps_milieu, 0, 0)  # Commence à 0

        plt.figure(figsize=(10, 5))
        plt.plot(temps_milieu[:len(vitesses)], vitesses, label="Vitesse (m/s)", color="blue")
        plt.xlabel("Temps écoulé (s)")
        plt.ylabel("Vitesse (m/s)")
        plt.title("Évolution de la vitesse")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


    def tracer_altitude_distance(self):
        """Trace l'altitude (en m) en fonction de la distance cumulée (en m)"""
        distances = self.distances_parcours()
        distance_cumulee = np.insert(np.cumsum(distances), 0, 0)

        plt.figure(figsize=(10, 5))
        plt.plot(distance_cumulee, self.altitudes, label="Altitude (m)")
        plt.xlabel("Distance (m)")
        plt.ylabel("Altitude (m)")
        plt.title("Altitude en fonction de la distance")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

 
def main():
    perf = Performances2("./historique/test.csv")

    # Vitesse entre 2 points
    v = perf.vitesse_entre_deux_points(
        perf.latitudes[0], perf.longitudes[0], perf.heures[0],
        perf.latitudes[1], perf.longitudes[1], perf.heures[1]
    )
    print(f"Vitesse entre les deux premiers points : {v:.2f} m/s")

    # Tableau de toutes les vitesses
    vitesses = perf.vitesses_parcours()
    print(f"Vitesses sur tout le parcours (m/s) : {vitesses}")


    poids = 70  # en kg
    taille = 1.75  # en m

    kcal = perf.calories_brulees(poids, taille)
    print(f"Calories brûlées : {kcal} kcal")

    print(f"Vitesse maximale : {perf.vitesse_max():.2f} m/s")
    print(f"Altitude moyenne : {perf.altitude_moyenne():.2f} m")
    print(f"Altitude minimale : {perf.altitude_min():.2f} m")
    perf.tracer_vitesse()
    perf.tracer_altitude_distance()


if __name__ == "__main__":
    main()