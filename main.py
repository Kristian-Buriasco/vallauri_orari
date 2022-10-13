import datetime
import logging
import random

import pytz
from telegram import Update
from telegram.ext import Updater, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackContext, MessageHandler

import database.classi.database_read as database_read

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="ciao, ti aiuterò nella configurazione \n- configura l'indirizzo con il comando /indirizzo seguito dall'indirizo (INF, ELT, LIC, ...)\n- configura la sezione con il comando /sezione seguito dalla sezione (A, B, C, D, ...)\n- come ultima cosa configura l'anno con il comando /anno seguito dall'anno (1, 2, 3, 4, 5)\n- puoi vedere la configurazione usando il comando /classe\nTutte le informazioni che verranno usate dal bot sono ricavate da una lettura automatizzata dei PDF forniti dall'istituto, pertanto potrebbero esserci degli errori, potrai comunicarceli con /errore seguito dalla descrizione dell'errore l'errore in modo che potremo sistemarli")

async def indirizzo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argomento = " ".join(context.args)
    argomento = argomento.replace(" ", "")
    argomento = argomento.upper()
    if argomento == "AFM" or argomento == "ELT" or argomento == "INF" or argomento == "LIC" or argomento == "MEC" or argomento == "TUR" or argomento == "MEN":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"fai parte dell'indirizzo {argomento},\nSe è sbagliato puoi modificarlo ripetendo lo stesso comando")
        if controllo_id(context._chat_id):
            cambia_valore(context._chat_id, argomento, 3)
        else:
            aggiungi_valore(context._chat_id, argomento, 3)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="c'è stato un errore, probabilmente hai sbagliato a inserire l'indirizzo")


async def sezione(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argomento = " ".join(context.args)
    argomento = argomento.replace(" ", "")
    argomento = argomento.upper()
    if argomento == "A" or argomento == "B" or argomento == "C" or argomento == "D" or argomento == "E" or argomento == "F" or argomento == "G":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"fai parte della sezione {argomento},\nSe è sbagliato puoi modificarlo "
                                            f"ripetendo lo stesso comando")
        if controllo_id(context._chat_id):
            cambia_valore(context._chat_id, argomento, 2)
        else:
            aggiungi_valore(context._chat_id, argomento, 2)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="c'è stato un errore, probabilmente hai sbagliato a inserire la sezione")


async def anno(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argomento = " ".join(context.args)
    argomento = argomento.replace(" ", "")
    argomento = argomento.upper()
    if argomento == "1" or argomento == "2" or argomento == "3" or argomento == "4" or argomento == "5":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"fai parte dell'anno {argomento},\nSe è sbagliato puoi modificarlo ripetendo lo stesso comando")
        if controllo_id(context._chat_id):
            cambia_valore(context._chat_id, argomento, 1)
        else:
            aggiungi_valore(context._chat_id, argomento, 1)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="c'è stato un errore, probabilmente hai sbagliato a inserire l'anno")


async def classe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    testo = "\n".join(linee)
    f.close()
    riga = "non è stata trovata l'informazione che hai chiesto, prova prima a impostare qualche parametro"
    for linea in linee:
        if int(linea.split(":")[0]) == int(context._chat_id):
            riga = linea.split(":")
    if len(riga) == 93: #è un accrocchio? si! funziona? certo. potrei farlo molto meglio? probabile. lo faro? forse.
                        #è un commento utile? ma assolutamente no
        await context.bot.send_message(chat_id=update.effective_chat.id, text=riga)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"ID:{riga[0]}, {riga[1]}{riga[2]} {riga[3]}")


