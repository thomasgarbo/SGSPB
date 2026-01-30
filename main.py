import sqlite3
from datetime import datetime

#CONNESSIONE AL DATABASE
conn = sqlite3.connect("db_sgspb.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

#CREAZIONE DATABASE
cur.execute("""
        CREATE TABLE IF NOT EXISTS CATEGORIE (
            nome_cat VARCHAR(50) PRIMARY KEY NOT NULL
        )
""")
conn.commit()

cur.execute("""
        CREATE TABLE IF NOT EXISTS SPESE (
            n_spesa INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            importo_spesa NUMERIC(50,2) NOT NULL CHECK (importo_spesa>0),
            descrizione VARCHAR(200),
            cat_spesa VARCHAR(50) NOT NULL,
            FOREIGN KEY (cat_spesa) REFERENCES CATEGORIE (nome_cat)
        );
""")
conn.commit()

cur.execute("""
        CREATE TABLE IF NOT EXISTS BUDGET (
            n_budget INTEGER PRIMARY KEY AUTOINCREMENT,
            anno INTEGER NOT NULL,
            mese INTEGER NOT NULL,
            importo_budget FLOAT NOT NULL CHECK (importo_budget>0),
            cat_budget VARCHAR(50) NOT NULL,
            FOREIGN KEY (cat_budget) REFERENCES CATEGORIE (nome_cat),
            UNIQUE (anno, mese, cat_budget)
        );
""")
conn.commit()

print("\nBUONGIORNO! BENVENUTO NEL PROGRAMMA DI GESTIONE DELLE TUE SPESE PERSONALI!")

#CREAZIONE DELLA FUNZIONE menu()
def menu():
    print("""
___________________________________   
|  SISTEMA SPESE PERSONALI        |
|—————————————————————————————————|
|  1. Gestione Categorie          |
|  2. Inserisci Spesa             |
|  3. Definisci Budget Mensile    |
|  4. Visualizza Report           |
|  5. Esci                        |
|_________________________________|
""")
        
#CREAZIONE DELLA FUNZIONE nuova_scelta() del menu'
def nuova_scelta():
    print("""
___________________________________   
|  MENU'                          |
|—————————————————————————————————|
|  1. Gestione Categorie          |
|  2. Inserisci Spesa             |
|  3. Definisci Budget Mensile    |
|  4. Visualizza Report           |
|  5. Esci                        |
|_________________________________|
"""
    )
    scelta = str(input("Inserisci una nuova scelta: "))
    return scelta

#CREAZIONE DELLA FUNZIONE menu_report()
def menu_report():
    print("""
________________________________________ 
|  MENU' DEI REPORT                    |
|——————————————————————————————————————|
|  1. Totale spese per categoria       |
|  2. Spese mensili VS Budget          |
|  3. Elenco completo delle spese      |
|  4. Ritorna al menu principale       |
|______________________________________|
"""
    )

#CREAZIONE DELLA FUNZIONE nuova_scelta_report() del menu' report
def nuova_scelta_report():
    print("""
________________________________________ 
|  MENU' DEI REPORT                    |
|——————————————————————————————————————|
|  1. Totale spese per categoria       |
|  2. Spese mensili VS Budget          |
|  3. Elenco completo delle spese      |
|  4. Ritorna al menu principale       |
|______________________________________|
"""
    )
    scelta_report = str(input("Vuoi consultare altri report? Inserisci il numero corrispondente o '4' per tornare al menu' principale: "))
    return scelta_report


#CREAZIONE FUNZIONI DEL PROGRAMMA:

#CREAZIONE DELLA FUNZIONE inserisci_cat() per l'inserimento di una nuova categoria nel db
def inserisci_cat():
    while True:
        cat = str(input("\nInserisci il nome di una nuova categoria: ")).strip().upper()
        while cat == "":
            cat = str(input("Riprova. Inserisci il nome di una nuova categoria: ")).strip().upper()
        cur.execute(
            "SELECT * FROM CATEGORIE WHERE nome_cat = ?",
            (cat,)
        )
        verifica_cat = cur.fetchone()
        if verifica_cat is not None:
            print("Errore, categoria presente nel database.")
        else:
            cur.execute(
            "INSERT INTO CATEGORIE (nome_cat) VALUES (?)",
            (cat,)
            )
            print("Categoria inserita correttamente.")
            conn.commit()
            break


#CREAZIONE DELLA FUNZIONE inserisci_spesa() per l'inserimento di una nuova spesa nel db
def inserisci_spesa():
    while True:
        try:     
            data_spesa = str(input("\nInserisci la data della spesa: (yyyy-mm-dd)    ")).strip()
            data_spesa = datetime.strptime(data_spesa, "%Y-%m-%d").date()
            if data_spesa.year < 1800 or data_spesa.year > 2200:
                print("Errore! Inserisci una data con un anno corretto.  (1800-2200)")
            else:
                data_spesa = data_spesa.isoformat()
                break
        except ValueError:
            print("Errore! Inserisci una data valida e nel formato corretto. (Es. 2026-01-14)")
    while True:
        try:
            importo_spesa = float(input("Inserisci l'importo della spesa effettuata: ").replace(",", "."))
            importo_spesa = round(importo_spesa, 2)
            if importo_spesa <= 0:
                print("Errore! Inserisci un importo superiore a zero.\n")
            else:
                break
        except ValueError:
            print("Errore! Importo non valido, inserisci un importo corretto (Es. 29,99)\n")
    
    
    cat_spesa = str(input("Inserisci la categoria su cui è stata effettuata la spesa: ")).strip().upper()
    cur.execute(
        "SELECT * FROM CATEGORIE WHERE nome_cat = ?",
        (cat_spesa,)
    )
    verifica_cat_spesa = cur.fetchone()
    while True:
        if verifica_cat_spesa is None:
            cat_spesa = str(input("Errore! Inserisci una categoria esistente o premere Invio per annullare l'operazione: ")).strip().upper()
        if cat_spesa == "":
            print("Operazione di inserimento nuova spesa annullata.")
            return
        else:
            cur.execute(
                "SELECT * FROM CATEGORIE WHERE nome_cat = ?",
                (cat_spesa,)
            )
            verifica_cat_spesa = cur.fetchone()
            if verifica_cat_spesa is not None:
                break

    descrizione_spesa = str(input("Descrivi la spesa effettuata: (Facoltativo. Premi Invio per saltare.)   ")).strip()
    if descrizione_spesa == "":
        descrizione_spesa = None
    print("\nSpesa inserita correttamente!  CATEGORIA:", cat_spesa , "  DATA:", data_spesa, "  IMPORTO:", str(importo_spesa).replace(".", ","), "€  DESCRIZIONE:", str(descrizione_spesa).replace("None","//"))
    
    cur.execute(
        "INSERT INTO SPESE (data, importo_spesa, descrizione, cat_spesa) VALUES (?, ?, ?, ?)",
        (data_spesa, importo_spesa, descrizione_spesa, cat_spesa)
    )
    conn.commit()


#CREAZIONE DELLA FUNZIONE inserisci_budget() per l'inserimento o l'aggiornamento di un nuovo budget nel db
mesi = ["01", "GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO", "LUGLIO", "AGOSTO", "SETTEMBRE", "OTTOBRE", "NOVEMBRE", "DICEMBRE", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
def inserisci_budget():
    while True:
        try:
            anno_budget = int(input("\nInserisci l'anno del budget: "))
            while True:
                if anno_budget <1800 or anno_budget > 2200:
                    anno_budget = int(input("Errore! Inserisci un anno corretto. (1800-2200)   "))
                else:
                    break
            break    
        except ValueError:
            print("Errore! Inserisci un valore corretto.")
        
    mese_budget = str(input("Inserisci il mese su cui stabilire il budget: ")).upper().strip()
    while mese_budget not in mesi:
        mese_budget = str(input("Errore! Inserisci un mese corretto su cui stabilire il budget: (Es. Aprile)    ")).upper().strip()

    if mese_budget in ("GENNAIO", "01"):
        mese_budget = 1
    elif mese_budget in ("FEBBRAIO", "02"):
        mese_budget = 2
    elif mese_budget in ("MARZO", "03"):
        mese_budget = 3
    elif mese_budget in ("APRILE", "04"):
        mese_budget = 4
    elif mese_budget in ("MAGGIO", "05"):
        mese_budget = 5
    elif mese_budget in ("GIUGNO", "06"):
        mese_budget = 6
    elif mese_budget in ("LUGLIO", "07"):
        mese_budget = 7
    elif mese_budget in ("AGOSTO", "08"):
        mese_budget = 8
    elif mese_budget in ("SETTEMBRE", "09"):
        mese_budget = 9
    elif mese_budget in ("OTTOBRE", "10"):
        mese_budget = 10
    elif mese_budget in ("NOVEMBRE", "11"):
        mese_budget = 11
    elif mese_budget in ("DICEMBRE", "12"):
        mese_budget = 12

    cat_budget = str(input("Inserisci la categoria su cui si vuole impostare il budget: ")).strip().upper()
    cur.execute(
        "SELECT * FROM CATEGORIE WHERE nome_cat = ?",
        (cat_budget,)
    )
    verifica_cat_budget = cur.fetchone()
    while True:
        if verifica_cat_budget is None:
            cat_budget = str(input("Errore! Inserisci una categoria esistente o premere Invio per annullare l'operazione: ")).strip().upper()
        if cat_budget == "":
            print("Operazione di inserimento budget annullata.")
            return
        else:
            cur.execute(
                "SELECT * FROM CATEGORIE WHERE nome_cat = ?",
                (cat_budget,)
            )
            verifica_cat_budget = cur.fetchone()
            if verifica_cat_budget is not None:
                break
    cur.execute(
    "SELECT * FROM BUDGET WHERE anno = ? AND mese = ? AND cat_budget = ?",
    (anno_budget, mese_budget, cat_budget)
    )
    if cur.fetchone() is not None:
        aggiorna_budget = input("ATTENZIONE! Esiste già un budget per questo mese, anno e categoria. Vuoi aggiornare il budget? (S/N)   ").strip().upper()
        while True:
            if aggiorna_budget == "S":
                while True:
                    try:
                        importo = float(input("Inserisci il budget: ").replace(",", "."))
                        if importo <= 0:
                            print("Errore! Inserisci un budget maggiore di zero.")
                        else:
                            cur.execute(
                                "UPDATE BUDGET SET importo_budget = ? WHERE anno = ? AND mese = ? AND cat_budget = ?",
                                (importo, anno_budget, mese_budget, cat_budget)
                            )
                            conn.commit()
                        return
                    except ValueError:
                        print("Errore! Inserisci un valore corretto. (Es.2190,50)")
            elif aggiorna_budget == "N":
                return
            else:
                aggiorna_budget = input("Errore! Inserisci 'S' per aggiornare il budget o 'N' per annullare l'operazione:  ")
    else:
        while True:
            try:
                importo = float(input("Inserisci il budget: ").replace(",", "."))
                if importo <= 0:
                    print("Errore! Inserisci un budget maggiore di zero.")
                else:
                    break
            except ValueError:
                print("Errore! Inserisci un valore corretto. (Es.2190,50)")
        cur.execute(
            "INSERT INTO BUDGET (mese, anno, importo_budget, cat_budget) VALUES (?, ?, ?, ?)",
            (mese_budget, anno_budget, importo, cat_budget)
        )
        conn.commit()
        print("\nBudget di", str(importo)+" € per la categoria", cat_budget, "inserito correttamente per il mese di", mesi[mese_budget],"!")


#CREAZIONE DELLA FUNZIONE tot_spese_per_cat() per la lettura dal db della somma di tutte le spese per ogni categoria
def tot_spese_per_cat():
    cur.execute(
        "SELECT cat_spesa, SUM(importo_spesa) AS totale_spese_per_cat FROM SPESE GROUP BY cat_spesa"
    )
    riga = cur.fetchall()
    print("\nTOTALE DELLE SPESE PER CATEGORIA:")
    print("""
CATEGORIA            | TOTALE SPESO
—————————————————————|——————————————————————————————————————""")
    for categoria, totale_spese_per_cat in riga:
        print(str(categoria).ljust(20),"|", str(round(totale_spese_per_cat, 2)).replace(".",",")+" €"),


#CREAZIONE DELLA FUNZIONE spese_mensili_vs_budget() per la lettura della somma delle spese per ogni categoria relativa al mese e anno qualora fosse stato impostato un budget per lo stesso
def spese_mensili_vs_budget():
    print("\n\nSPESE MENSILI VS BUDGET:")
    cur.execute(
            "SELECT cat_budget, mese, anno, SUM(importo_spesa) AS totale_speso, importo_budget FROM SPESE LEFT JOIN BUDGET ON cat_spesa = cat_budget WHERE data LIKE anno || '-' || printf('%02d', mese) || '-%' GROUP BY cat_budget, mese, anno ORDER BY cat_budget, anno, mese"
    )
    riga = cur.fetchall()
    
    print("""
CATEGORIA            | MESE + ANNO            | TOTALE SPESO           | BUDGET                 | STATO 
—————————————————————|————————————————————————|————————————————————————|————————————————————————|——————————————————————————""")
    for cat_budget, mese, anno, totale_speso, importo_budget in riga:
        if totale_speso > importo_budget:
            print(str(cat_budget).ljust(20),"|", str(str(mesi[mese]).ljust(10) + "" + str(anno)).ljust(22), "|", str(str(round(float(totale_speso), 2))+" €").ljust(22), "|", str(str(importo_budget)+" €").ljust(22), "| SUPERAMENTO BUDGET")
        else:
            print(str(cat_budget).ljust(20),"|", str(str(mesi[mese]).ljust(10) + "" + str(anno)).ljust(22), "|", str(str(round(float(totale_speso), 2))+" €").ljust(22), "|", str(str(importo_budget)+" €").ljust(22), "| OK")


#CREAZIONE DELLA FUNZIONE tot_spese_per_cat() per la lettura dal db dell'elenco tutte le spese effettuate ordinate per data
def elenco_di_tutte_le_spese():
    print("\nELENCO COMPLETO DI TUTTE LE SPESE PER CATEGORIA:")
    cur.execute(
        "SELECT data, importo_spesa, descrizione, cat_spesa FROM SPESE ORDER BY data"
    )
    riga = cur.fetchall()
    print("""
DATA           | CATEGORIA            | IMPORTO                | DESCRIZIONE
———————————————|——————————————————————|————————————————————————|——————————————————————————————————————————————————————————""")
    for data, importo_spesa, descrizione, cat_spesa in riga:
        print(str(data).ljust(14),"|", str(cat_spesa).ljust(20), "|", str(str(importo_spesa)+" €").ljust(22), "|", str(descrizione).replace("None", "\\\\"))


menu()
scelta = input("Inserisci la tua scelta: ").strip()

#CREAZIONE DEL CICLO del programma con menu' e sottomenu' implementato con match - case'x' (Funzionamento equivalente allo SWITCH in linguaggio C)
while True:
    match scelta:
        case "1":
            print("""
CATEGORIE PRESENTI NEL DATABASE:
——————————————————————————————————————————""")
            cur.execute(
                "SELECT nome_cat FROM CATEGORIE ORDER BY nome_cat"
            )
            riga = cur.fetchall()
            if riga:
                for (nome_cat,) in riga:
                    print(nome_cat)
            else:
                print("\\\\ Nessuna categoria")
            while True:
                sn = str(input("\nVuoi inserire una nuova categoria? (S/N)  ")).strip().upper()
                if sn == "S":
                    inserisci_cat()
                    scelta = str(nuova_scelta())
                    break
                elif sn == "N":
                    scelta = str(nuova_scelta())
                    break
                else:
                    print("Errore! Inserisci 'S' per creare una categoria o 'N' per tornare al menu' principale.")  
        case "2":
            inserisci_spesa()
            scelta = str(nuova_scelta())
        case "3":
            print("\nBUDGET INSERITI:")
            print("""
CATEGORIA            | MESE + ANNO            | BUDGET IMPOSTATO 
—————————————————————|————————————————————————|——————————————————————————————————————""")
            cur.execute(
                "SELECT cat_budget, mese, anno, importo_budget FROM BUDGET ORDER BY cat_budget, anno, mese"
            )
            riga = cur.fetchall()
            for cat_budget, mese, anno, importo_budget in riga:
                print(str(cat_budget).ljust(20),"|", str(str(mesi[mese]).ljust(10) + "" + str(anno)).ljust(22), "|", str(round(float(importo_budget), 2))+" €")
            while True:
                sn = str(input("\nVuoi impostare un nuovo budget o aggiornarne uno esistente? (S/N)  ")).strip().upper()
                if sn == "S":
                    inserisci_budget()
                    scelta = str(nuova_scelta()).strip()
                    break
                elif sn == "N":
                    scelta = str(nuova_scelta()).strip()
                    break
                else:
                    print("Errore! Inserisci 'S' per inserire/aggiornare un budget o 'N' per tornare al menu' principale.")
        case "4":
            menu_report()
            scelta_r = input("Inserisci il report che vuoi consultare: ").strip()
            while True:
                match scelta_r:
                    case "1":
                        tot_spese_per_cat()
                        scelta_r = str(nuova_scelta_report()).strip()
                    case "2":
                        spese_mensili_vs_budget()
                        scelta_r = str(nuova_scelta_report()).strip()
                    case "3":
                        elenco_di_tutte_le_spese()
                        scelta_r = str(nuova_scelta_report()).strip()
                    case "4":
                        break
                    case _:
                        print("Scelta non valida")
                        scelta_r = str(input("Inserisci una nuova scelta (1-4): ")).strip()
            scelta = str(nuova_scelta()).strip()
        case "5":
            print("\nBuona giornata!\n\n")
            break
        case _:
            print("Errore! Scelta non valida.")
            scelta = str(input("Inserisci una nuova scelta (1-5): ")).strip()
