from lidar import LIDAR, PORT_LIDAR, MIN_RANGE, MAX_RANGE
from ..utils import CSVHandler
import argparse

# A COMPLETER
MIN_ANGLE=...
MAX_ANGLE=...
QUALITY_THRESHOLD=...

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--save-path', '-s',
                        type=str,
                        default=None,
                        help="Chemin où sauvegarder les données.")
    args = parser.parse_args()

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
    
    # Scan en continu et affichage dynamique des mesures
    try:
        lidar.get_stream_scan(args.save_path)
        
    except KeyboardInterrupt:
        print("Arrêt du scan par l'utilisateur.")

    finally:
        print("Arrêt du LiDAR...")
        lidar.stop()