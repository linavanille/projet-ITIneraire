# /bin/bash

if [ "$1" = 'clean' ]; then
    echo "rm ./output/HTML/plot*/*"
    echo "rm ./output/CSV_Filtre/*"
    rm ./output/HTML/plot*/*
    rm ./output/CSV_Filtre/*

elif [ "$1" = 'raw' ]; then
    echo "python3 src/analyse_acquisitions.py -- raw"
    python3 src/analyse_acquisitions.py -- raw

elif [ "$1" = '-a' ]; then
    echo "python3 src/analyse_acquisitions.py -- all"
    python3 src/analyse_acquisitions.py -- all

elif [ "$1" = "-n" ]; then
    echo "clean output"
    rm ./output/HTML/plot*/*
    rm ./output/CSV_Filtre/*
    echo "python3 src/analyse_acquisitions.py -- all"
    python3 src/analyse_acquisitions.py -- all
else
    echo "python3 src/analyse_acquisitions.py -- filtre"
    python3 src/analyse_acquisitions.py -- filtre
fi
