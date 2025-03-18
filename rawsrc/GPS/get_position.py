import time
from gnss import *
from ..utils import *
import argparse

COORDS_DD=0
COORDS_DMM=1
COORDS_DMS=2

def get_position(csv_out=None,no_LCD=False):
  """
  Lit les données GNSS et affiche la position du module GNSS sur l'invité de commandes et le LCD.

  Arguments:
  - csv_out: Le chemin et nom de fichier CSV pour l'enregistrement des acquisitions GNSS. 
             S'il n'est pas défini, aucun enregistrement n'est effectué.
  - no_LCD: Booléen optionnel indiquant si on ne veut pas utiliser le LCD. Valeur par défaut à False. 
  """
  
  # A COMPLETER
  GNSS_DEVICE_ADDR = ...
  LCD_DEVICE_ADDR = ...

  mode=GPS_BEIDOU_GLONASS
  gnss = GNSS(1, GNSS_DEVICE_ADDR)
  gnss.initialisation(mode)
  save_csv=False
  if csv_out is not None:
    save_csv=True
    if not(csv_out.endswith('.csv')):
      csv_out +='.csv'
    record = CSVHandler(csv_out)
    record.create_csv_with_header(['Timestamp','UTC','Latitude','Longitude'])

  if not(no_LCD):
    lcd_display = LCD(LCD_DEVICE_ADDR)
  
  try:
    while True:
      # Actualisation des données GNSS
      gnss.update()
      if save_csv and gnss.reception_ok:
        record.append_row([gnss.timestamp,gnss.utc,gnss.latitude.coords_DD,gnss.longitude.coords_DD])
      
      # A COMPLETER
      latitude = ...
      longitude = ...      
      
      # Affichage sur le LCD
      if gnss.reception_ok:
        if not(no_LCD):
          # A COMPLETER
          lcd_display.afficher(...)
      else:
        if not(no_LCD):
          lcd_display.afficher("Recherche de    signal GNSS...")
      
      # Affichage sur console
      if gnss.reception_ok:
        print("--------------------------------------------------------------")
        print(f"Nombre de satellites utilisés: {gnss.number_satellites}")
        print(f"Latitude : {latitude}")
        print(f"Longitude : {longitude}")
        print("")
      else:
        print("Recherche de signal GNSS...")
        
      time.sleep(1)
      
  except KeyboardInterrupt as e:
    print("Arrêt du programme")
    if not(no_LCD):
      lcd_display.effacer()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--no-LCD', 
                      action='store_true',
                      help="Permet de ne rien afficher sur le LCD.")
  parser.add_argument('--save-path', '-s',
                      type=str,
                      default=None,
                      help="Chemin où sauvegarder les données."
    )
  args = parser.parse_args()
  
  get_position(args.save_path,args.no_LCD)