# /bin/bash

if [ "$1" = 'clean' ]; then
    echo "rm ./output/HTML/plot*/*"
    rm ./output/HTML/plot*/*
    echo "rm ./output/CSV_Filtre*/*"
    rm ./output/CSV_Filtre*/*
    echo "rm ./output/GPX/*"
    rm ./output/GPX/*

elif [ "$1" = 'raw' ]; then
    echo "python3 src/analyse_acquisitions.py -- raw"
    python3 src/analyse_acquisitions.py -- raw

elif [ "$1" = '-a' ]; then
    echo "python3 src/analyse_acquisitions.py -- all"
    python3 src/analyse_acquisitions.py -- all

elif [ "$1" = "-n" ]; then
    echo "clean output"
    rm ./output/HTML/plot*/*
    rm ./output/CSV_Filtre*/*
    rm ./output/GPX/*
    echo "python3 src/analyse_acquisitions.py -- all"
    python3 src/analyse_acquisitions.py -- all
    echo "creation des gpx"
    ipython3 convertisseur/csv_to_gpx.py output/CSV_Filtre/magellan.csv output/GPX/filtre.gpx
    ipython3 convertisseur/csv_to_gpx.py output/DoubleAcquisition/acquisitionGPS.csv output/GPX/raw.gpx

elif [ "$1" = '-gpx' ]; then
    echo "conversion gpx de l'output filtre"
    ipython3 convertisseur/csv_to_gpx.py output/CSV_Filtre/magellan.csv output/GPX/filtre.gpx
    echo "conversion gpx des données brutes"
    ipython3 convertisseur/csv_to_gpx.py output/DoubleAcquisition/acquisitionGPS.csv output/GPX/raw.gpx
else
    echo "python3 src/analyse_acquisitions.py -- filtre"
    python3 src/analyse_acquisitions.py -- filtre
fi
