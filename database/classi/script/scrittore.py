import os
def scrivi(classe, orario, giorno, dati):
    try:
        os.mkdir(f"cartelle/{orario}/{classe.strip()}")
        #os.mkdir(f"../cartelle/{orario}/{classe}")
    except:
        print("already exist")
    f = open(f"cartelle/{str(orario)}/{classe.strip()}/{str(giorno)}.txt", "w")
    #f = open(f"../cartelle/{str(orario)}/{str(classe)}/{str(giorno)}.txt", "w")
    f.write(dati)
    f.close()