async def ora(update: Update,context: ContextTypes.DEFAULT_TYPE): #ancora moooooooooooooooooooolto da modificare
    argomenti = " ".join(context.args).strip()
    argomenti = argomenti.split(" ")
    giorno = "nulla"
    if len(argomenti) == 2:
        giorno = "oggi"
    elif len(argomenti) == 3:
        if argomenti[1] == "oggi":
            giorno = "oggi"
        elif argomenti[1] == "domani":
            giorno = "domani"
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="/ora <ora>, se si vuole si può specificare se far inviare l'orario del giorno attuale o del giorno successivo con \"oggi\" o \"domani\"")

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="/ora <ora>, se si vuole si può specificare se far inviare l'orario del giorno attuale o del giorno successivo con \"oggi\" o \"domani\"")

    if argomenti == "oggi":
        divisa = " ".join(argomenti[0]).replace(" ", "").split(":")
        divisa[0] = int(divisa[0])
        divisa[1] = int(divisa[1])

        if len(divisa) == 2 and divisa[0] <= 24 and divisa[0] >= 0 and divisa[1] <= 59 and divisa[1] >= 0:

            chat_id = update.effective_chat.id
            context.job_queue.run_daily(orario_programmato_oggi, time=datetime.time(hour=divisa[0], minute=divisa[1],tzinfo=pytz.timezone('Europe/Rome')),chat_id=chat_id, name=str(chat_id))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Orario automatico correttamente settato alle {divisa[0]}:{divisa[1]} di ogni giorno.\nManderà l'orario della giornata.\n\nPuoi modificarlo con /modificaora")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="controlla il messaggio che hai mandato, assicurati di aver scritto l'ora in 24h (14:20)")
    elif argomenti == "domani":
        divisa = " ".join(argomenti[0]).replace(" ", "").split(":")
        divisa[0] = int(divisa[0])
        divisa[1] = int(divisa[1])

        if len(divisa) == 2 and divisa[0] <= 24 and divisa[0] >= 0 and divisa[1] <= 59 and divisa[1] >= 0:

            chat_id = update.effective_chat.id
            context.job_queue.run_daily(orario_programmato_domani, time=datetime.time(hour=divisa[0], minute=divisa[1],tzinfo=pytz.timezone('Europe/Rome')),chat_id=chat_id, name=str(chat_id))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Orario automatico correttamente settato alle {divisa[0]}:{divisa[1]} di ogni giorno.\nManderà l'orario della giornata successiva.\n\nPuoi modificarlo con /modificaora")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="controlla il messaggio che hai mandato, assicurati di aver scritto l'ora in 24h (14:20)")


async def orario_programmato_oggi(context: ContextTypes.DEFAULT_TYPE):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    riga = "non è stata trovata l'informazione che hai chiesto, prova prima a impostare qualche parametro"
    for linea in linee:
        if int(linea.split(":")[0]) == int(context._chat_id):
            riga = linea.split(":")
    if len(riga) == 93:
        await context.bot.send_message(chat_id=context.job.chat_id, text=riga)
    else:
        giorno = datetime.date.today().weekday()
        giorno = giorno
        if giorno == 7:
            giorno = 0
        if giorno == 6 or giorno == 5:
            text = no_scuola()
            await context.bot.send_message(chat_id=context.job.chat_id, text=text)
        for ora in range(0, 6):
            risposta = database_read.lettura(f"{riga[1]}{riga[2]} {riga[3]}", giorno, ora)
            await context.bot.send_message(chat_id=context.job.chat_id, text=risposta)


async def orario_programmato_domani(context: ContextTypes.DEFAULT_TYPE):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    riga = "non è stata trovata l'informazione che hai chiesto, prova prima a impostare qualche parametro"
    for linea in linee:
        if int(linea.split(":")[0]) == int(context._chat_id):
            riga = linea.split(":")
    if len(riga) == 93:
        await context.bot.send_message(chat_id=context.job.chat_id, text=riga)
    else:
        giorno = datetime.date.today().weekday()
        giorno = giorno + 1
        if giorno == 7:
            giorno = 0
        if giorno == 6 or giorno == 5:
            text = no_scuola()
            await context.bot.send_message(chat_id=context.job.chat_id, text=text)
        for ora in range(0, 6):
            risposta = database_read.lettura(f"{riga[1]}{riga[2]} {riga[3]}", giorno, ora)
            await context.bot.send_message(chat_id=context.job.chat_id, text=risposta)


async def orario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    riga = "non è stata trovata l'informazione che hai chiesto, prova prima a impostare qualche parametro"
    for linea in linee:
        if int(linea.split(":")[0]) == int(context._chat_id):
            riga = linea.split(":")
    if len(riga) == 93:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=riga)
    else:
        giorno = datetime.date.today().weekday()
        giorno = giorno

        if database_read.controllo(riga[1] + riga[2] + " " + riga[3].replace("\n", ""), giorno):
            for ora in range(0, 6):
                risposta = database_read.lettura(riga[1] + riga[2] + " " + riga[3].replace("\n", ""), giorno, ora)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta)
        else:
            testo = no_scuola()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=testo)


