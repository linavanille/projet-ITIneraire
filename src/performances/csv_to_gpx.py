#!/usr/bin/env python 3
""" Module permettant de convertir un fichier csv au format gpx """

from gpx_converter import Converter
import argparse

def main(in_file, out_file):

    Converter(input_file=in_file).csv_to_gpx(lats_colname='Latitude',longs_colname='Longitude',alts_colname='Altitude',output_file=out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')

    args = parser.parse_args()
    main(args.input_file, args.output_file)