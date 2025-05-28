import pandas as pd
from datetime import datetime,timezone

def traitement_date_gps(chaine,sep):
		if not isinstance(chaine, str):
			raise TypeError("la chaine à traiter doit être une Chaine de Caractères")

		jour, horaire = chaine.split(sep["sep_central"])
		h = [int(elt) for elt in jour.split(sep["sep_jour"]) + horaire.split(sep["sep_heure"])]
		return datetime(h[0],h[1],h[2],h[3]+2,h[4],h[5],tzinfo=timezone.utc)

def remplacement_date_formatee_gps(data):
    if not isinstance(data, pd.core.frame.DataFrame) :
        raise TypeError("n'accepte que des DataFrame")

    c = data.columns
    print(c)
    nom_col_date = 'UTC'
    sep = {"sep_jour":"/","sep_central":"-","sep_heure":":"}

    data.insert(loc=1, column="Date_Formatee", value=[traitement_date_gps(elt,sep) for elt in data[nom_col_date]])
    del data[nom_col_date]

def conversion(data):
    remplacement_date_formatee_gps(data)
    return data