from lidar import LIDAR, PORT_LIDAR, MIN_RANGE, MAX_RANGE
import argparse
from ..utils import CSVHandler

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

    # Préparation du fichier CSV (si un chemin de sauvegarde est précisé)
    if args.save_path:
        csv_file = CSVHandler(args.save_path)
        csv_file.create_csv_with_header(['Timestamp','Measurements','XY_points'])

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
    
    # Scan unique à 360°
    lidar.get_single_scan()
    
    # Affichage des mesures
    lidar.print_current_scan()

    # Filtrage des points de mauvaise qualité
    lidar.filter_low_quality_pts()
    
    # Filtrage des points pour sélectionner uniquement ceux dans un intervalle angulaire précisé
    lidar.filter_angle()
    
    # Transformation des points pour le replacer dans un plan cartésien
    lidar.polar_to_cartesian()
    
    # Affichage des coordonnées des points dans le plan cartésien
    lidar.print_xy_points()

    # Enregistrement des données dans le fichier CSV
    if args.save_path:  
        csv_file.append_row([lidar.get_timestamp(),lidar.get_current_scan(),lidar.get_xy_points()])
        
    # Affichage des points mesurés dans un plan cartésien
    #lidar.plot_single_scan()
    
    # Arrêt du LiDAR
    print("Arrêt du LiDAR...")
    lidar.stop()