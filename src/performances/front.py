#!/usr/bin/env python 3

from performances import Performances, main
import os

class Front () :

	def __init__(self):
		print("Demarrage de l'application")

	@property
	def menu(self):
		def affichage_menu():
			os.system('clear')
			print("---- Menu ----\n")
			print("\t 1 - Historique")
			print("\t 2 - Mode")
			print("")
			print("\t C - Crédits")
			print("\t H - Help!!!")
			print("")
			print("Q - Quitter")

		choix = ''
		while choix != "Q" :

			affichage_menu()

			choix = input("Menu : ").upper()

			if choix == "1" :
				self.historique
			elif choix == "2" :
				self.mode
			elif choix == "C" :
				self.credit
			elif self.help == "H" :
				self.help

	@property
	def historique(self):
		def affichage_historique():
			os.system("clear")
			print("---- Liste des acquisitions passées ----\n")
			liste_acquisitions = os.listdir("./output/CSV_FiltrePrediction/")
			for i in range(len(liste_acquisitions)):
				print(f"\t{i+1} - {liste_acquisitions[i][:-4]}")
			print("\nR - Retour menu")
			return liste_acquisitions

		choix = ''
		while choix != "R":
			liste_acquisitions = affichage_historique()
			choix = input("Option : ").upper()

			try:
				num = int(choix) - 1
				if 0 <= num < len(liste_acquisitions):
					main()
			except:
				pass


	@property
	def mode (self):
		def affichage_mode(opt):
			os.system('clear')
			print("---- Mode ---- \n")
			print(f"Mode selectionné : {opt} \n")
			print("\t 1 - Classique")
			print("\t 2 - Spécial")
			print("")
			print("-- Appuyer sur le bouton pour lancer une acquisition--")
			print("")
			print("R - retour menu")

		choix = ''
		selection = "Classique"
		while choix != "R" :
			affichage_mode(selection)
			choix = input("Option : ").upper()

			if choix == "1" :
				selection = "Classique"
				self.acquisition_classique
			elif choix == "2" :
				selection = "Spécial"
				self.acquisition_speciale

	@property
	def credit(self):
		pass

	@property
	def help(self):
		pass

	@property
	def acquisition_classique(self):
		pass

	@property
	def acquisition_speciale(self):
		pass


if __name__ == "__main__" :
	app = Front()
	app.menu
