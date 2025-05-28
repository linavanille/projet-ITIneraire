#!/usr/bin/env python3
"""Module permettant de calculer les performances de l'utilisateur"""

import numpy as np
import matplotlib.pyplot as plt
from valeurs_aberrantes import nettoyer_csv_gps

class Performances:

	def __init__(self, chemin):
		nettoyer_csv_gps(chemin)
		raw_data = np.loadtxt(chemin, delimiter=",", dtype=str, skiprows=1)

		valid_rows = [row for row in raw_data if " - " in row[0]]
		data = np.array(valid_rows)

		self.timestamps = data[:, 0]
		self.latitudes = data[:, 1].astype(float)
		self.longitudes = data[:, 2].astype(float)
		self.altitudes = np.char.replace(data[:, 3], ',', '.').astype(float)

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

	def point_arrivee(self):
		return {
			"Date": self.dates[-1],
			"Heure": self.heures[-1],
			"Latitude": self.latitudes[-1],
			"Longitude": self.longitudes[-1],
			"Altitude": self.altitudes[-1],
		}

	def distance_totale(self):
		total = 0
		for i in range(len(self.latitudes) - 1):
			total += self.distance_entre_2_points(
				self.latitudes[i], self.longitudes[i],
				self.latitudes[i + 1], self.longitudes[i + 1]
			)
		return total

	def duree_totale_secondes(self):
		secondes = self.conversion_heures_secondes(self.heures)
		return secondes[-1] - secondes[0]

	def duree_totale_minutes(self):
		return self.duree_totale_secondes() / 60

	@staticmethod
	def calcul_imc(poids_kg, taille_m):
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
		return distance / temps_min if temps_min > 0 else 0

	def vitesse_minimale(self):
		vitesses = []
		for i in range(1, len(self.latitudes)):
			v = self.vitesse_instantanee(i)
			vitesses.append(v)
		return min(vitesses) if vitesses else 0

	def altitude_max(self):
		return np.max(self.altitudes)

	def altitude_en_fonction_du_temps(self):
		temps_sec = self.conversion_heures_secondes(self.heures)
		temps_depuis_debut = temps_sec - temps_sec[0]
		plt.figure()
		plt.plot(temps_depuis_debut, self.altitudes, marker='o', linestyle='-')
		plt.title("Profil Altimétrique")
		plt.xlabel("Temps écoulé (s)")
		plt.ylabel("Altitude (m)")
		plt.grid(True)
		plt.tight_layout()
		plt.show()

	def detecter_pauses(self, seuil=0.2):
		pauses = []
		for i in range(1, len(self.latitudes)):
			v = self.vitesse_instantanee(i)
			if v < seuil:
				pauses.append(i)
		return pauses

	def vitesse_instantanee(self, i):
		temps_sec = self.conversion_heures_secondes(self.heures)
		dt = temps_sec[i] - temps_sec[i - 1]
		if dt <= 0:
			return 0
		d = self.distance_entre_2_points(
			self.latitudes[i - 1], self.longitudes[i - 1],
			self.latitudes[i], self.longitudes[i]
		)
		return d / dt

	def distance_entre_2_points(self, lat1, lon1, lat2, lon2):
		from math import radians, sin, cos, sqrt, atan2
		R = 6371000  # rayon Terre en m
		phi1, phi2 = radians(lat1), radians(lat2)
		dphi = radians(lat2 - lat1)
		dlambda = radians(lon2 - lon1)
		a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
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
		vitesses = self.vitesses_parcours()
		return np.max(vitesses) if vitesses.size > 0 else None

	def altitude_moyenne(self):
		return np.mean(self.altitudes) if self.altitudes.size > 0 else None

	def altitude_min(self):
		return np.min(self.altitudes) if self.altitudes.size > 0 else None

	def tracer_vitesse(self):
		vitesses = self.vitesses_parcours()
		temps = self.temps_ecoule_secondes()
		temps_cumule = np.insert(np.cumsum(temps), 0, 0)
		temps_milieu = (temps_cumule[:-1] + temps_cumule[1:]) / 2
		temps_milieu = np.insert(temps_milieu, 0, 0)

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
	test = Performances("./historique/test.csv")
	print("Point de départ:", test.point_depart())
	print("Point d'arrivée:", test.point_arrivee())
	print("Durée totale en secondes:", test.duree_totale_secondes())
	print("Durée totale en minutes:", test.duree_totale_minutes())
	print("IMC Lina:", Performances.calcul_imc(49, 1.63))
	print("Altitude maximale:", test.altitude_max())
	test.altitude_en_fonction_du_temps()
	pauses = test.detecter_pauses()
	print(f"Nombre de pauses détectées : {len(pauses)}")
	for i in pauses:
		print(f"Pause vers {test.heures[i]} à la position ({test.latitudes[i]}, {test.longitudes[i]})")

	v = test.vitesse_entre_deux_points(test.latitudes[0], test.longitudes[0], test.heures[0],
	                                    test.latitudes[1], test.longitudes[1], test.heures[1])
	print(f"Vitesse entre les deux premiers points : {v:.2f} m/s")

	vitesses = test.vitesses_parcours()
	print(f"Vitesses sur tout le parcours (m/s) : {vitesses}")

	poids = 70  # en kg
	taille = 1.75  # en m

	kcal = test.calories_brulees(poids, taille)
	print(f"Calories brûlées : {kcal} kcal")

	print(f"Vitesse maximale : {test.vitesse_max():.2f} m/s")
	print(f"Altitude moyenne : {test.altitude_moyenne():.2f} m")
	print(f"Altitude minimale : {test.altitude_min():.2f} m")

	test.tracer_vitesse()
	test.tracer_altitude_distance()


if __name__ == "__main__":
	main()
