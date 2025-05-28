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

    def __init__(self, range_acc=8, range_gyro=1000, correction=False)->None:
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
    def gnss(self)->np.array:
        """Renvoie la position en DMM et l'altitude"""
        self._data_gnss.update()

        latitude = self._data_gnss.latitude.coords_DD
        longitude = self._data_gnss.longitude.coords_DD
        altitude = self._data_gnss.altitude

        return np.array([longitude, latitude, altitude])

    def get_utc(self):
        return self.to_cartesien(*self._data_gnss.utc)

    @property
    def imu(self)->np.array:
        self._data_imu = read_IMU(self._range_acc, self._range_gyro)
        return Mesures._rotation(*self._data_imu)

    def _rotation(x, y, z, theta, phi, psi)->np.array:
        """Applique une matrice de rotation sur les accélérations"""

        theta, phi, psi = np.pi/180*theta, np.pi/180*phi, np.pi/180*psi
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
        return Rx@Ry@Rz@np.array([x, y, z])

    def to_cartesien(theta:float, phi:float, alt:float, R:int=6356752)->np.array:
        """Conversion du repère shérique au cartésien"""

        theta, phi = m.radians(theta), m.radians(phi)
        return np.array([(R + alt) * np.sin(theta) * np.cos(phi),
                        (R + alt) * np.sin(theta) * np.sin(phi),
                        (R + alt) * np.cos(theta) ])

    def to_spherique(x:float, y:float, z:float)->np.array:
        """Conversion du repère cartésien au sphérique"""
        R = 6356752
        alt = np.sqrt(x**2 + y**2 + z**2) - R
        return np.array([m.degrees(m.acos(z/R)),
                        m.degrees(m.atan(y/x)),
                        alt])

if __name__ == "__main__":
    # main = Mesures()
    # print(main.gnss)
    # print("-"*15)
    # print(read_IMU(8, 1000)[:3])
    # print(main.imu)
    # time.sleep(2)
    # Mesures._rotation(0, 0, -9.81, 30, 45, 0)
    pass