from lidar import LIDAR, PORT_LIDAR, MIN_RANGE, MAX_RANGE

# A COMPLETER
MIN_ANGLE=...
MAX_ANGLE=...
QUALITY_THRESHOLD=...
DISTANCE_THRESHOLD=...

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
    
    # Détection de mouvements dans l'intervalle d'angle [MIN_ANGLE,MAX_ANGLE]
    # Le buzzer du détecteur sonnera lorsque des modifications significatives seront détectées à une distance inférieure ou égale à DISTANCE_THRESHOLD
    try:
        lidar.motion_sensor(DISTANCE_THRESHOLD)
        
    except KeyboardInterrupt:
        print("Arrêt du scan par l'utilisateur.")

    finally:
        print("Arrêt du LiDAR...")
        lidar.stop()