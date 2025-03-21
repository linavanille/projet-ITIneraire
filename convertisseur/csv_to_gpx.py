#!/usr/bin/env python 3 
""" Module permettant de convertir un fichier csv au format gpx """

from gpx_converter import Converter 

def main():
    
    Converter(input_file='test.csv').csv_to_gpx(lats_colname='Latitude',longs_colname='Longitude',alts_colname='Altitude',output_file='test.gpx')

if __name__ == "__main__":
    main()