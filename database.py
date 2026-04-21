"""
Módulo de gerenciamento do banco de dados SQLite
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from config import DB_PATH


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """
    Estabelece conexão com o banco de dados SQLite
    """
    conn = sqlite3.connect(str(db_path), timeout=10)
    conn.row_factory = sqlite3.Row  # permite acesso por nome de coluna
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Inicializa as tabelas do banco de dados
    """
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS datajogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dt_jogo VARCHAR(10) NOT NULL,
        horario VARCHAR(5),
        sigla_hora VARCHAR(3)
    );

    CREATE TABLE IF NOT EXISTS resultjogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_id INTEGER,
        numMilhar VARCHAR(4) NOT NULL,
        numCentena VARCHAR(3) NOT NULL,
        numDezena VARCHAR(2) NOT NULL,
        FOREIGN KEY (data_id) REFERENCES datajogo(id)
    );

    CREATE TABLE IF NOT EXISTS grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_id INTEGER,
        result_id INTEGER,
        premio VARCHAR(20),
        animal VARCHAR(10),
        FOREIGN KEY (data_id) REFERENCES datajogo(id),
        FOREIGN KEY (result_id) REFERENCES resultjogo(id)
    );
    """)


def insert_datajogo(conn: sqlite3.Connection, dt_jogo: str, 
                   horario: str = None, sigla_hora: str = None) -> int:
    """
    Insere registro na tabela datajogo e retorna o ID inserido
    """
    cursor = conn.execute(
        "INSERT INTO datajogo (dt_jogo, horario, sigla_hora) VALUES (?, ?, ?)",
        (dt_jogo, horario, sigla_hora)
    )
    conn.commit()
    return cursor.lastrowid


def insert_numero(conn: sqlite3.Connection, data_id: int, 
                 grupomilhar: str, grupocentena: str, grupodezena: str) -> int:
    """
    Insere registro na tabela resultjogo e retorna o ID inserido
    """
    cursor = conn.execute(
        "INSERT INTO resultjogo (data_id, numMilhar, numCentena, numDezena) VALUES (?, ?, ?, ?)",
        (data_id, grupomilhar, grupocentena, grupodezena)
    )
    conn.commit()
    return cursor.lastrowid


def insert_grupo(conn: sqlite3.Connection, data_id: int, result_id: int, 
                premio: str, animal: str) -> int:
    """
    Insere registro na tabela grupo e retorna o ID inserido
    """
    cursor = conn.execute(
        "INSERT INTO grupo (data_id, result_id, premio, animal) VALUES (?, ?, ?, ?)",
        (data_id, result_id, premio, animal)
    )
    conn.commit()
    return cursor.lastrowid


def fetch_results(conn: sqlite3.Connection, limit: int = None) -> List[Dict]:
    """
    Busca resultados da tabela resultjogo
    """
    query = "SELECT * FROM resultjogo ORDER BY id DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    cur = conn.execute(query)
    return [dict(row) for row in cur.fetchall()]


def fetch_all_results_with_details(conn: sqlite3.Connection) -> List[Dict]:
    """
    Busca todos os resultados com detalhes completos (JOIN entre tabelas)
    """
    query = """
    SELECT 
        d.dt_jogo, d.horario, d.sigla_hora, 
        r.numMilhar, r.numCentena, r.numDezena, 
        g.premio, g.animal 
    FROM datajogo d 
    INNER JOIN grupo g ON d.id = g.data_id 
    INNER JOIN resultjogo r ON g.result_id = r.id 
    ORDER BY d.id DESC, g.id DESC
    """
    
    cur = conn.execute(query)
    return [dict(row) for row in cur.fetchall()]


def update_datajogo(conn: sqlite3.Connection, id: int, dt_jogo: str, 
                   sigla_hora: str) -> None:
    """
    Atualiza registro na tabela datajogo
    """
    conn.execute(
        "UPDATE datajogo SET dt_jogo = ?, sigla_hora = ? WHERE id = ?",
        (dt_jogo, sigla_hora, id)
    )
    conn.commit()


def update_resultjogo(conn: sqlite3.Connection, id: int, data_id: int, 
                    numMilhar: str, numCentena: str, numDezena: str) -> None:
    """
    Atualiza registro na tabela resultjogo
    """
    conn.execute(
        "UPDATE resultjogo SET data_id = ?, numMilhar = ?, numCentena = ?, numDezena = ? WHERE id = ?",
        (data_id, numMilhar, numCentena, numDezena, id)
    )
    conn.commit()


def update_grupo(conn: sqlite3.Connection, id: int, data_id: int, result_id: int, 
               premio: str, animal: str) -> None:
    """
    Atualiza registro na tabela grupo
    """
    conn.execute(
        "UPDATE grupo SET data_id = ?, result_id = ?, premio = ?, animal = ? WHERE id = ?",
        (data_id, result_id, premio, animal, id)
    )
    conn.commit()
