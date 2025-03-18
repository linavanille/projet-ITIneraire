import smbus
import time

# Registres pour l'accéléromètre
# A COMPLETER
CTRL1_XL = 0x10
OUTX_L_A = 0x28

FREQS_ACC = {
    0       : 0b0000,
    # 1.6     : 0b1011,
    12.5    : 0b0001,
    26      : 0b0010,
    52      : 0b0011,
    104     : 0b0100,
    208     : 0b0101,
    416     : 0b0110,
    833     : 0b0111,
    1.66e3  : 0b1000,
    3.33e3  : 0b1001,
    6.66e3  : 0b1010
}

RANGE_ACC = {
    2        : 0b00,
    4        : 0b10,
    8        : 0b11,
    16       : 0b01
}

SENS_ACC = {
    2        : 0.061e-3,
    4        : 0.122e-3,
    8        : 0.244e-3,
    16       : 0.488e-3
}

def accelerometer_configuration(accel_range, accel_freq):
    """
    Configure les paramètres du LSM6DSO pour l'accéléromètre.

    Arguments: 
    - accel_range: la range de l'accélérateur
    - accel_freq: la fréquence d'acquisition de l'accélérateur

    Résultat : l'octet à écrire dans le registre CTRL1_XL pour configurer l'accéléromètre
    """
    return (RANGE_ACC[accel_range] << 4) | (FREQS_ACC[accel_freq] << 2)

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
    sensitivity = SENS_ACC[accel_range]
    return x * sensitivity, y * sensitivity, z * sensitivity
