def lettura(classe, giorno, ora):
    """
    Legge una singola ora
        :param classe: Classe ricercata come stringa
        :param giorno: Giorno dell'ora da leggere (contando a partire da 0)
        :param ora: Ora da leggere (contando a partire da 0)
        :return: riporta il contenuto dell'ora richiesta
    """
    classe = classe.replace("\n", "")
    if classe.endswith("INF") or classe.endswith("ELT") or classe.endswith("MEC"):
        if (int(classe[0]) > 1):
            orario = leggiNumeroOrario("triennio")
        else:
            orario = leggiNumeroOrario("prima")
    else:
        orario = leggiNumeroOrario("liceo")

    return leggiOrario(classe, giorno, orario, ora)


def leggiNumeroOrario(classe):
    """
    Legge il numero dell'orario da usare (1,2,3 ovvero se sabati chiusi, aperti per le prime o aperti per tutti) in
    base alla settimana attuale
        :param classe: classe da cercare (triennio, prima o liceo)
        :return: ritorna il numero di orario da usare (1,2,3)
    """
    f = open(f"database/classi/orario/{classe}", "r")
    letto = int(f.read())
    f.close()
    return letto


def leggiOrario(classe, giorno, orario, ora):
    """
    Legge l'orario e ritorna una singola ora
        :param classe: Classe da cercare come stringa
        :param giorno: Giorno da cercare (contando da 0)
        :param orario: Orario da usare (1,2,3)
        :param ora: Ora da Cercare (Contando da 0)
        :return: ritorna una singola ora in formato string
    """
    testo = ""
    f = open(f"database/classi/cartelle/{orario}/{classe}/{giorno}.txt", "r")
    testo = "".join(f.readlines())
    f.close()
    testo = testo.split(":::")[ora + 1]
    return testo


def controllo(classe, giorno):
    """
    Controlla se nel giorno indicato la classe frequenta o meno, se non frequenta ritornerà un valore falso, se frequenta sarà vero
        :param classe: Classe da carcare come stringa
        :param giorno: Giorno da controllare
        :return: Valore booleano in base a se frequenta o meno
    """
    if classe.endswith("INF") or classe.endswith("ELT") or classe.endswith("MEC"):
        if (int(classe[0]) > 1):
            orario = leggiNumeroOrario("triennio")
        else:
            orario = leggiNumeroOrario("prima")
    else:
        orario = leggiNumeroOrario("liceo")
    if orario == 1:
        if (giorno == 5 or giorno == 6):
            return False
        else:
            return True
    else:
        if (giorno == 6):
            return False
        else:
            return True


if __name__ == "__main__":
    print(lettura("3E INF", 2, 0))
