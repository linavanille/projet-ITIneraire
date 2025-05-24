#!/usr/bin/env python 3
""" Module d'implémentation du filtre de Kalman"""

import numpy as np
import pandas as pd
import logging
from utils2 import CSVHandler

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
        self.F = nouveau

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
        self.Q = nouveau

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("R doit être un np.array")
        self.R = nouveau

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

class KalmanException (Exception):
    pass

class DimensionsNonConformesException (KalmanException):
    pass

class ParametreNonDefiniException (KalmanException):
    pass

def filtrage_csv(source:str, csv_out:str, filtre:FiltreKalman)->None:
    """Filtre les données d'un csv et les écrits dans un nouveau csv"""

    # def F(dt:float, n:int=6):
    #     """Definition dynamique de la matrice F"""
    #     F_dt = np.eye(n)
    #     F_dt [0:n//2, n//2:]  = dt*np.eye(n//2)
    #     return F_dt

    # Préparation des fichiers
    df = pd.read_csv(source)

    if not(csv_out.endswith('.csv')):
        csv_out +='.csv'

    record = CSVHandler(csv_out)
    record.create_csv_with_header(['UTC','Latitude','Longitude', 'Altitude'])

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

if __name__ == "__main__":
    F = np.eye(6)
    F [0:3, 3:]  = np.eye(3)
    H = np.block([np.eye(3), np.zeros((3, 3))])
    G = np.block([[(1/2)**2*np.eye(3)],[np.eye(3)]])
    print("initialisation")
    print(G.shape)
    filtre = FiltreKalman(F, H, G, Q=np.zeros((6, 6)))

    print("filtrage")
    filtrage_csv("./output/gnss_acq.csv", "testFiltrage.csv", filtre)

    print("Fin du filtrage")