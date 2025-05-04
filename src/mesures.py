#!/usr/bin/env python 3 
""" Module de récupération des mesures"""

import numpy as np
from IMU.IMU import read_IMU
import GPS.gnss as gs
import time
from datetime import datetime as dt

GNSS_DEVICE_ADDR = 0x20

class Mesures ():
    def __init__(self, range_acc=8, range_gyro=1000, correction=False):
        """Initialise le regroupement des données des capteurs"""
        self._data_imu = read_IMU(range_acc, range_gyro)
        self._range_acc = range_acc
        self._range_gyro = range_gyro
        mode = gs.GPS_BEIDOU_GLONASS
        self._data_gnss = gs.GNSS(1, GNSS_DEVICE_ADDR)
        self._data_gnss.initialisation(mode)

    @property
    def gnss(self):
        """Renvoie la position en DMM et l'altitude"""
        self._data_gnss.update()
        
        latitude = self._data_gnss.latitude.coords_DMM
        longitude = self._data_gnss.longitude.coords_DMM
        altitude = self._data_gnss.altitude
        return np.array([latitude, longitude, altitude])

    @property
    def imu(self):
        self._data_imu = read_IMU(self._range_acc, self._range_gyro)
        return Mesures._rotation(*self._data_imu), dt.now()

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

if __name__ == "__main__":
    main = Mesures()
    print(main.gnss)
    print("-"*15)
    print(read_IMU(8, 1000)[:3])
    print(main.imu)
    time.sleep(2)
    pass