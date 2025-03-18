import time
from gnss import *

def get_raw_data():
  """
  Lit les données GNSS brutes (trames NMEA) toutes les 3 secondes et les affiches.
  """
  
  # A COMPLETER
  GNSS_DEVICE_ADDR = 32
  mode = GLONASS
  gnss = GNSS(1, GNSS_DEVICE_ADDR)
  gnss.initialisation(mode)
  
  while True:
    rslt = gnss.get_raw_data()
    data = ""
    for num in range (0, len(rslt)):
      rslt[num] = chr(rslt[num])
      data  = data + rslt[num]
    print(data)
    print("")
    time.sleep(3)
  
if __name__ == "__main__":
  get_raw_data()