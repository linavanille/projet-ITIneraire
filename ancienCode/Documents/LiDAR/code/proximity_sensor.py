from utils import Buzzer
from lidar import LIDAR, PORT_LIDAR, MIN_RANGE, MAX_RANGE

# A COMPLETER
MIN_ANGLE=80
MAX_ANGLE=90
QUALITY_THRESHOLD=14
DISTANCE_THRESHOLD=200

if __name__ == '__main__':
   
    # Initialisation du LiDAR
    print("Connexion au LiDAR...")
    lidar = LIDAR(PORT_LIDAR,
                  quality_threshold=QUALITY_THRESHOLD,
                  min_range=MIN_RANGE,
                  max_range=MAX_RANGE,
                  min_angle=MIN_ANGLE,
                  max_angle=MAX_ANGLE)
    
    print("Démarrage du LiDAR...")
    lidar.start()
    
    # Détection de proximité dans l'intervalle d'angle [MIN_ANGLE,MAX_ANGLE]
    # Le buzzer du détecteur sonnera lorsque une estimation de mesureest inférieure ou égale à DISTANCE_THRESHOLD
    try:
        lidar.proximity_sensor(DISTANCE_THRESHOLD)
        
    except KeyboardInterrupt:
        print("Arrêt du scan par l'utilisateur.")
        buzz = Buzzer(24)
        buzz.stop()

    finally:
        print("Arrêt du LiDAR...")
        lidar.stop()