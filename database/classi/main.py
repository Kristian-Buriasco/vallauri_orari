import logging
import os

from pdf2image import convert_from_path
import script.divisore as divisore

import time
start = time.process_time()

logging.basicConfig(format='[%(asctime)s] %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%d-%m-%Y %H:%M:%S', filename="../log/LetturaPDF.log", filemode="a")
logging.info('Lettura file PDF iniziata')

os.system("cd PDF && rm * && wget http://www.vallauri.edu/public/ita/img/documenti/Comunicazioni/Comunicazioni202223/Orario/ORARIO_CLASSI_SABATI_CHIUSI.pdf http://www.vallauri.edu/public/ita/img/documenti/Comunicazioni/Comunicazioni202223/Orario/ORARIO_CLASSI_SABATO_APERTO_Classi_PRIME_TECNOLOGICO.pdf http://www.vallauri.edu/public/ita/img/documenti/Comunicazioni/Comunicazioni202223/Orario/ORARIO_CLASSI_SABATO_APERTO_Classi_TECNOLOGICO.pdf")
os.system("rm -rf immagini/* && mkdir immagini/1 immagini/2 immagini/3")

logging.info('Scaricati i file PDF')

CHIUSO = convert_from_path("PDF/ORARIO_CLASSI_SABATI_CHIUSI.pdf")
print("divisione primo...")
for i in range(len(CHIUSO)):
    CHIUSO[i].save('immagini/1/p' + str(i) + '.png', 'PNG')

del CHIUSO #non tutti hanno 64 gb di ram, i comuni mortali si devono arrangiare

logging.info('Diviso ORARIO_CLASSI_SABATI_CHIUSI.pdf')

APERTO_PRIME = convert_from_path("PDF/ORARIO_CLASSI_SABATO_APERTO_Classi_PRIME_TECNOLOGICO.pdf")
print("divisione secondo...")
for i in range(len(APERTO_PRIME)):
    APERTO_PRIME[i].save('immagini/2/p' + str(i) + '.png', 'PNG')

del APERTO_PRIME

logging.info('Diviso ORARIO_CLASSI_SABATO_APERTO_Classi_PRIME_TECNOLOGICO.pdf')


APERTO = convert_from_path("PDF/ORARIO_CLASSI_SABATO_APERTO_Classi_TECNOLOGICO.pdf")
print("divisione terzo...")
for i in range(len(APERTO)):
    APERTO[i].save('immagini/3/p' + str(i) + '.png', 'PNG')

del APERTO

logging.info('Diviso ORARIO_CLASSI_SABATO_APERTO_Classi_TECNOLOGICO.pdf')

divisore.divisore()

logging.info(f'Lettura file PDF finita in {time.process_time() - start}')
