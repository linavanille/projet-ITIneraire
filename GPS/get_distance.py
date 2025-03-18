import time
from gnss import *
from ..utils import *
import argparse

def compute_distance(pt1,pt2):
    """
    Calcul de la distance entre 2 points en coordonnées latitude/longitude.
    
    Arguments:
    - pt1: tuple des coordonnées du 1er point (latitude/longitude).
    - pt2: tuple des coordonnées du 2ème point (latitude/longitude).

    Sortie: La distance en mètre entre les 2 points en vol d'oiseau sur la surface de la Terre (sphérique).
    """
    
    # A COMPLETER
    return 0

def format_distance(distance_meters):
    """
    Formate une chaîne représentant une distance avec des unités adaptées (m ou km)
    et une précision dépendant de la distance.

    :param distance_meters: La distance en mètres (float ou int).
    :return: Une chaîne formatée avec l'unité appropriée.
    """
    if distance_meters < 1000:
        # Distance inférieure à 1 km, rester en mètres
        return f"{distance_meters:.0f} m"
    else:
        # Distance égale ou supérieure à 1 km, convertir en kilomètres
        distance_km = distance_meters / 1000
        if distance_km < 10:
            # Moins de 10 km : 2 décimales
            return f"{distance_km:.2f} km"
        elif distance_km < 100:
            # Entre 10 et 100 km : 1 décimale
            return f"{distance_km:.1f} km"
        else:
            # 100 km ou plus : pas de décimales
            return f"{distance_km:.0f} km"

def get_distance(position_target):
  """
  Lit les données GNSS et affiche la distance en vol d'oiseau du point d'intérêt.

  Arguments:
  - position_target: Tuple indiquant la position du point d'intérêt (latitude et longitude en degrés décimaux).
  """
  
  # A COMPLETER
  GNSS_DEVICE_ADDR = ...
  LCD_DEVICE_ADDR = ...

  mode = GPS_BEIDOU_GLONASS
  gnss = GNSS(1, GNSS_DEVICE_ADDR)
  gnss.initialisation(mode)

  lcd_display = LCD(LCD_DEVICE_ADDR)
  
  try:
    while True:
      # Actualisation des données GNSS
      gnss.update()

      # Calcul de la distance à la target      
      distance = format_distance(compute_distance(position_target,(gnss.latitude.coords_DD,gnss.longitude.coords_DD)))
      
      # Affichage sur le LCD
      if gnss.reception_ok:
        lcd_display.afficher(f"Distance:       {distance}")
      else:
        lcd_display.afficher("Recherche de    signal GNSS...")
      
      # Affichage sur console
      if gnss.reception_ok:
        print("--------------------------------------------------------------")
        print(f"Distance de la target: {distance}")
        print("")
        
      time.sleep(1)
      
  except KeyboardInterrupt as e:
    print("Arrêt du programme")
    lcd_display.effacer()
        
if __name__ == "__main__":
    # Instantiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('latitude', 
                        type=float,
                        help="Latitude du point d'intérêt (en degrés décimaux)")
    parser.add_argument('longitude', 
                        type=float,
                        help="Longitude du point d'intérêt (en degrés décimaux)")
    args = parser.parse_args()
	
    get_distance((args.latitude,args.longitude))

