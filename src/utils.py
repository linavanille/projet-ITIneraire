import pandas as pd
import xml.etree.ElementTree as ET
import re
from datetime import datetime

def convert_gpx_to_csv(gpx_file, csv_file):
    """
    Convertit un fichier GPX en un fichier CSV avec les colonnes 'Timestamp', 'Latitude' et 'Longitude'.
    
    Arguments:
    - gpx_file: Chemin du fichier GPX d'entrée.
    - csv_file: Chemin du fichier CSV de sortie.
    """
    
    def get_namespace(element):
        """ Récupère l'espace de noms utilisé dans le fichier GPX """
        match = re.match(r'\{.*\}', element.tag)
        return match.group(0) if match else ''
    
    """
    def format_time(date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return f"{date_obj.year:04}/{date_obj.month:02}/{date_obj.day:02} - {date_obj.hour:02}:{date_obj.minute:02}:{date_obj.second:02}"
    """
    def format_time(date_str):
        date_str = date_str.rstrip("Z")  # Supprime le 'Z' à la fin
        date_str = date_str.split('.')[0]  # Supprime les millisecondes si présentes
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return f"{date_obj.year:04}/{date_obj.month:02}/{date_obj.day:02} - {date_obj.hour:02}:{date_obj.minute:02}:{date_obj.second:02}"


    # Parse le fichier GPX
    tree = ET.parse(gpx_file)
    root = tree.getroot()

    # Détecter l'espace de noms utilisé
    namespace = get_namespace(root)

    # Extraire les données
    data = []
    for trk in root.findall(f"{namespace}trk"):
        for trkseg in trk.findall(f"{namespace}trkseg"):
            for trkpt in trkseg.findall(f"{namespace}trkpt"):
                lat = trkpt.get("lat")
                lon = trkpt.get("lon")
                time_element = trkpt.find(f"{namespace}time")
                timestamp = time_element.text if time_element is not None else None
                data.append([format_time(timestamp), lat, lon])

    # Convertir en DataFrame
    df = pd.DataFrame(data, columns=["UTC", "Latitude", "Longitude"])

    # Enregistrer en fichier CSV
    df.to_csv(csv_file, index=False)
    print(f"Conversion terminée ! Fichier enregistré : {csv_file}")


def correct_csv(csv_file):
    """
    Corrige le format de date d'un fichier CSV (colonne UTC). 
    Un petit problème dans l'enregistrement de la chaîne de caractères
    Dsl... Mais c'est corrigé...
    
    Arguments:
    - csv_file: Chemin du fichier CSV à corriger.
    """
    df = pd.read_csv(csv_file)
    
    def format_date(date_str):
        date_obj = datetime.strptime(date_str, "%Y/%m/%d - %H:%M:%S")
        return f"{date_obj.year:04}/{date_obj.month:02}/{date_obj.day:02} - {date_obj.hour:02}:{date_obj.minute:02}:{date_obj.second:02}"
        
    df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: format_date(x))
    df.to_csv(csv_file,index=False)

if __name__ == "__main__":

    gpx_file = r"C:\Users\INSA\Documents\ITI32\itineraire\output\acquisitions_gps_loger\Leclerc_chloe.gpx"
    csv_file = r"C:\Users\INSA\Documents\ITI32\itineraire\output\acquisitions_gps_loger\Leclerc_chloe.csv"

    convert_gpx_to_csv(gpx_file=gpx_file, csv_file=csv_file)
