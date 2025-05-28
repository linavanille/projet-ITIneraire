#!/usr/bin/env python3

import os
from performances import Performances

class MenuPerformances:

	def __init__(self):
		self.chemin_csv = self.selection_fichier_csv()
		self.poids = float(input("Entrez votre poids (kg) : "))
		self.taille = float(input("Entrez votre taille (m) : "))
		self.perf = Performances(self.chemin_csv)
		self.lancer_menu()

	def selection_fichier_csv(self):
		os.system("clear")
		print("---- Sélection du fichier CSV ----\n")
		historique = "./output/Historique/"
		fichiers = [f for f in os.listdir(historique) if f.endswith(".csv")]
		for i, fichier in enumerate(fichiers):
			print(f"{i+1} - {fichier}")
		print("\n")

		while True:
			try:
				choix = int(input("Choisissez un fichier : ")) - 1
				if 0 <= choix < len(fichiers):
					return f"{historique}{fichiers[choix]}"
			except:
				pass

	def lancer_menu(self):
		while True:
			os.system("clear")
			print("---- Menu Performances ----\n")
			print("1 - Départ et arrivée")
			print("2 - Altitude")
			print("3 - Vitesse")
			print("4 - Distance & Durée")
			print("5 - Énergie & IMC")
			print("6 - Pauses")
			print("7 - Graphiques")
			print("Q - Quitter\n")

			choix = input("Votre choix : ").upper()

			match choix:
				case "1":
					self.afficher_infos_generales()
				case "2":
					self.afficher_altitude()
				case "3":
					self.afficher_vitesse()
				case "4":
					self.afficher_distance_duree()
				case "5":
					self.afficher_energie_imc()
				case "6":
					self.afficher_pauses()
				case "7":
					self.graphiques()
				case "Q":
					break

			input("\nAppuyez sur Entrée pour continuer...")

	def afficher_infos_generales(self):
		print(">>> Point de départ :", self.perf.point_depart())
		print(">>> Point d’arrivée :", self.perf.point_arrivee())

	def afficher_altitude(self):
		print(f"Altitude max : {self.perf.altitude_max():.2f} m")
		print(f"Altitude min : {self.perf.altitude_min():.2f} m")
		print(f"Altitude moyenne : {self.perf.altitude_moyenne():.2f} m")

	def afficher_vitesse(self):
		print(f"Vitesse moyenne : {self.perf.vitesse_moyenne():.2f} m/s")
		print(f"Vitesse max : {self.perf.vitesse_max():.2f} m/s")
		print(f"Vitesse min : {self.perf.vitesse_minimale():.2f} m/s")

	def afficher_distance_duree(self):
		print(f"Distance totale : {self.perf.distance_totale():.2f} m")
		print(f"Durée totale : {self.perf.duree_totale_secondes()} sec ({self.perf.duree_totale_minutes():.2f} min)")
		print("Temps entre points :", self.perf.temps_ecoule_secondes())

	def afficher_energie_imc(self):
		kcal = self.perf.calories_brulees(self.poids, self.taille)
		imc, interpretation = self.perf.calcul_imc(self.poids, self.taille)
		print(f"Calories brûlées : {kcal} kcal")
		print(f"IMC : {imc} — {interpretation}")

	def afficher_pauses(self):
		pauses = self.perf.detecter_pauses()
		print(f"Nombre de pauses : {len(pauses)}")
		for i in pauses:
			print(f"- Pause à {self.perf.heures[i]} ({self.perf.latitudes[i]}, {self.perf.longitudes[i]})")

	def graphiques(self):
		print("Affichage du profil altimétrique...")
		self.perf.altitude_en_fonction_du_temps()
		print("Affichage des vitesses...")
		self.perf.tracer_vitesse()
		print("Affichage altitude/distance...")
		self.perf.tracer_altitude_distance()


if __name__ == "__main__":
	MenuPerformances()

