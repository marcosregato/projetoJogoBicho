import sqlite3
from pathlib import Path
import screenScraping

def main():
    # Caminho do arquivo SQL
    sql_file = Path(__file__).parent / "populate_data.sql"
    
    if not sql_file.exists():
        print(f"Erro: Arquivo {sql_file} não encontrado.")
        return

    print("Executando script de população no banco de dados...")
    
    with screenScraping.get_connection() as conn:
        screenScraping.init_db(conn)  # Garante que as tabelas existam
        with open(sql_file, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            
    print("Concluído.")

if __name__ == "__main__":
    main()