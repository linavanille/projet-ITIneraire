import time
import smbus
import time

I2C_YEAR_H = 0
I2C_YEAR_L = 1
I2C_MONTH = 2
I2C_DATE  = 3
I2C_HOUR  = 4
I2C_MINUTE = 5
I2C_SECOND = 6
I2C_LAT_1 = 7
I2C_LAT_2 = 8
I2C_LAT_X_24 = 9
I2C_LAT_X_16 = 10
I2C_LAT_X_8  = 11
I2C_LAT_DIR  = 18 # Inversion Direction Latitude et Longitude (erreur composant)
I2C_LON_1 = 13
I2C_LON_2 = 14
I2C_LON_X_24 = 15
I2C_LON_X_16 = 16
I2C_LON_X_8  = 17
I2C_LON_DIR  = 12 # Inversion Direction Latitude et Longitude (erreur composant)
I2C_USE_STAR = 19
I2C_ALT_H = 20
I2C_ALT_L = 21
I2C_ALT_X = 22
I2C_SOG_H = 23
I2C_SOG_L = 24
I2C_SOG_X = 25
I2C_COG_H = 26
I2C_COG_L = 27
I2C_COG_X = 28
I2C_START_GET = 29
I2C_ID = 30
I2C_DATA_LEN_H = 31
I2C_DATA_LEN_L = 32
I2C_ALL_DATA = 33
I2C_GNSS_MODE = 34
I2C_SLEEP_MODE = 35


GPS = 1
BEIDOU = 2
GPS_BEIDOU = 3
GLONASS = 4
GPS_GLONASS = 5
BEIDOU_GLONASS = 6
GPS_BEIDOU_GLONASS = 7

class struct_utc_time:
  """
  Structure pour l'enregistrement temporel (date et heure).
  """
  def __init__(self):
    """
    Initialise une structure date/heure.
    """
    self.year=2000
    self.month=1
    self.date=1
    self.hour=0
    self.minute=0
    self.second=0
  
  def update_utc_time(self,rslt):
    """
    Met à jour la date et l'heure.

    Arguments:
    - rslt: Une liste contenant les informations de date et heure (lue directement via smbus).
    """
    if rslt != -1:
      self.year = rslt[0]*256 + rslt[1]
      self.month = rslt[2]
      self.date = rslt[3]    
      self.hour = rslt[4]
      self.minute = rslt[5]
      self.second = rslt[6]
      
  def __str__(self):
    """
    Renvoie une chaîne de caractères formatée de la date et l'heure.

    Sortie: Une chaîne de caractère formatée.
    """
    return f"{self.year}/{self.month}/{self.date} - {self.hour}:{self.minute}:{self.second}" 

class struct_GNSS_coordinate:
  """
  Structure pour l'enregistrement positionel (coordonnée latitude ou longitude).
  """
  def __init__(self):
    """
    Initialise une stucture coordonnée.
    """
    self.degres = 0
    self.minutes = 0
    self.fractions_minutes = 0
    self.direction = "S" # N ou S pour la latitude, E ou W pour la longitude
    self.coordinates_DD = 0.00 # Coordonnées au format degré décimaux
    self.coordinates_DMM = "0.00" # Coordonnées au format degré / minute décimales
    self.coordinates_DMS = "0.00" # Coordonnées au format degré décimaux / minutes / secondes
  
  def update_coordinate(self,rslt):
    """
    Met à jour la coordonnée.
    """
    if rslt != -1:
      self.degres = rslt[0]
      self.minutes = rslt[1]
      self.fractions_minutes = rslt[2]*65536 + rslt[3]*256 + rslt[4]
      self.direction = chr(rslt[5])
      
      # A compléter
      self.coords_DD = ...
      self.coords_DMM = ...
      self.coords_DMS = ...
  
