CREATE TABLE datajogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_jogo VARCHAR(10) NOT NULL,
    horario VARCHAR(5),
    sigla_hora VARCHAR(3)
);

CREATE TABLE resultjogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_id INTEGER,
    numMilhar VARCHAR(4) NOT NULL,
    numCentena VARCHAR(3) NOT NULL,
    numDezena VARCHAR(2) NOT NULL,
    FOREIGN KEY (data_id) REFERENCES datajogo(id)
);

CREATE TABLE grupo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_id INTEGER,
    result_id INTEGER,
    premio VARCHAR(20),
    animal VARCHAR(10),
    FOREIGN KEY (data_id) REFERENCES dataJogo(id),
    FOREIGN KEY (result_id) REFERENCES resultjogo(id)
);