async def orariodomani(update: Update, context: ContextTypes.DEFAULT_TYPE):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    riga = "non è stata trovata l'informazione che hai chiesto, prova prima a impostare qualche parametro"
    for linea in linee:
        if int(linea.split(":")[0]) == int(context._chat_id):
            riga = linea.split(":")
    if len(riga) == 93:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=riga)
    else:
        giorno = datetime.date.today().weekday()
        giorno = giorno + 1
        if giorno == 7:
            giorno = 0

        if database_read.controllo(riga[1] + riga[2] + " " + riga[3].replace("\n", ""), giorno):
            for ora in range(0, 6):
                risposta = database_read.lettura(f"{riga[1]}{riga[2]} {riga[3]}", giorno, ora)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=risposta)
        else:
            testo = no_scuola()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=testo)


async def errore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argomento = " ".join(context.args)
    if len(argomento) > 0:
        f = open("database/errori.txt", "a")
        f.write("\n" + argomento)
        f.close()
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="la segnalazione è stata registrata con successo")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="non è stato possibile registrare la segnalazione, probabilmente non sono stati trasmessi valori al comando (/errore questo è un errore)")


async def gattino(update: Update, context: ContextTypes.DEFAULT_TYPE): #mi sembra scontata come cosa... non può assolutamente mancare un comando simile...
    gatti = [100, 101, 102, 200, 201, 202, 203, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402,
             403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424,
             425, 426, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511,
             521, 522, 523, 525, 599]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="un gattino per sanino")
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                 photo=f"https://http.cat/{str(random.choice(gatti))}")


def controllo_id(id):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    for linea in linee:
        id_salvato = linea.split(":")[0]
        if int(id_salvato) == int(id):
            return 1
    return 0


def cambia_valore(id, valore, posizione):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    finale = []
    for linea in linee:
        riga = linea.split(":")
        if int(riga[0]) == int(id):
            riga[posizione] = valore
        if posizione == 3 and linee[-1] != linea:
            finale.append(":".join(riga) + "\n")
        else:
            finale.append(":".join(riga))
    f = open("database/groups.txt", "w")
    f.writelines(finale)
    f.close()


def aggiungi_valore(id, valore, posizione):
    f = open("database/groups.txt", "r")
    linee = f.readlines()
    f.close()
    diviso = [str(id), "", "", ""]
    diviso[posizione] = valore
    linea = ":".join(diviso)
    linee.append(linea)
    finale = []
    for x in linee:
        if not "\n" in x:
            x = x + "\n"
        finale.append(x)
    f = open("database/groups.txt", "w")
    f.writelines(finale)
    f.close()


def no_scuola():
    f = open("database/frasi/no_scuola.txt", "r") #per la fantasia di queste bellissime frasi bisogna ringraziare gabriel ferrero
    righe = f.readlines()
    f.close()
    text = random.choice(righe)
    text.replace("\n", "")
    return text


if __name__ == '__main__':
    application = ApplicationBuilder().token('1739515881:AAFHCxiH52FCT9tDhFyFinRQa6in8umzCEg').build()
    # application = ApplicationBuilder().token('1794508549:AAEYyhKlru1gRnUP3XE0-hsbDmqtJ_56FxU').build()

    start_handler = CommandHandler('start', start)
    indirizzo_comando = CommandHandler('indirizzo', indirizzo)
    sezione_comando = CommandHandler('sezione', sezione)
    anno_comando = CommandHandler('anno', anno)
    classe_comando = CommandHandler('classe', classe)
    ora_comando = CommandHandler('ora', ora)
    orario_comando = CommandHandler('orario', orario)
    orariodomani_comando = CommandHandler('orariodomani', orariodomani)
    errore_comando = CommandHandler('errore', errore)
    gattino_comando = CommandHandler('gattino', gattino)

    application.add_handler(start_handler)
    application.add_handler(indirizzo_comando)
    application.add_handler(sezione_comando)
    application.add_handler(anno_comando)
    application.add_handler(classe_comando)
    application.add_handler(ora_comando)
    application.add_handler(orario_comando)
    application.add_handler(orariodomani_comando)
    application.add_handler(errore_comando)
    application.add_handler(gattino_comando)
    application.run_polling()
