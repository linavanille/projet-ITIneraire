#!/usr/bin/env python 3
""" Module d'implémentation du filtre de Kalman"""

import numpy as np
import math  as m
import datetime
import pandas as pd
import logging

from .mesures import Mesures
from .filtre_date import conversion
from .utils2 import CSVHandler, calcul_R, calcul_Q

LOG = logging.getLogger()

class FiltreKalman ():

    def __init__(self, F, H ,G=None, Q=None, R=None):
        if not isinstance(F,np.ndarray) :
            raise TypeError("F doit être un np Array")
        self._F = F
        self.__n, self.__p = np.shape(F)
        if not isinstance(H, np.ndarray) :
            raise TypeError("H doit être un np Array")
        if self.__p != np.shape(H)[1] :
            raise DimensionsNonConformesException(f"dimension de H {np.shape(H)} attendue {self.__n ,self.__p}")
        self._H = H

        self._G = G

        if Q is None :
            self._Q = np.eye(self.__p)
        else :
            self._Q = Q

        if R is None :
            self._R = np.eye(np.shape(H)[0])
        else:
            self._R = R

        self._P = np.eye((self.__n))

        self._x = None
        self._K = None

    def __para_pas_set(self):
        return None in (self.x, self.F, self.G, self.H, self.Q, self.R)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("u doit être un ndarray")
        self._x = nouveau

    @property
    def G(self):
        return self._G

    @G.setter
    def G(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("G doit être un ndarray")
        self._G = nouveau

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("F doit être un ndarray")
        self._F = nouveau

    @property
    def H(self):
        return self._H

    @H.setter
    def H(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("H doit être un np.array")
        self.H = nouveau

    @property
    def Q(self):
        return self._Q

    @Q.setter
    def Q(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("Q doit être un np.array")
        self._Q = nouveau

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("R doit être un np.array")
        self._R = nouveau

    @property
    def P(self):
        return self._P

    @property
    def K(self):
        return self._K

    def __call__(self, u_mesures, y_observations=None):
        if not isinstance(u_mesures, np.ndarray):
            raise TypeError("u doit être un np.array")
        if u_mesures.shape[0] != self.G.shape[1]:
            raise DimensionsNonConformesException(f"obtenues : {u_mesures.shape} attendues : {self.G.shape[1], 1}")

        self.__prediction_x(u_mesures)
        self.__prediction_P()

        if y_observations is not None:
        # print("Correction")
            self.__correction_K()
            self.__correction_x(y_observations)
            self.__correction_P()
        return self.x


    def __prediction_x(self, u):
        self.x = self.F@self.x+self.G@u

    def __prediction_P(self):
        self._P = self.F@self.P@self.F.T+self.Q

    def __correction_K(self):
        self._K = self.P@self.H.T@np.linalg.inv(self.H@self.P@self.H.T + self.R)

    def __correction_x(self, y):
        self.x = self.x + self.K@(y-self.H@self.x)

    def __correction_P(self):
        self._P = (np.eye(self.K.shape[0])-self.K@self.H)@self.P

def F(dt:float, n:int=6):
    """Definition dynamique de la matrice F"""
    F_dt = np.eye(n)
    F_dt [0:n//2, n//2:]  = dt*np.eye(n//2)
    return F_dt

def G(dt:float, n:int=3):
    """Definition dynamique de la matrice G"""
    g = np.block([[1/2*dt**2*np.eye(n)],
                    [dt*np.eye(n)]
                    ])
    return g

class KalmanException (Exception):
    pass

class DimensionsNonConformesException (KalmanException):
    pass

class ParametreNonDefiniException (KalmanException):
    pass

def initialisation_des_csv(source_gnss:str,
                            csv_out:str,
                            source_imu:str="")->(pd.DataFrame, pd.DataFrame, CSVHandler):
    """
    Preparation des fichiers csv d'entrée et de sortie
    - rajoute extensions si besoin
    - renvoie:
        Les data Frame des fichiers source et le CSVHandler de la destination
    """

    if not(source_gnss.endswith('.csv')):
        source_gnss +='.csv'
    df_gnss = pd.read_csv(source_gnss)

    if not(source_imu.endswith('.csv')):
        source_imu +='.csv'
    try:
        df_imu = pd.read_csv(source_imu)
    except FileNotFoundError:
        df_imu = None

    if not(csv_out.endswith('.csv')):
        csv_out +='.csv'
    record = CSVHandler(csv_out)
    record.create_csv_with_header(['UTC','Latitude','Longitude', 'Altitude'])

    return df_gnss, df_imu, record

def filtrage_csv(source:str, csv_out:str, filtre:FiltreKalman)->None:
    """Filtre les données d'un csv et les écrits dans un nouveau csv"""

    df, _, record = initialisation_des_csv(source, csv_out)

    filtre.x = np.array([df['Latitude'][0],
                      df['Longitude'][0],
                      df['Altitude'][0],
                      0, 0, 0 ])

    for i in range (df.shape[0]):
        y = np.array([df['Latitude'][i],
                      df['Longitude'][i],
                      df['Altitude'][i]
                     ])
        filtre(np.zeros(3), y)
        record.append_row([df['UTC'][i] ,filtre.x[0], filtre.x[1], filtre.x[2]])

def filtrage_cartesien(source:str, csv_out:str, filtre:FiltreKalman)->None:
    """Filtre les données en coordonnées cartésiennes
    d'un csv et les écrits dans un nouveau csv en coordonnées sphériques"""

    df, _, record = initialisation_des_csv(source, csv_out)

    # initialisation du premier x du filtre
    filtre.x = np.block([Mesures.to_cartesien(df['Latitude'][0],
                                              df['Longitude'][0],
                                              df['Altitude'][0]),
                                              0, 0, 0 ])

    for i in range (df.shape[0]):
        y = Mesures.to_cartesien(df['Latitude'][i],
                                 df['Longitude'][i],
                                 df['Altitude'][i])

        filtre(np.zeros(3), y)
        X = Mesures.to_spherique(*filtre.x[:3])
        record.append_row([df['UTC'][i] ,X[0]+0.000547, X[1], X[2]])

def filtrage_prediction(source_imu:str, source_gnss:str, csv_out:str, filtre:FiltreKalman)->None:
    """Filtre les données d'un csv en prenant en compte les données de l'imu. Les écrit dans un nouveau csv"""

    def dt(i:int)->float:
        """calcule le temps entre 2 acquisitions"""
        if i>0:
            s_1 = eval(df_imu['Timestamp'][i]).second
            ms_1 = eval(df_imu['Timestamp'][i]).microsecond*1e-6
            s_0 = eval(df_imu['Timestamp'][i-1]).second
            ms_0 = eval(df_imu['Timestamp'][i-1]).microsecond*1e-6
        return (s_1 + ms_1) - (s_0 + ms_0)

    # filtre.R = calcul_R(source_gnss + ".csv")
    # filtre.Q = calcul_Q(source_imu + ".csv")*10

    df_gnss, df_imu, record = initialisation_des_csv(source_gnss, csv_out, source_imu)

    #Conversion du format du timestamp
    conversion(df_gnss)

    #initialisation du premier x du filtre
    filtre.x = np.block([Mesures.to_cartesien(df_gnss['Latitude'][0],
                                              df_gnss['Longitude'][0],
                                              df_gnss['Altitude'][0]),
                                              0, 0, 0 ])

    j = 1
    i = 1
    while j<df_gnss.shape[0]:
        u = Mesures.rotation(df_imu['Accel X'][i],
                             df_imu['Accel Y'][i],
                             df_imu['Accel Z'][i],
                             df_imu['Gyro X'][i],
                             df_imu['Gyro Y'][i],
                             df_imu['Gyro Z'][i],)
        # u[2] -= err

        while (eval(df_imu['Timestamp'][i]) < df_gnss['Date_Formatee'][j]) and i<df_imu.shape[0]:
            filtre.F = F(dt(i))
            filtre.G = G(dt(i))
            filtre(u)
            i = i+1
            u = Mesures.rotation(df_imu['Accel X'][i],
                                 df_imu['Accel Y'][i],
                                 df_imu['Accel Z'][i],
                                 df_imu['Gyro X'][i],
                                 df_imu['Gyro Y'][i],
                                 df_imu['Gyro Z'][i],)
            # u[2] -= err
        filtre.F = F(dt(i))
        filtre.G = G(dt(i))
        y = Mesures.to_cartesien(df_gnss['Latitude'][j],
                                 df_gnss['Longitude'][j],
                                 df_gnss['Altitude'][j])
        filtre(u, y)

        X = Mesures.to_spherique(*filtre.x[:3])
        record.append_row([df_gnss['Date_Formatee'][j] ,X[0]+0.000547, X[1], X[2]])
        i = i+1
        j += 1

if __name__ == "__main__":
    pass