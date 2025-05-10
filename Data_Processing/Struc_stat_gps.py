import pandas as pd
import os
from utils import convert_gpx_to_csv
from datetime import datetime, timezone

class Donnees():
	root = "../output/"
	sources_gps = ("RPI", "Chloe", "Thomas")
	sources_imu = ("Tom", "RPI")
	timezone = timezone.utc

	#méthode d'import des données

	def __gpx_to_csv(paff):
		if not os.path.exists(paff+".csv"):
			convert_gpx_to_csv(paff+".gpx", paff+".csv")

	def __import_GPS_Data(paff):
		for src in Donnees.sources_gps[1:] :
			Donnees.__gpx_to_csv(Donnees.root+paff+"/GPS_"+paff+"_"+src)
		
		return {src:pd.read_csv((Donnees.root+paff+"/GPS_"+paff+"_"+src+".csv")) for src in Donnees.sources_gps}

	def __import_IMU_Data(paff):
		return {src:pd.read_csv((Donnees.root+"IMU/"+paff+"/IMU_"+paff+"_"+src+".csv")) for src in Donnees.sources_imu}

	#Méthode de formatage de date

	def __reformatage_date_source_gps(self):
		for elt in self :
			Donnees.__remplacement_date_formatee_gps(self[elt],1 if elt == 'RPI' else 0)
			
	def __traitement_date_gps(chaine,sep):
		if not isinstance(chaine, str):
			raise TypeError("la chaine à traiter doit être une Chaine de Caractères")
		
		jour, horaire = chaine.split(sep["sep_central"])
		h = [int(elt) for elt in jour.split(sep["sep_jour"]) + horaire.split(sep["sep_heure"])]
		return datetime(h[0],h[1],h[2],h[3],h[4],h[5],tzinfo=Donnees.timezone)
	
	def __remplacement_date_formatee_gps(data, rpi=False):
		if not isinstance(data, pd.core.frame.DataFrame) :
			raise TypeError("n'accepte que des DataFrame")

		c = data.columns
		if 'UTC' in c :
			nom_col_date = 'UTC'
		elif 'Timestamp' in c :
			nom_col_date = 'Timestamp'
		else :
			raise FormatDataCSVInconnuException("La construction du csv ne permet de lire une date correctement : soit UTC soit Timestamp")

		if rpi :
			if data[nom_col_date][0][4] != "-" :
				raise FormatDataCSVInconnuException("Mauvaise séparateur de date dans le csv")
		sep = {"sep_jour":"-","sep_central":"T","sep_heure":":"} if rpi else {"sep_jour":"/","sep_central":"-","sep_heure":":"}
		
		data.insert(loc=1, column="Date_Formatee", value=[Donnees.__traitement_date_gps(elt,sep) for elt in data[nom_col_date]])
		del data[nom_col_date]

	def __reformatage_date_source_imu(self):
		for elt in self :
			Donnees.__remplacement_date_formatee_imu(self[elt], 1 if elt == 'RPI' else 0)
	
	#initialiseur
	
	def __init__(self, chemin, mode="gps"):
		self.mode = mode
		if self.mode == "imu" :
			if not os.path.exists(Donnees.root + "IMU/" + chemin):
				raise AcquisitionInexistanteException(f"le dossier d'acquisition {chemin} n'existe pas. \n Possibilités {os.listdir(Donnees.root+"IMU/")}")

			dossier = os.listdir(Donnees.root+"IMU/"+chemin)

			acces = "IMU_" + chemin + "_"
			for src in Donnees.sources_imu:
				if acces + src + ".csv" not in dossier:
					raise AcquisitionInexistanteException(f"Aucun fichier d'acquisition pour la source {elt}")

			self.donnees = Donnees.__import_IMU_Data(chemin)

			self.__reformatage_date_source_imu()

		elif self.mode == "gps" :
			if not os.path.exists(Donnees.root+chemin):
				raise AcquisitionInexistanteException(f"le dossier d'acquisition {chemin} n'existe pas. \n Possiblités {os.listdir(Donnees.root)}")
			dossier = os.listdir(Donnees.root+chemin)
		
			acces = "GPS_" + chemin + "_"
			for elt in Donnees.sources_gps:
				if acces + elt + ".gpx" not in dossier :
					if acces + elt + ".csv" not in dossier :
						raise AcquisitionInexistanteException(f"Aucun fichier d'acquisition pour la source {elt}")
				
			self._donnees = Donnees.__import_GPS_Data(chemin)
			
			self.__reformatage_date_source_gps()
			
			indice_moins_colonne = Donnees.sources_gps[0]
			min_nb_colonne = len(self[indice_moins_colonne].columns)
			for src in Donnees.sources_gps[1:] :
				if len(self[src].columns) < min_nb_colonne :
					min_nb_colonne = len(self[src].columns)
					indice_moins_colonne = src
			self.champs_avec_Date = self[indice_moins_colonne].columns
			self.champs = self.champs_avec_Date[1:]

			for elt in self :
				if len(self[elt].columns) < 4 :
					print(f"/!\ Warning : Des colonnes sont manquantes pour la source {elt}, attendues : 4, actuelles : {len(self[elt].columns)} => {list(self[elt].columns)}")
		else :
			raise ModeInvalideException("Le mode n'est pas renseigné ou non reconnu")
				

	#méthode built-in
	
	def __getitem__(self,cle):
		'''renvoi un acces direct aux données, pas de copies'''
		if isinstance(cle, str) :
			if cle not in Donnees.sources_gps :
				raise NomSourceInvalideException(f"le nom de la source n'est pas valide. \n Possibilités {Donnees.sources_gps}")
			return self._donnees[cle]
		elif isinstance(cle, tuple) :
			if len(cle) == 2 :
				if isinstance(cle[0], str) :
					if cle[0] not in Donnees.sources_gps :
						raise NomSourceInvalideException(f"le nom de la source n'est pas valide. \n Possibilités {Donnees.sources_gps}")
				if isinstance(cle[1],int):
					if cle[1] < 0 or cle[1] >= len(self[cle[0]]) :
						raise IndexError(f"indice de la ligne hors limite = {len(self[cle[0]])}, donné = {cle[1]}")
					return self[cle[0]].loc[cle[1]]
				if isinstance(cle[1],slice):
					return self[cle[0]].loc[cle[1]]
		else :
			TypeError("format de clé de non supporté")

	def __iter__(self):
		return self._donnees.__iter__()

	#méthode de stat

	@property
	def match_date(self):

		ensemble_date = set()
		for src in Donnees.sources_gps :
			ensemble_date = ensemble_date | set(self[src]["Date_Formatee"])

		#self.champs = ("Latitude", "Longitude")#, "Altitude") # à déplacer
		res = pd.DataFrame({"Date":sorted(list(ensemble_date))})

		index = {src:0 for src in Donnees.sources_gps}
		stock = {src+"_"+c:[] for c in self.champs for src in Donnees.sources_gps}

		for stamp, i in Donnees.__generateur_timestamp_index(res,"Date") :
			for src in Donnees.sources_gps :
				if stamp == self[src].Date_Formatee[index[src]] :
					for c in self.champs :
						stock[src+"_"+c].append(self[src][c][index[src]])
					if index[src] < len(self[src])-1 :
						index[src] += 1
				else :
					for c in self.champs :
						stock[src+"_"+c].append(None)

		for src in Donnees.sources_gps :
			for c in self.champs :
				res.insert(loc=1, column=src+"_"+c, value=stock[src+"_"+c])
		return res 

	@property
	def match_date_sans_NaN(self):
		return Donnees.sans_NaN(self.match_date)

	def __generateur_timestamp_index(data,champ):
		if not isinstance(data, pd.core.frame.DataFrame) :
			raise TypeError(f"data doit être de type DataFrame, actuellement {type(data)}")
		if champ not in data.columns :
			raise KeyError(f"le champ n'existe pas dans le DataFrame, champs disponibles {data.columns}")
		
		for i in range(len(data)):
			yield data[champ][i], i

	def sans_NaN(data):
		a_drop = data.index[data.isnull().any(axis=1)]
		return data.drop(a_drop,axis=0)
	
	def nb_NaN(df):return df.isnull().values.sum()

	
class DonneesException(Exception):
	pass

class ModeInvalideException(DonneesException):
	pass

class AcquisitionInexistanteException(DonneesException):
	pass

class NomSourceInvalideException(DonneesException):
	pass

class FormatDataCSVInconnuException(DonneesException):
	pass