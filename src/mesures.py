#!/usr/bin/env python 3 
""" Module de récupération des mesures"""

import numpy as np

from datetime import datetime as dt
import GPS.gnss as gs
from IMU import read_IMU
from GPS.get_distance import compute_distance

GNSS_DEVICE_ADDR = 0x20

class Mesures ():
    """Classe permettant de récupérer / traiter les données acquises par la RPi"""

    def __init__(self, range_acc=8, range_gyro=1000, correction=False):
        """Initialise le regroupement des données des capteurs"""
        self._range_acc = range_acc
        self._range_gyro = range_gyro
        mode = gs.GPS_BEIDOU_GLONASS
        self._data_gnss = gs.GNSS(1, GNSS_DEVICE_ADDR)
        self._data_gnss.initialisation(mode)
        self._origine = self.gnss

    @property
    def origine(self):
        """Renvoie le tout premier point de l'acquisition"""
        return self._origine

    @property
    def gnss(self):
        """Renvoie la position en DMM et l'altitude"""
        self._data_gnss.update()
        
        latitude = self._data_gnss.latitude.coords_DD
        longitude = self._data_gnss.longitude.coords_DD
        altitude = self._data_gnss.altitude

        return np.array([longitude, latitude, altitude])

    def getutc(self):
        return self._data_gnss.utc

    @property
    def imu(self):
        self._data_imu = read_IMU(self._range_acc, self._range_gyro)
        return Mesures._rotation(*self._data_imu)

    def _rotation(x, y, z, theta, phi, psi):
        """Applique une matrice de rotation sur les accélérations"""
        Rx = np.array([[1,             0,              0],
                       [0, np.cos(theta), -np.sin(theta)],
                       [0, np.sin(theta),  np.cos(theta)],
                      ])
        Ry = np.array([[np.cos(phi),  0, np.sin(phi)],
                       [0,            1,           0],
                       [-np.sin(phi), 0, np.cos(phi)]
                      ])
        Rz = np.array([[np.cos(psi), -np.sin(psi), 0],
                       [np.sin(psi),  np.cos(psi), 0],
                       [0,              0,         1]
                      ])
        return np.array([x, y, z])@Rz@Rx@Ry

    def distance_a_lorigine(self, y2:np.array)->np.array:
        """
        Calcule la distance de deux points GPS projetés sur un plan 2D.

        Utilisation de la formule de distance entre deux points sur Terre en posant 
        d'abord phi_1 = phi_2 puis theta_1 = theta_2.
        """
        y1 = self.origine
        #Rayon de la Terre
        R = 6731
        return R*np.array([180/np.pi*np.acos(np.sin(y1[1])**2+np.cos(y1[0]-y2[0])*np.cos(y1[1])**2),
                           180/np.pi*np.acos(np.sin(y1[1])*np.sin(y2[1])+np.cos(y1[1])*np.cos(y2[1])),
                           y2[2]
                          ])

if __name__ == "__main__":
    # main = Mesures()
    # print(main.gnss)
    # print("-"*15)
    # print(read_IMU(8, 1000)[:3])
    # print(main.imu)
    # time.sleep(2)
    pass