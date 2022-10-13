import os
import logging

from PIL import Image
from pytesseract import pytesseract

import script.lettore as lettore
import script.scrittore as scrittore

# import lettore
# import scrittore

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S', filename="../log/LetturaPDF.log", filemode="a")

posGiorni = [[[158, 224], [506, 1531]], [[509, 224], [856, 1531]], [[858, 224], [1207, 1531]],
             [[1209, 224], [1558, 1531]], [[1559, 224], [1907, 1531]], [[1910, 224], [2258, 1531]]]


def divisore():
    """
    Divide le immagini in colonne che vengono passate a "lettore" per poi esser salvati i dati che ritornano
    """
    logging.info('Inizio divisione delle immagini')
    for orario in range(1, 4):
        logging.info(f"Divisione orario {orario}")
        if orario == 1:
            logging.info('Inizio elaborazione primo orario')
        elif orario == 2:
            logging.info('Inizio elaborazione secondo orario')
        else:
            logging.info('Inizio elaborazione terzo orario')

        print(orario)
        numero = int(os.popen(f"ls -l immagini/{orario} | grep -v ^l | wc -l").read()) - 1
        #numero = int(os.popen(f"ls -l ../immagini/{orario} | grep -v ^l | wc -l").read()) - 1
        for pagina in range(numero):
            im = Image.open(f"immagini/{orario}/p{pagina}.png")
            #im = Image.open(f"../immagini/{orario}/p{pagina}.png")
            if orario == 1:
                img = im.crop((910, 90, 1066, 148))
            elif orario == 2:
                img = im.crop((505, 90, 662, 148))
            else:
                img = im.crop((505, 90, 662, 148))
            classe = pytesseract.image_to_string(img)
            del img
            classe = classe.split("\n")[0]
            classe = classe.replace("(", "")
            classe = classe.replace("|", "")
            classe = classe.replace(":", "")
            classe = classe.replace(".", "")
            classe = classe.replace("2AELT", "2A ELT")
            classe = classe.replace("AA", "4A")
            classe = classe.replace("AB", "4B")
            classe = classe.replace("AC", "4C")
            classe = classe.replace("AD", "4D")

            logging.info(f"ELABORAZIONE PAGINA: {pagina}, CLASSE: {classe}")

            print(f"----------------{classe}----------------")
            if orario == 1:
                for giorno in range(5):
                    img = im.crop((posGiorni[giorno][0][0], posGiorni[giorno][0][1], posGiorni[giorno][1][0],
                                   posGiorni[giorno][1][1]))
                    img.save("immagini/1.png")
                    print(f"giorno: {giorno}, orario: {orario}, classe: {classe}")
                    letto = lettore.lettore(img, orario)
                    scrittore.scrivi(classe, orario, giorno, letto)

            elif orario == 2:
                if int(classe[0]) == 1:
                    if classe.split(" ")[1] == "INF" or classe.split(" ")[1] == "ELT" or classe.split(" ")[1] == "MEC":
                        for giorno in range(6):
                            img = im.crop((posGiorni[giorno][0][0], posGiorni[giorno][0][1], posGiorni[giorno][1][0],
                                           posGiorni[giorno][1][1]))
                            print(f"giorno: {giorno}, orario: {orario}, classe: {classe}")
                            letto = lettore.lettore(img, orario)
                            scrittore.scrivi(classe, orario, giorno, letto)
                    else:
                        print("Scartato")
                        logging.info("scartata")
                else:
                    print("Scartato")
                    logging.info("scartata")
            else:
                if int(classe[0]) > 1:
                    if classe.split(" ")[1] == "INF" or classe.split(" ")[1] == "ELT" or classe.split(" ")[1] == "MEC":
                        for giorno in range(6):
                            img = im.crop((posGiorni[giorno][0][0], posGiorni[giorno][0][1], posGiorni[giorno][1][0],
                                           posGiorni[giorno][1][1]))
                            print(f"giorno: {giorno}, orario: {orario}, classe: {classe}")
                            letto = lettore.lettore(img, orario)
                            scrittore.scrivi(classe, orario, giorno, letto)
                    else:
                        print("Scartato")
                        logging.info("scartata")
                else:
                    print("Scartato")
                    logging.info("scartata")
        if orario == 1:
            logging.info('Fine elaborazione primo orario')
        elif orario == 2:
            logging.info('Fine elaborazione secondo orario')
        else:
            logging.info('Fine elaborazione terzo orario')


if __name__ == "__main__":
    divisore()
