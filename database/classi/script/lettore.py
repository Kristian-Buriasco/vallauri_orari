from pytesseract import pytesseract



def lettore(im, orario):
    if orario == 1:
        righeUno = [
            [0, 175],
            [267, 380],
            [495, 595],
            [715, 815],
            [933, 1030],
            [1152, 1260]
        ]
        righeDue = [
            [165, 275],
            [390, 490],
            [615, 720],
            [820, 920],
            [1035, 1160]
        ]
        righeTre = [
            [295, 390],
            [515, 605],
            [735, 815],
            [950, 1040]
        ]
    elif orario == 2:
        righeUno = [
            [0, 135],
            [260, 380],
            [475, 575],
            [715, 815],
            [920, 1030],
            [1130, 1275]
        ]
        righeDue = [
            [130, 245],
            [380, 500],
            [580, 695],
            [810, 930],
            [1030, 1160]
        ]
        righeTre = [
            [295, 390],
            [515, 605],
            [735, 815],
            [950, 1040]
        ]
    else:
        righeUno = [
            [0, 135],
            [260, 380],
            [475, 575],
            [715, 815],
            [920, 1030],
            [1130, 1270]
        ]
        righeDue = [
            [130, 245],
            [380, 500],
            [580, 695],
            [810, 930],
            [1030, 1160]
        ]
        righeTre = [
            [295, 390],
            [515, 605],
            [735, 815],
            [950, 1040]
        ]
    risposta = ""
    riga = 0
    pos = 1
    while riga < 6:
        print(f"riga: {riga}, posizione: {pos}")
        if pos == 1:
            img = im.crop((0, righeUno[riga][0], 347, righeUno[riga][1]))
            text = img_to_string(img)
            print("LETTO:{\n" + text+"\n}")
            if len(text) < 10:
                pos = 2
            else:
                pos = 1
                riga = riga + 1
                risposta=risposta+f":::{text}\n"
        elif pos == 2:
            img = im.crop((0, righeDue[riga][0], 347, righeDue[riga][1]))
            text = img_to_string(img)
            print("LETTO:{\n" + text+"\n}")
            if len(text) < 10:
                pos = 3
            else:
                pos = 1
                riga = riga + 2
                risposta=risposta+f":::{text}\n"
                risposta=risposta+f":::{text}\n"
        else:
            img = im.crop((0, righeTre[riga][0], 347, righeTre[riga][1]))
            text = img_to_string(img)
            pos = 1
            riga = riga + 3
            risposta = risposta + f":::{text}\n"
            risposta = risposta + f":::{text}\n"
            risposta = risposta + f":::{text}\n"
    return risposta

def img_to_string(img):
    text = pytesseract.image_to_string(img)
    text = text.replace("", "")
    text = text.replace("ecnologie meccaniche di processo e prodott", "Tecnologie meccaniche di processo e prodotto")

    test = text.replace("oleae Wray", "Economia aziendale")
    test = text.replace("Seto eva ly", "Economia aziendale")
    test = text.replace("Seto eva ly","Economia aziendale")
    test = text.replace("PTR T", "Diritto ed economia")

    test = text.replace("T.P.S.LT.", "T.P.S.I.T.")

    test = text.replace("DOMINIC! E.", "DOMINICI E.")
    test = text.replace("PAOLETTIL.", "PAOLETTI L.")
    test = text.replace("Ouinae.", "FOTI R.")
    test = text.replace("FACAS |.", "FACAS L.")
    #ottimo modo professionale per risolvere problemi che altrimenti non saprei risolvere o non ho voglia di perderci la testa dietro, è una cosa sbagliata? MA CERTAMENTE
    return text
