#!/usr/bin/env python 3 
""" Module de récupération des mesures"""

import numpy as np
# from IMU import read_IMU
# import GPS.gnss
import logging

LOG = logging.getLogger()

class Mesures ():
    def __init__(self, range_acc=8, range_gyro=1000, correction=False):
        """Initialise le regroupement des données des capteurs"""
        self._data_imu = None
        if not correction:
            self._data_gnss = read_IMU(range_acc, range_gyro)

    @property
    def gnss(self):
        """Renvoie la position en DMM et l'altitude"""
        latitude = self.data_gnss.latitude.coords_DMM
        longitude = self.data_gnss.longitude.coords_DMM
        altitude = self.data_gnss.altitude
        return np.array([latitude, longitude, altitude])

    @property
    def imu(self):
        return self._rotation(self._data_imu)

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
        return np.array([x, y, z])@Rx@Ry@Rz

if __name__ == "__main__":
    pass