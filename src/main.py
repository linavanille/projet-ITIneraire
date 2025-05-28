import multiprocessing
import time
import os
import random
from performances import csv_to_gpx

from GPS.plot_gnss import plot_GNSS
from GPS.Button import Button
from performances.front import Front
from get_data import get_data

RESET = "\033[0m"
GREEN = "\033[32m"
BLUE = "\033[34m"

def main()->None:

    iid = random.randint(1, 100)*random.randint(1, 5)

    b = Button(17)
    com_bouton = multiprocessing.Queue()
    def press():
        com_bouton.put('debut')
    time.sleep(1)

    b.on_press(press)

    # app = Front()
    # choix = ''
    # while choix != "Q" :

    #     app.menu()

    #     choix = input("Menu : ").upper()

    #     if choix == "1" :
    #         app.historique
    #     elif choix == "2" :
    #         entree = ''

    while com_bouton.empty():
        os.system('clear')
        print("-- Appuyer sur le bouton pour lancer une acquisition--")

        time.sleep(5)
        # app.avant_acquisition

    b.cleanup()
    csv_out = f"./output/Historique/acquisition_{iid}.csv"
    html_out = f"./output/Historique/HTML/"
    gpx_out = f"./output/Historique/GPX/acquisition_{iid}.gpx"

    print(f"C'est parti !!\n Filtrage de l'acquisition dans {GREEN}{csv_out}{RESET}")
    get_data(csv_out)
    print(f'Génération de {BLUE}{csv_out}{RESET} dans {GREEN}{html_out}{RESET}')
    plot_GNSS(csv_out, html_out)
    print(f'Génération de {BLUE}{csv_out}{RESET} dans {GREEN}{gpx_out}{RESET}')
    csv_to_gpx.main(csv_out, gpx_out)

    print('fin')

if __name__ == "__main__":
    main()
