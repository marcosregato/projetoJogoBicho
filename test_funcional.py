import unittest
import sqlite3
import io
import sys
import os
import screenScraping

class TestScreenScrapingFuncional(unittest.TestCase):
    def setUp(self):
        # Cria um banco de dados em memória para cada teste
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        screenScraping.init_db(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_fluxo_banco_dados(self):
        """Testa a inserção e recuperação de dados no banco."""
        
        # 1. Testar insert_datajogo
        screenScraping.insert_datajogo(self.conn, '03/01/2026', 'PT')
        cur = self.conn.execute("SELECT * FROM datajogo")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['dt_jogo'], '03/01/2026')
        self.assertEqual(row['sigla_hora'], 'PT')

        # 2. Testar insert_numero (versão atual sem data_id)
        screenScraping.insert_numero(self.conn, '1234', '234', '34')
        cur = self.conn.execute("SELECT * FROM resultjogo")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['numMilhar'], '1234')
        self.assertEqual(row['numCentena'], '234')

        # 3. Testar insert_grupo (versão atual sem data_id)
        screenScraping.insert_grupo(self.conn, '1º', 'avestruz')
        cur = self.conn.execute("SELECT * FROM grupo")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['premio'], '1º')
        self.assertEqual(row['animal'], 'avestruz')

    def test_fatiaNumero_print(self):
        """Testa se a função fatiaNumero imprime os dados corretamente."""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Simula dados vindos do scraping: ['Texto', 'Milhar - Grupo', 'Bicho']
        sample_data = [['1º Prêmio', '5678 - 20', 'Peru']]
        screenScraping.fatiaNumero(sample_data)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        # Verifica se o output contém o que esperamos
        self.assertIn("grupo milhar  =>  5678", output)
        self.assertIn("grupo centena =>  678", output)
        self.assertIn("grupo Dezena  =>  78", output)

    def test_populate_data_sql(self):
        """Testa a execução do script populate_data.sql no banco em memória."""
        sql_file = os.path.join(os.path.dirname(__file__), "populate_data.sql")
        
        if not os.path.exists(sql_file):
            self.skipTest(f"Arquivo {sql_file} não encontrado.")

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        try:
            self.conn.executescript(sql_script)
        except sqlite3.Error as e:
            self.fail(f"Falha ao executar populate_data.sql: {e}")

        # Verifica se os dados foram inseridos nas tabelas
        for table in ['datajogo', 'resultjogo', 'grupo']:
            cur = self.conn.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            self.assertGreater(count, 0, f"A tabela {table} deveria ter registros.")

if __name__ == '__main__':
    unittest.main()