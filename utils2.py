import csv
import os
from math import sin, cos, acos, radians
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import pandas as pd
import xml.etree.ElementTree as ET
import re

class CSVHandler:
    """
    Classe pour la création et l'écriture d'un fichier CSV pour l'enregistrement des données GNSS.
    """
    def __init__(self, file_path):
        """
        Initialise un gestionnaire pour un fichier CSV.
        
        Arguments:
        - file_path: Chemin vers le fichier CSV.
        """
        assert file_path.endswith('.csv'), f"Le nom de fichier de sauvegarde ({file_path}) doit avoir une extension csv"
        self.file_path = file_path

    def create_csv_with_header(self, header):
        """
        Crée un fichier CSV avec un en-tête s'il n'existe pas déjà.
        
        Arguments:
        - header: Liste contenant les noms des colonnes.
        """
        if not os.path.isfile(self.file_path):
            try:
                with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
            except Exception as e:
                print(f"Erreur lors de la création du fichier CSV : {e}")


    def append_row(self, data):
        """
        Ajoute une ligne de données dans le fichier CSV.
        
        Arguments:
        - data: Liste contenant les valeurs de la ligne à ajouter.
        """
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(data)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la ligne dans le fichier CSV : {e}")
            

class LCD:
    """
    Une classe pour l'affichage sur un LCD, connecté en I2C sur la Raspberry.
    """
    
    def __init__(self,LCD_address):
        """
        Initialise l'afficheur LCD.
        
        Arguments:
        - LCD_address: L'addresse I2C où communique l'afficheur LCD.
        """
        self.lcd = CharLCD(i2c_expander='PCF8574', address=LCD_address, port=1, cols=16, rows=2, dotsize=8)
        self.lcd.clear()
        
    def afficher(self,message):
        """
        Affiche un message sur un LCD.
        
        Arguments:
        - message: le message à afficher sur le LCD.
        """
        self.lcd.clear()
        self.lcd.write_string(message)
        
    def effacer(self):
        """
        Efface l'affichage.
        """
        self.lcd.clear()


class Buzzer:
    """
    Classe pour l'utilisation d'un buzzer.
    
    Branchement:
    
    +   : VCC 5V
    -   : GND
    SIG : PORT GPIO
    NCC : /
    
    Exemple d'utilisation:
    buzzer = Buzzer(17)  # Connexion au port GPIO 17
    buzzer.play(440)  # Joue un La (440 Hz)
    buzzer.stop()    # Stop le son
    buzzer.cleanup() # Libération des ressouces du GPIO
    
    """
    def __init__(self, pin):
        """
        Initialisation du buzzer sur un GPIO donné
        
        Arguments:
        - pin: Le pin GPIO où communique le buzzer.
        """
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 440)  # Fréquence par défaut 440 Hz
        self.pwm.start(0)  # Duty cycle à 0 pour ne pas faire de bruit au démarrage

    def play(self, frequency):
        """
        Joue un son à une fréquence donnée (Hz)
        
        Arguments:
        - frequency : la fréquence de l'audio à jouer (en Hz)
        """
        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(30)

    def stop(self):
        """
        Arrête le son 
        """
        self.pwm.stop()

    def cleanup(self):
        """Libère les ressources du GPIO"""
        self.pwm.stop()
        GPIO.cleanup()

class Button:
    """
    Classe pour l'utilisation d'un bouton actionneur. L'utilisation du bouton
    se fait grâce à une fonction callback 
    
    Branchement:
    
    +   : VCC 3.3V
    -   : GND
    S : PORT GPIO
    
    Exemple d'utilisation:
    button = Button(17)  # Connexion au port GPIO 17
    def on_button_press(): # Création d'une fonction callback
        print("Bouton pressé !")
    button.on_press(on_button_press) # Définition d'un listener (on_press), qui lorsqu'activé, 
                                     # exécute une fonction callback (on_button_press)
    
    button.cleanup() # Libère les ressources
    
    """
    def __init__(self, pin, debounce_time=0.05):
        """
        Initialisation du bouton sur un GPIO donné
        
        Arguments:
        - pin: Le pin GPIO où communique le bouton.
        - debounce_time: Le temps de rebond (en secondes)
        """
        self.pin = pin
        self.debounce_time = debounce_time
        self.last_pressed = 0
        self.callback = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Détection d'interruption sur appui
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self._handle_press, bouncetime=int(self.debounce_time * 1000))

    def _handle_press(self):
        """ Méthode interne appelée lorsque le bouton est pressé."""
        current_time = time.time()
        if current_time - self.last_pressed > self.debounce_time:
            self.last_pressed = current_time
            if self.callback:
                self.callback()

    def on_press(self, callback):
        """
        Définit une fonction callback appelée lorsque le bouton est pressé.
        
        Arguments:
        - callback: Fonction à exécuter sur pression du bouton.
        """
        self.callback = callback

    def is_pressed(self):
        """ Vérifie si le bouton est actuellement pressé."""
        return GPIO.input(self.pin) == GPIO.LOW

    def cleanup(self):
        """ Nettoie les ressources GPIO."""
        GPIO.cleanup(self.pin)
        
class LED:
    """
    Classe pour l'utilisation d'une LED 
    
    Branchement:
    
    +   : PORT GPIO
    -   : GND
    N : /
    
    Exemple d'utilisation:
    led = LED(17)  # Connexion au port GPIO 17
    led.on() # Allume la LED
    time.sleep(1)
    led.off() # Eteint la LED
    led.toggle() # Inverse l'état de la LED et donc l'allume
    led.toggle() # Inverse l'état de la LED et donc l'éteint
    led.cleanup() # Libère les ressources
    
    """
    def __init__(self, pin):
        """
        Initialise le module LED Adeept.
        
        Arguments:
        - pin: Numéro du GPIO auquel la LED est connectée.
        """
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.state = False  # État initial de la LED (éteinte)

    def on(self):
        """Allume la LED."""
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        """Éteint la LED."""
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def toggle(self):
        """Inverse l'état de la LED."""
        if self.state:
            self.off()
        else:
            self.on()
    
    def is_on(self):
        """Retourne True si la LED est allumée, False sinon."""
        return self.state
    
    def cleanup(self):
        """Nettoie les ressources GPIO."""
        GPIO.cleanup(self.pin)
        
       
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
                data.append([timestamp, lat, lon])

    # Convertir en DataFrame
    df = pd.DataFrame(data, columns=["UTC", "Latitude", "Longitude"])

    # Enregistrer en fichier CSV
    df.to_csv(csv_file, index=False)
    print(f"Conversion terminée ! Fichier enregistré : {csv_file}")