class GNSS:
  """
  Classe pour la gestion des acqusitions du GNSS.
  """
  def __init__(self, bus, addr):
    """
    Intialise le module de gestion du GNSS.

    Arguments:
    - bus: Le bus de communication du module GNSS.
    - addr: L'adresse I2C de communication du module GNSS.
    """
    self.i2cbus = smbus.SMBus(bus)
    self.__addr = addr
    self.timestamp = 0
    self.utc = struct_utc_time()
    self.latitude = struct_GNSS_coordinate()
    self.longitude = struct_GNSS_coordinate()
    self.altitude = 0
    self.number_satellites = 0
    self.COG = 0
    self.SOG = 0
    self.reception_ok=False
    
  def begin(self):
    """
    Initialise la connexion au capteur GNSS.   
    """
    rslt = self._read_reg(I2C_ID, 1)
    time.sleep(0.1)
    if rslt == -1:
      return False
    if rslt[0] != self.__addr:
      return False
    return True

  def enable_power(self):
    """
    Active la récupération des données GNSS.
    """
    self._write_reg(I2C_SLEEP_MODE, [0])
    time.sleep(0.1)

  def disable_power(self):
    """
    Désactive la récupération des données GNSS. 
    """
    self._write_reg(I2C_SLEEP_MODE, [1])
    time.sleep(0.1)
  
  def get_mode(self):
    """
    Retourne le mode GNSS utilisé.
    
    Sortie: le mode GNSS utilisé.  
    """
    rslt = self._read_reg(I2C_GNSS_MODE, 1)
    return rslt[0]

  def set_mode(self, mode):
    """
    Actualise le mode GNSS du capteur.
    
    Arguments:
    - mode: le mode GNSS.
    """
    self._write_reg(I2C_GNSS_MODE, [mode])
    time.sleep(0.1) 
    
  def initialisation(self,mode):
    """
    Initialise le module GNSS avant acquisition.
    
    Arguments:
    - mode: le mode GNSS.
    """
    while (self.begin() == False):
      print("Echec de l'initialisation")
      time.sleep(1)
    self.enable_power()
    self.set_mode(mode)

  def check_gnss_reception(self):
    rslt = self._read_reg(I2C_USE_STAR, 1)
    return rslt != -1

  def update_utc_time(self):
    rslt = self._read_reg(I2C_YEAR_H, 7)
    self.utc.update_utc_time(rslt)

  def update_number_satellites(self):
    """
    Actualise le nombre de satellites connectés au module GNSS.
    """
    rslt = self._read_reg(I2C_USE_STAR, 1)
    if rslt != -1:
      self.number_satellites = rslt[0]
    else:
      self.number_satellites = 0

  def update_latitude(self):
    """
    Actualise la latitude du capteur.
    """
    rslt = self._read_reg(I2C_LAT_1, 5)
    rslt.append(self._read_reg(I2C_LAT_DIR,1)[0])
    self.latitude.update_coordinate(rslt)

  def update_longitude(self):
    """
    Actualise la longitude du capteur. 
    """
    rslt = self._read_reg(I2C_LON_1, 5)
    rslt.append(self._read_reg(I2C_LON_DIR,1)[0])
    self.longitude.update_coordinate(rslt)


  def update_altitude(self):
    """
    Actualise l'altitude du capteur. 
    """
    rslt = self._read_reg(I2C_ALT_H, 3)
    if rslt != -1:
      self.altitude = rslt[0]*256 + rslt[1] + rslt[2]/100.0
    else:
      self.altitude = 0.0

  def update_COG(self):
    """
    Actualise la COG (Course Over Ground) du capteur. 
    """
    rslt = self._read_reg(I2C_COG_H, 3)
    if rslt != -1:
      self.COG = rslt[0]*256 + rslt[1] + rslt[2]/100.0
    else:
      self.COG = 0.0

  def update_SOG(self):
    """
    Actualise la SOG (Speed Over Ground) du capteur. 
    """
    rslt = self._read_reg(I2C_SOG_H, 3)
    if rslt != -1:
      self.SOG = rslt[0]*256 + rslt[1] + rslt[2]/100.0
    else:
      self.SOG = 0.0

  def update_timestamp(self):
    self.timestamp=time.time()

  def update(self):
    """
    Actualise les données capteur.
    """
    self.update_number_satellites()
    if self.number_satellites!=0:
      self.reception_ok = True
      self.update_utc_time()
      self.update_timestamp()
      self.update_latitude()
      self.update_longitude()
      self.update_altitude()
      self.update_COG()
      self.update_SOG()
    else:
      self.reception_ok = False

  def get_gnss_len(self):
    """
    Retourne la longueur des données GNSS reçues.
    
    Sortie: la longueur des données GNSS.
    """
    self._write_reg(I2C_START_GET, [0x55])
    time.sleep(0.1)
    rslt = self._read_reg(I2C_DATA_LEN_H, 2)
    if rslt != -1:
      return rslt[0]*256 + rslt[1]
    else:
      return 0

  def get_raw_data(self):
    """
    Retourne les données brutes reçues par le GNSS (les différentes trames NMEA).
    """
    len = self.get_gnss_len()
    time.sleep(0.1)
    all_data = [0]*(len+1)
    len1 = (len) // 32
    len2 = ((len)%32) 
    for num in range (0, len1+1):
      if num == len1:
        rslt = self._read_reg(I2C_ALL_DATA, len2)
        for i in range (0, len2):
          if rslt[i] == 0:
            rslt[i] = 0x0A
        all_data[num*32:] = rslt
      else:
        rslt = self._read_reg(I2C_ALL_DATA, 32)
        for i in range (0, 32):
          if rslt[i] == 0:
            rslt[i] = 0x0A
        all_data[num*32:] = rslt
    return all_data

  def _write_reg(self, reg, data):
    while 1:
      try:
        self.i2cbus.write_i2c_block_data(self.__addr, reg, data)
        return
      except:
        print("Problème d'écriture")
        time.sleep(1)

  def _read_reg(self, reg, len):
    try:
      rslt = self.i2cbus.read_i2c_block_data(self.__addr, reg, len)
    except:
      rslt = -1
    return rslt