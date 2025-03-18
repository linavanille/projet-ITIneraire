import math
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar
import time
from ..utils import CSVHandler, Buzzer

# A COMPLETER
PORT_LIDAR = ...                 # Port USB connecté au LiDAR
PORT_BUZZER = ...                # Port GPIO du buzzer
MIN_RANGE = ...                  # Portée minimale du LiDAR en mm
MAX_RANGE = ...                  # Portée maximale du LiDAR en mm

SCAN_SKIP = 3                    # Ignorer X scans pour alléger l'affichage
LEN_PREVIOUS_SCANS = 3

class LIDAR():
    def __init__(self, port_name, 
                 min_range=MIN_RANGE, 
                 max_range=MAX_RANGE, 
                 quality_threshold=0,
                 min_angle=0,
                 max_angle=360):
        """
        Initialise la classe LIDAR et configure les paramètres de mesure.

        Arguments:
        - port_name: nom du port série où est connecté le LiDAR
        - min_range: portée minimale en mm
        - max_range: portée maximale en mm
        - quality_threshold: seuil de qualité pour filtrer les mesures
        - min_angle: angle minimal pour filtrer les mesures (en degrés)
        - max_angle: angle maximal pour filtrer les mesures (en degrés)
        """
        self.lidar = RPLidar(port_name)
        self.quality_threshold = quality_threshold
        self.min_range = min_range
        self.max_range = max_range
        self.min_angle = min_angle
        self.max_angle = max_angle

        self.current_scan = None
        self.timestamp_scan = None
        self.x_points = []
        self.y_points = []

    def get_timestamp(self):
        """
        Retourne le timestamp du dernier scan effectué
        """
        return self.timestamp_scan

    def get_current_scan(self):
        """
        Retourne le dernier scan effectué
        """
        return self.current_scan
    
    def get_xy_points(self):
        """
        Retourne les points mesurés du dernier scan effectué dans un format cartésien (LiDAR aux coordonnées 0,0)
        """
        return [[x,y] for x,y in zip(self.x_points,self.y_points)]
        
    def print_current_scan(self):
        """
        Affiche proprement les mesures du dernier scan
        """
        print("Mesures :")
        for m in self.current_scan:
            print(m)
        print(f"Le scan courant contient {len(self.current_scan)} mesures")

    def print_xy_points(self):
        """
        Affiche proprement les mesures sous format cartésien
        """
        print("\nCoordonnées des points dans le plan cartésien: ")
        for x,y in zip(self.x_points,self.y_points):
            print(f"({x},{y})")

    def start(self):
        """
        Démarre le LiDAR en activant son moteur.
        """
        self.lidar.start_motor()

    def stop(self):
        """
        Arrête le LiDAR, son moteur et déconnecte la connexion série.
        """
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

    def filter_low_quality_pts(self):
        """
        Filtre les points de la mesure actuelle en ne conservant que ceux dont la qualité dépasse le seuil défini.
        """
        # A COMPLETER
        pass

    def filter_angle(self):
        """
        Filtre les points de la mesure actuelle en fonction de la plage d'angle définie.
        """
        # A COMPLETER
        pass

    def polar_to_cartesian(self):
        """
        Convertit les coordonnées polaires (angle, distance) en coordonnées cartésiennes (x, y).
        """
        # A COMPLETER
        # Les informations du scans sont dans l'objet self.current_scan
        pass

    def get_single_scan(self):
        """
        Acquiert un scan complet après avoir ignoré les premiers scans pour stabiliser la mesure.
        """

        self.lidar.clean_input()

        # Afin d'avoir un scan complet à 360°, on laisse le LiDAR faire quelques premiers scans avant d'en sélectionner un
        i = 0
        for scan in self.lidar.iter_scans():
            if i > 2:
                break
            i += 1
        self.timestamp_scan = time.time()
        self.current_scan = scan

    def plot_single_scan(self):
        """
        Affiche le nuage de points 2D de la dernière mesure, avec les cercles indiquant les portées minimale et maximale.
        """
        
        # Création de la figure Matplotlib pour l'affichage des points en BEV
        plt.figure(figsize=(8, 8))
        
        # Tracé des points mesurés en BEV
        plt.scatter(self.x_points, self.y_points, s=5, c="blue", alpha=0.6, label="Points mesurés")

        # Tracé de la position du LiDAR en 0,0
        plt.scatter(0, 0, c="red", marker="x", label="LiDAR")  # Position du LiDAR (0,0)

        # Tracé des portées maximale et minimale du LiDAR
        circle_max = plt.Circle((0, 0), self.max_range, color='orange', fill=False, linestyle='--', label="Portée maximale")
        circle_min = plt.Circle((0, 0), self.min_range, color='green', fill=False, linestyle='--', label="Portée minimale")
        plt.gca().add_patch(circle_min)
        plt.gca().add_patch(circle_max)

        # Définition de la vue de la figure (max et min)
        plt.xlim(-self.max_range - 200, self.max_range + 200)
        plt.ylim(-self.max_range - 200, self.max_range + 200)

        # Labellisation de la figure
        plt.xlabel("Position X (mm)")
        plt.ylabel("Position Y (mm)")
        plt.title("Nuage de points LiDAR - Vue de dessus (BEV)")
        plt.axis("equal")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.show()

    def get_stream_scan(self,save_path=None):
        """
        Lance un scan continu et met à jour dynamiquement l'affichage du nuage de points en temps réel.
 
         Arguments:
        - save_path: Le chemin de sauvegarde du fichier CSV (None par défaut signifie aucun enregistrement)
        """
        self.lidar.clean_input()

        # Enregistrement des données dans un fichier CSV (si un chemin de sauvegarde est précisé)
        if save_path:
            csv_file = CSVHandler(save_path)
            csv_file.create_csv_with_header(['Timestamp','Measurements','XY_points'])

        # Création de la figure Matplotlib pour l'affichage des points en BEV
        fig, ax = plt.subplots(figsize=(8, 8))

        # Définition de la vue de la figure (max et min)
        ax.set_xlim(-self.max_range, self.max_range)
        ax.set_ylim(-self.max_range, self.max_range)

        # Labellisation de la figure
        ax.set_xlabel("Position X (mm)")
        ax.set_ylabel("Position Y (mm)")
        ax.set_title("Scan LiDAR en temps réel")
        ax.set_aspect('equal')
        ax.grid(True, linestyle="--", alpha=0.5)

        # Tracé des portées maximale et minimale du LiDAR
        circle_max = plt.Circle((0, 0), self.max_range, color='orange', fill=False, linestyle='--', label="Portée maximale")
        circle_min = plt.Circle((0, 0), self.min_range, color='green', fill=False, linestyle='--', label="Portée minimale")
        plt.gca().add_patch(circle_min)
        plt.gca().add_patch(circle_max)

        # Tracé de la position du LiDAR en 0,0
        ax.scatter(0, 0, c="red", marker="x", label="LiDAR")
        
        # Tracé des points mesurés en BEV
        scatter = ax.scatter([], [], s=5, c="blue", alpha=0.6)

        plt.legend()
        plt.ion()
        plt.show()

        scan_counter = 0

        try:
            for scan in self.lidar.iter_scans():

                # Mise à jour du timestamp du dernier scan
                self.timestamp_scan = time.time()

                # Afin d'éviter de surcharger le buffer du LiDAR, on ne sélectionne qu'un scan tous les #SCAN_SKIP# scans.
                scan_counter += 1
                if scan_counter % SCAN_SKIP != 0:
                    continue

                # Mise à jour du scan
                self.current_scan = scan

                if not self.current_scan or len(self.current_scan) == 0:
                    continue
                
                # Traitement du scan
                self.filter_low_quality_pts()
                self.filter_angle()
                self.polar_to_cartesian()
                
                # Enregistrement des données dans le fichier CSV
                if save_path:  
                    csv_file.append_row([self.get_timestamp(),self.get_current_scan(),self.get_xy_points()])
                
                # Mise à jour des points sur la figure
                scatter.set_offsets(np.c_[self.x_points, self.y_points])
                plt.pause(0.01)

                self.lidar.clean_input()
        except KeyboardInterrupt:
            print("Scan interrompu par l'utilisateur.")
        finally:
            plt.ioff()
            plt.close()


    def stream_distance(self,save_path=None):
        """
        Mesure et affiche continuellement la distance moyenne dans la plage d'angle définie.
        
        Arguments:
        - save_path: Le chemin de sauvegarde du fichier CSV (None par défaut signifie aucun enregistrement)
        """

        print("Mesure continue de la distance dans la plage angulaire de {}° à {}°.".format(self.min_angle, self.max_angle))

        # Enregistrement des données dans un fichier CSV (si un chemin de sauvegarde est précisé)
        if save_path:
            csv_file = CSVHandler(save_path)
            csv_file.create_csv_with_header(['Timestamp','Mean Distance','STD Distance'])
        
        scan_counter = 0

        for scan in self.lidar.iter_scans():
            # Mise à jour du timestamp du dernier scan
            self.timestamp_scan = time.time()

            # Afin d'éviter de surcharger le buffer du LiDAR, on ne sélectionne qu'un scan tous les #SCAN_SKIP# scans.
            scan_counter += 1
            if scan_counter % SCAN_SKIP != 0:
                continue

            # Mise à jour du scan
            self.current_scan = scan

            if not self.current_scan or len(self.current_scan) == 0:
                continue

            # Traitement du scan
            self.filter_low_quality_pts()
            self.filter_angle()

            # A MODIFIER
            # Extraction des distances estimées
            distances = []
            
            # A MODIFIER
            # Calcul de la moyenne et de l'écart-type des distances extraites
            average_distance = 0
            std_distance = 0
                
            print(f"Nombre de points: {len(distances)} - Distance moyenne: {average_distance:8.2f} mm - Ecart-type: {std_distance:8.2f} mm", end="\r", flush=True)
            
            # Enregistrement des données dans le fichier CSV
            if save_path:  
                csv_file.append_row([self.get_timestamp(),average_distance,std_distance])
       
    def proximity_sensor(self,distance_threshold=MAX_RANGE):
        # A COMPLETER
        # Fonction de détection de proximité
        while True:
            pass
    
    def motion_sensor(self,distance_threshold=MAX_RANGE):
        # A COMPLETER
        # Fonction de détection de mouvement
        while True:
            pass    
        