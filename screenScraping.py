from datetime import datetime

from pathlib import Path
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


dicHorario  ={'PPT':'9:00',
              'PTM':'11:00',
              'PT':'14:00',
              'PTV':'16:00',
              'PTN':'18:00',
              'COR':'21:00'}


dicbichos = { 1: 'avestruz',
              2: 'aguia',
              3: 'burro',
              4: 'borboleta',
              5: 'cachorro',
              6: 'cabra',
              7: 'carneiro',
              8: 'camelo',
              9: 'cobra',
              10: 'coelho',
              11: 'cavalo',
              12: 'elefante',
              13: 'galo',
              14: 'gato',
              15: 'jacare',
              16: 'leao',
              17: 'macaco',
              18: 'porco',
              19: 'pavao',
              20: 'peru',
              21: 'touro',
              22: 'tigre',
              23: 'urso',
              24: 'veado',
              25: 'vaca'}

dicgrupobichos = { 'avestruz': [1, 2, 3, 4],
              'aguia': [5, 6, 7, 8],
              'burro': [9, 10, 11, 12],
              'borboleta': [13, 14, 15, 16],
              'cachorro': [17, 18, 19, 20],
              'cabra': [21, 22, 23, 24],
              'carneiro': [25, 26, 27, 28],
              'camelo': [29, 30, 31, 32],
              'cobra': [33, 34, 35, 36],
              'coelho': [37, 38, 39, 40],
              'cavalo': [41, 42, 43, 44],
              'elefante': [45, 46, 47, 48],
              'galo': [49, 50, 51, 52],
              'gato': [53, 54, 55, 56],
              'jacare': [57, 58, 59, 60],
              'leao': [61, 62, 63, 64],
              'macaco': [65, 66, 67, 68],
              'porco': [69, 70, 71, 72],
              'pavao': [73, 74, 75, 76],
              'peru': [77, 78, 79, 80],
              'touro': [81, 82, 83, 84],
              'tigre': [85, 86, 87, 88],
              'urso': [89, 90, 91, 92],
              'veado': [93, 94, 95, 96],
              'vaca': [97, 98, 99, 00]}

sigla_horario = ['PPT','PTM','PT','PTV']

