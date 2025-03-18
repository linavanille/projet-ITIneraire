import smbus
import time

# Registres pour le gyroscope
# A COMPLETER
CTRL2_G = ...
OUTX_L_G = ...

def gyroscope_configuration(gyro_range, gyro_freq):
    """
    Configure les paramètres du LSM6DSO pour le gyroscope.

    Arguments: 
    - gyro_range: la range du gyroscope
    - gyro_freq: la fréquence d'acquisition du gyroscope

    Résultat : l'octet à écrire dans le registre CTRL2_G pour configurer le gyroscope
    """
    # Configuration du gyroscope
    # A COMPLETER
    ...
    return 0

def read_gyroscope(gyro_range):
    """
    Lit les données du gyroscope et les convertit.

    Arguments: 
    - gyro_range: la range du gyroscope

    Résultat: les données acquises par le gyroscope en unité physique sur les 3 axes
    """
    from IMU import read_raw_data, LSM6DSO_ADDR
    x, y, z = read_raw_data(LSM6DSO_ADDR, OUTX_L_G)
    
    # A COMPLETER
    sensitivity = ...
    return x * sensitivity, y * sensitivity, z * sensitivity
