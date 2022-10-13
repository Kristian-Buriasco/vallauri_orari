"""
SI DOVREBBERO GESTIRE LE SETTIMANE DI VACANZA
"""
def main():
    prima()
    triennio()

def prima():
    """
    Esegue le operazioni per variare i file in base alla settimana attuale per i file della prima
    """
    f = open("nSettPrima", "r")
    letto = f.read()
    f.close()
    if letto.startswith("A"):
        if int(letto[1]) == 3:
            f=open("nSettPrima", "w")
            f.write(f"B{1}")
            f.close()
            f=open("prima","w")
            f.write("2")
            f.close()
        else:
            f=open("nSettPrima", "w")
            f.write(f"A{int(letto[1])+1}")
            f.close()


    elif letto.startswith("B"):
        if int(letto[1]) == 3:
            f=open("nSettPrima", "w")
            f.write(f"A{1}")
            f.close()
            f=open("prima","w")
            f.write("1")
            f.close()
        else:
            f=open("nSettPrima", "w")
            f.write(f"B{int(letto[1])+1}")
            f.close()

def triennio():
    """
    Esegue le operazioni per variare i file in base alla settimana attuale per i file del triennio
    """
    f = open("nSettTriennio", "r")
    letto = f.read()
    f.close()
    if letto.startswith("A"):
        if int(letto[1]) == 4:
            f=open("nSettTriennio", "w")
            f.write(f"B{1}")
            f=open("triennio","w")
            f.write("3")
            f.close()
        else:
            f = open("nSettTriennio", "w")
            f.write(f"A{int(letto[1])+1}")
    elif letto.startswith("B"):
        if int(letto[1]) == 2:
            f=open("nSettTriennio", "w")
            f.write(f"A{1}")
            f=open("triennio","w")
            f.write("1")
            f.close()
        else:
            f=open("nSettTriennio", "w")
            f.write(f"B{int(letto[1])+1}")


if __name__ == "__main__":
    main()