DB_PATH = Path(__file__).parent / "resultados.db"

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path), timeout=10)
    conn.row_factory = sqlite3.Row  # permite acesso por nome de coluna
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS datajogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dt_jogo VARCHAR(10) NOT NULL,
    sigla_hora VARCHAR(3)
    );

    CREATE TABLE IF NOT EXISTS resultjogo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_id INTEGER,
        numMilhar VARCHAR(4) NOT NULL,
        numCentena VARCHAR(3) NOT NULL,
        numDezena VARCHAR(2) NOT NULL,
        FOREIGN KEY (data_id) REFERENCES dataJogo(id)
    );

    CREATE TABLE IF NOT EXISTS grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_id INTEGER,
        result_id INTEGER,
        premio VARCHAR(20),
        animal VARCHAR(10),
        FOREIGN KEY (data_id) REFERENCES dataJogo(id),
        FOREIGN KEY (result_id) REFERENCES resultjogo(id)
    );
    """)
    
# PRIMEIRA PARTE

def getInfoResult(driver=None):

    if driver is None:
        driver = webdriver.Chrome()
        driver.get('https://www.ojogodobicho.com/deu_no_poste.htm')

    try:
        table = driver.find_element(By.XPATH, "//table[@class='twelve']") 
        rows = table.find_elements(By.TAG_NAME, "tr")
        print(f"Total number of rows: {len(rows)}")
    except NoSuchElementException:
        print("Erro: Tabela de resultados não encontrada.")
        return

    listInfo = []
    table_data_list = []
    for i, row in enumerate(rows):
        cols = row.find_elements(By.TAG_NAME, "td")
        if not cols:
             cols = row.find_elements(By.TAG_NAME, "th")

        row_data = [cell.text for cell in cols]
        table_data_list.append(row_data)

        if row_data:
            listInfo.append(row_data)
    fatiaNumero(table_data_list)
    #fatiaNumero(listInfo)

#def getSiglaHorario(sigla):
#    return dicHorario.get(sigla.lower())

def getDataAtual(sigla_procurada):
    
    for chave, valor in dicHorario.items():
        if chave == sigla_procurada:
            return sigla_procurada
            #break # Para
    
    '''
    data_atual = datetime.now()
    data_string = data_atual.strftime("%d/%m/%Y %H:%M")
    apenas_data = data_string[:10]
    apenas_hora = data_string[11:15]
    chave_encontrada = None
    
    for inicio, fim in intervalo:
        if inicio <= apenas_hora <= fim:

            for chave, valor in dicHorario.items():
                if valor == valor_procurado:
                    chave_encontrada = chave
                    break # Para 
    '''

    

    #return data_atual.strftime("%d/%m/%Y %H:%M:%S")

def fatiaNumero(listInfo):
    #getDataAtual()
    delimitador = '-'
    for linha in listInfo:
        for cell in linha:
            if not cell:
                continue
            parts = cell.split(delimitador) 
            valor = parts[0].strip()
            if not valor:
                continue
            if valor.isdigit():
                if len(valor) == 3:
                    value = str(valor).rjust(4, '0')
                    print("Sigla horario  => ", sigla_horario.index(value))
                    print("grupo centena => ", value[1:4])
                    print("grupo Dezena  => ", value[2:4])

                    print(parts)

                elif len(valor) >= 4:
                    print("grupo milhar  => ", valor)
                    print("grupo centena => ", valor[1:4])
                    print("grupo Dezena  => ", valor[2:4])
                else:
                    print(parts)
            else:
                if len(valor) >= 3:
                    print("grupo milhar  => ", valor)
                    print("grupo centena => ", valor[1:4])
                    print("grupo Dezena  => ", valor[2:4])
                else:
                    print(parts)



def insert_datajogo(conn: sqlite3.Connection, dt_jogo: str, sigla_hora: str) -> None:
    conn.execute(
        "INSERT INTO dataJogo (dt_jogo, sigla_hora) VALUES (?, ?)",
        (dt_jogo,sigla_hora)
    )
    conn.commit()

def insert_numero(conn: sqlite3.Connection, grupomilhar: str, grupocentena: str, grupodezena: str) -> None:
    conn.execute(
        "INSERT INTO resultjogo (numMilhar, numCentena, numDezena) VALUES (?, ?, ?)",
        (grupomilhar, grupocentena, grupodezena)
    )
    conn.commit()

def insert_grupo(conn: sqlite3.Connection, premio: str, animal: str) -> None:
    conn.execute(
        "INSERT INTO grupo (premio, animal) VALUES (?, ?)",
        (premio, animal)
    )
    conn.commit()

def update_datajogo(conn: sqlite3.Connection, id: int, dt_jogo: str, sigla_hora: str) -> None:
    conn.execute(
        "UPDATE datajogo SET dt_jogo = ?, sigla_hora = ? WHERE id = ?",
        (dt_jogo, sigla_hora, id)
    )
    conn.commit()

def update_resultjogo(conn: sqlite3.Connection, id: int, data_id: int, numMilhar: str, numCentena: str, numDezena: str) -> None:
    conn.execute(
        "UPDATE resultjogo SET data_id = ?, numMilhar = ?, numCentena = ?, numDezena = ? WHERE id = ?",
        (data_id, numMilhar, numCentena, numDezena, id)
    )
    conn.commit()

def update_grupo(conn: sqlite3.Connection, id: int, data_id: int, result_id: int, premio: str, animal: str) -> None:
    conn.execute(
        "UPDATE grupo SET data_id = ?, result_id = ?, premio = ?, animal = ? WHERE id = ?",
        (data_id, result_id, premio, animal, id)
    )
    conn.commit()

def fetch_results(conn: sqlite3.Connection):
    cur = conn.execute("SELECT * FROM resultjogo ORDER BY id DESC")
    return [dict(row) for row in cur.fetchall()]

if __name__ == "__main__":

    # Obtém data atual formatada
    now = datetime.now()
    data = now.strftime("%d/%m/%Y")
    
    # Define sigla fixa para teste (lógica de horário pode ser implementada futuramente)
    sigla_hora = 'PT'

    with get_connection() as conn: 
        init_db(conn)
        insert_datajogo(conn, data, sigla_hora)
        insert_numero(conn, "0123", "123", "23")
        insert_grupo(conn, "1º", "avestruz")
        
        print(f"Dados inseridos para {data} - {sigla_hora}. Resultados no banco:")
        print(fetch_results(conn))
