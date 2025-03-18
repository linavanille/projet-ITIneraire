import smbus
import time
from accelerometer import accelerometer_configuration, read_accelerometer, CTRL1_XL
from gyroscope import gyroscope_configuration, read_gyroscope, CTRL2_G

# Adresse I2C du capteur LSM6DSO
# A COMPLETER
LSM6DSO_ADDR = ...

# Initialisation du bus I2C
bus = smbus.SMBus(1)

def initialize_sensors(accel_range, accel_freq, gyro_range, gyro_freq):
    """
    Initialise les capteurs en écrivant dans leurs registres de configuration en fonction des paramètres de configuration précisés.

    Arguments:
    - accel_range: la range de l'accélérateur
    - accel_freq: la fréquence d'acquisition de l'accélérateur
    - gyro_range: la range du gyroscope
    - gyro_freq: la fréquence d'acquisition du gyroscope
    """
    bus.write_byte_data(LSM6DSO_ADDR, CTRL1_XL, accelerometer_configuration(accel_range,accel_freq))
    bus.write_byte_data(LSM6DSO_ADDR, CTRL2_G, gyroscope_configuration(gyro_range,gyro_freq))
    time.sleep(0.1)


def read_raw_data(device_addr, start_register):
    """
    Lit 6 octets depuis le capteur à l'adresse spécifiée et retourne les valeurs signées.

    Arguments:
    - device_addr: l'adresse I2C du composant
    - start_register: l'addresse du premier registre à lire 

    Résultat: les données acquises de l'accélérateur ou gyroscope sur ces 3 axes (en valeur entières brutes signées)
    """
    data = bus.read_i2c_block_data(device_addr, start_register, 6)
    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)
    z = data[4] | (data[5] << 8)

    # Convertir en valeurs signées 16 bits
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    return x, y, z


def read_IMU(accel_range,gyro_range):
    """
    Lit les données d'acquisition de l'IMU (accéléromètre et gyroscope)

    Arguments: 
    - accel_range: la range de l'accélérateur
    - gyro_range: la range du gyroscope

    Résultat: Les données acquises par l'accélérateur (accel_x,accel_y,accel_z) et le gyroscope (gyro_x,gyro_y,gyro_z) 
    """
    accel_x,accel_y,accel_z = read_accelerometer(accel_range)
    gyro_x,gyro_y,gyro_z = read_gyroscope(gyro_range)
    return accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z