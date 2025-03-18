import time
from IMU import read_IMU, initialize_sensors
from evdev import UInput, ecodes as e

sensi = 0.2

ui = UInput()

def send_key(key, press_or_release=0):
    """
    Envoie au système une instruction sur une touche clavier (pressée ou relachée)
    
    Arguments: 
    - key: La touche à controller
    - press_or_release: L'état de la touche à controller:
            - press_or_release=0 => release
            - press_or_release=1 => press
    """
    ui.write(e.EV_KEY, key, press_or_release)
    ui.syn()


def game_controller():
    """
    Permet de controller les touches directionnelles du clavier en fonction de l'inclinaison de l'IMU.
    """
    
    # Paramètres configurables
    # A COMPLETER
    accel_range = 4
    accel_freq = 26
    gyro_range = 1000
    gyro_freq = 12.5

    # Initialisation des capteurs
    initialize_sensors(accel_range, accel_freq, gyro_range, gyro_freq)

    try:
        while True:

            # Lecture des données
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = read_IMU(accel_range, gyro_range)

            # A COMPLETER
            if accel_z > sensi:
                print("UP")
                send_key(e.KEY_UP, 1)
            else:
                send_key(e.KEY_UP, 0)
            
            if accel_z < -sensi:
                print("DOWN")
                send_key(e.KEY_DOWN, 1)
            else:
                send_key(e.KEY_DOWN, 0)
                
            if accel_y < -sensi:
                print("LEFT")
                send_key(e.KEY_LEFT, 1)
            else:
                send_key(e.KEY_LEFT, 0)
            
            if accel_y > sensi:
                print("RIGHT")
                send_key(e.KEY_RIGHT, 1)
            else:
                send_key(e.KEY_RIGHT, 0)
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Arrêt du programme.")
    
if __name__ == "__main__":
    game_controller()
