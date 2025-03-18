import smbus
import time

# Registres pour le gyroscope
# A COMPLETER
CTRL2_G = 0x11
OUTX_L_G = 0x22

FREQS_G ={
    0           : 0b0000,
    12.5        : 0b0001,
    26          : 0b0010,
    52          : 0b0011,
    104         : 0b0100,
    208         : 0b0101,
    416         : 0b0110,
    833         : 0b0111,
    1.66        : 0b1000,
    3.33e3      : 0b1001,
    6.66e3      : 0b1010,
}

RANGE_G ={
    250         : 0b00,
    500         : 0b01,
    1000        : 0b10,
    2000        : 0b11
}

SENS_G ={
    250         : 8.75e-3,
    500         : 17.50e-3,
    1000        : 35e-3,
    2000        : 70e-3
}

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
    return (FREQS_G[gyro_freq] << 4) | (RANGE_G[gyro_range] << 2)

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
    sensitivity = SENS_G[gyro_range]
    return x * sensitivity, y * sensitivity, z * sensitivity
