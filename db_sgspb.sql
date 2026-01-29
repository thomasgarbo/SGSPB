-- File SQL per la creazione del database

CREATE TABLE IF NOT EXISTS CATEGORIE (
            nome_cat VARCHAR(50) PRIMARY KEY UNIQUE NOT NULL
        );

CREATE TABLE IF NOT EXISTS BUDGET (
            n_budget INTEGER PRIMARY KEY AUTOINCREMENT,
            anno INTEGER NOT NULL,
            mese INTEGER NOT NULL,
            importo_budget FLOAT NOT NULL CHECK (importo_budget>0),
            cat_budget VARCHAR(50) NOT NULL,
            FOREIGN KEY (cat_budget) REFERENCES CATEGORIE (nome_cat),
            UNIQUE (anno, mese, cat_budget)
        );

CREATE TABLE IF NOT EXISTS SPESE (
            n_spesa INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            importo_spesa NUMERIC(50,2) NOT NULL CHECK (importo_spesa>0),
            descrizione VARCHAR(200),
            cat_spesa VARCHAR(50) NOT NULL,
            FOREIGN KEY (cat_spesa) REFERENCES CATEGORIE (nome_cat)
        );
