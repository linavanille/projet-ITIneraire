import RPi.GPIO as GPIO
import time
import os
import csv

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
        """Initialisation du buzzer sur un GPIO donné"""
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 440)  # Fréquence par défaut 440 Hz
        self.pwm.start(0)  # Duty cycle à 0 pour ne pas faire de bruit au démarrage

    def play(self, frequency):
        """
        Joue un son à une fréquence donnée (Hz)
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


class CSVHandler:
    """
    Classe pour la création et l'écriture d'un fichier CSV pour l'enregistrement des données LiDAR.
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