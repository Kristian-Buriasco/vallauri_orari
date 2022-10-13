def lettura(classe, giorno, ora):
    classe=classe.replace("\n","")
    if classe.endswith("INF") or classe.endswith("ELT") or classe.endswith("MEC"):
        if (int(classe[0]) > 1):
            orario = leggiNumeroOrario("triennio")
        else:
            orario = leggiNumeroOrario("prima")
    else:
        orario = leggiNumeroOrario("liceo")

    return leggiOrario(classe, giorno, orario, ora)
def leggiNumeroOrario(classe):
    f = open(f"database/classi/orario/{classe}", "r")
    letto = int(f.read())
    f.close()
    return letto

def leggiOrario(classe, giorno, orario, ora):
    testo = ""
    f=open(f"database/classi/cartelle/{orario}/{classe}/{giorno}.txt","r")
    testo = "".join(f.readlines())
    f.close()
    testo=testo.split(":::")[ora+1]
    return testo

def controllo(classe, giorno):
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
