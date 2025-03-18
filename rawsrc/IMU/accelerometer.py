import smbus
import time

# Registres pour l'accéléromètre
# A COMPLETER
CTRL1_XL = ...
OUTX_L_A = ...

def accelerometer_configuration(accel_range, accel_freq):
    """
    Configure les paramètres du LSM6DSO pour l'accéléromètre.

    Arguments: 
    - accel_range: la range de l'accélérateur
    - accel_freq: la fréquence d'acquisition de l'accélérateur

    Résultat : l'octet à écrire dans le registre CTRL1_XL pour configurer l'accéléromètre
    """
    # Configuration de l'accéléromètre
    # A COMPLETER
    ...
    return 0

def read_accelerometer(accel_range):
    """
    Lit les données de l'accéléromètre et les convertit.

    Arguments: 
    - accel_range: la range de l'accéléromètre

    Résultat: les données acquises par de l'accéléromètre en unité physique sur les 3 axes
    """
    from IMU import read_raw_data, LSM6DSO_ADDR
    x, y, z = read_raw_data(LSM6DSO_ADDR, OUTX_L_A)

    # A COMPLETER
    sensitivity = ...
    return x * sensitivity, y * sensitivity, z * sensitivity
