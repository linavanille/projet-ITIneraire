#!/usr/bin/env python 3 
""" Module d'implémentation du filtre de Kalman"""

import numpy as np
import logging

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
            raise DimensionsNonConformesException(f"dimension de H {np.shape(H)} attendue {n ,self.__p}")
        self._H = H

        self._G = G

        if Q is None :
            self._Q = np.eye(self.__p)
        else :
            self._Q = Q

        if R is None :
            self._R = np.eye(self.__p)
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
        return self._x

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
            raise TypeError("H doit être un ndarray")
        self.H = nouveau

    @property
    def Q(self):
        return self._Q

    @Q.setter
    def Q(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("Q doit être un ndarray")
        self.Q = nouveau

    @property
    def R(self):
        return self._R

    @R.setter
    def R(self, nouveau):
        if not isinstance(nouveau, np.ndarray):
            raise TypeError("R doit être un ndarray")
        self.R = nouveau

    @property
    def P(self):
        return self._P

    @property
    def K(self):
        return self._K

    def __call__(self, u_mesures, y_observations=None):
        if not isinstance(u_mesures, np.ndarray):
            raise TypeError("u doit être un ndarray")
        if u_mesures.shape[0] != self.G.shape[1]:
            raise DimensionsNonConformesException(f"obtenues : {u_mesures.shape} attendues : {self.G.shape[1], 1}")

        print("Prediction:")
        self.__prediction_x(u_mesures)
        print(f"x : \n{self.x}")
        self.__prediction_P()
        print(f"P_pre : \n {filtre.P}\n\n")

        print("Correction")
        if y_observations is not None:
            self.__correction_K()
            print(f"K : \n{filtre.K}")
            self.__correction_x(y_observations)
            print(f"x : \n{self.x}")
            self.__correction_P()
            print(f"P : \n {filtre.P}\n")
        return self.x


    def __prediction_x(self, u):
        self.x = self.F@self.x+self.G@u

    def __prediction_P(self):
        self._P = self.F@self.P@self.F.T+self.Q
        print(self.F.T)

    def __correction_K(self):
        self._K = self.P@self.H.T@np.linalg.inv(self.H@self.P@self.H.T + self.R)

    def __correction_x(self, y):
        print(self.x, self.K, y, self.H)
        self.x = self.x + self.K@(y-self.H@self.x)

    def __correction_P(self):
        self._P = (np.eye(self.K.shape[0])-self.K@self.H)@self.P
        print(np.eye(self.K.shape[0]), self.K@self.H, self.P)


class KalmanException (Exception):
    pass

class DimensionsNonConformesException (KalmanException):
    pass

class ParametreNonDefiniException (KalmanException):
    pass


if __name__ == "__main__":
    F = np.array([[1, 1], 
                [0, 1]])
    H = np.array([[1, 0]])
    G = np.array([[0.5], [1]])
    filtre = FiltreKalman(F, H, G=G, Q=np.zeros((2, 2)), R=np.array([[2]]))
    filtre.x = np.array([0, 1]).reshape(2, 1)

    print("=============FILTRE===================")
    filtre(np.zeros((1,1)), y_observations=np.array([1.2]))
    print("=============FILTRE===================")
    filtre(np.zeros((1,1)), y_observations=np.array([2.1]))
    print("=============FILTRE===================")
    filtre(np.zeros((1,1)), y_observations=np.array([3.3]))