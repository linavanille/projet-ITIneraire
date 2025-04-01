import RPi.GPIO as GPIO
import time
import sys
import RPLCD
from get_position import get_position
import argparse
import time


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

    def _handle_press(self, channel):
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
        
def acquisitions():
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



if __name__ == "__main__":
    def on_button_press(): # Création d'une fonction callback
        get_position(no_LCD=True)
        
    #def stop( bouton): # Création d'une fonction callback
        #button.cleanup()
        #exit()
        
    button = Button(17) 
    

    button.on_press(on_button_press) 
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        button.cleanup()
