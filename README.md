# SGSPB (Sistema di Gestione delle Spese e del Budget)

* PROGETTO FINALE DI PROGRAMMAZIONE: Sistema di Gestione delle Spese e del Budget
* CORSO: Fondamenti di Informatica 
* STUDENTE: Thomas Garbo
* MATRICOLA: 0082500049

————————————————————————————————

> Requisiti per l'esecuzione:

- Compilatore / Interprete necessario:
    Python 3 (Versione aggiornata - 3.8 o superiore / es: Python 3.14.2)

- Librerie standard utilizzate:
    "sqlite3" (Gestione del DB con SQLite) / "datetime" (Gestione delle date)

————————————————————————————————

> Istruzioni dettagliate per eseguire il programma:

- Istruzioni di compilazione:
    Nessuna compilazione necessaria in quanto scritto in Python ed eseguito con interprete

- Istruzione di avvio del programma: 
    Aprire il terminale, verificare di avere Python installato e con una versione recente utilizzando il comando: 'python --version' (oppure 'python3 --version'), posizionarsi da terminale nella cartella contenente il file main.py 

- Comando esatto da eseguire:
    Per avviare il programma digitare su terminale:  'python main.py' (oppure 'python3 main.py')

————————————————————————————————

> Info utili:

* Il programma è stato sviluppato in Python + SQLite e viene eseguito tramite console, le sue funzionalità sono per la 'gestione delle spese personali e di budget' inseriti dall'utente, scegliendo ogni operazione tramite menù. Tutti i dati inseriti vengono controllati prima di essere inseriti permanentemente nel database.

* Il file e le tabelle del database relazionale SQLite chiamato db_sgspb.db vengono creati al primo avvio del programma (qualora non esistano già) ed i dati inseriti successivamente resteranno salvati in modo permanente nel db generato localmente.

* All'interno del branches 'src' in GitHub è stato caricato il programma completo (main.py) ed il file del database (db_sgspb.db) che è stato creato per registrare il video dimostrativo (demo) del programma. Per creare od inizializzare il proprio DB è sufficiente eliminare il file db_sgspb.db e riavviare il programma.

* Non sono necessari software aggiuntivi o librerie esterne per l'esecuzione del programma, solo aver installato sul proprio dispositivo una versione recente di Python.
