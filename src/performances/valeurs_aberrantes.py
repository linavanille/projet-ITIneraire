#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def nettoyer_csv_gps(chemin_csv, taille_fenetre=27, facteur_iqr=3.0):
	assert taille_fenetre % 2 == 1, "La taille de la fenêtre doit être impaire."

	df = pd.read_csv(chemin_csv)
	altitudes = df["Altitude"].values
	moitie = taille_fenetre // 2
	valide = np.full(len(altitudes), True)

	for i in range(moitie, len(altitudes) - moitie):
		voisinage = np.concatenate((altitudes[i - moitie:i], altitudes[i + 1:i + moitie + 1]))
		q1 = np.percentile(voisinage, 25)
		q3 = np.percentile(voisinage, 75)
		iqr = q3 - q1
		borne_inf = q1 - facteur_iqr * iqr
		borne_sup = q3 + facteur_iqr * iqr

		if not (borne_inf <= altitudes[i] <= borne_sup):
			valide[i] = False

	df_clean = df[valide].copy()

	df_clean.to_csv(chemin_csv, index=False)

	print(f"{len(df) - len(df_clean)} lignes supprimées.")
