"""
Módulo principal do sistema Jogo do Bicho
Mantido para compatibilidade, mas agora usa os novos módulos modulares
"""

from datetime import datetime
import sys

# Importações dos novos módulos
from config import DIC_HORARIO
from database import get_connection, init_db, insert_datajogo, insert_numero, insert_grupo, fetch_results
from scraper import JogoBichoScraper, salvar_resultados_no_banco

# Mantém compatibilidade com código antigo
dicHorario = DIC_HORARIO
sigla_horario = ['PPT','PTM','PT','PTV']

# Funções legadas para compatibilidade - agora usam os novos módulos
def getInfoResult(driver=None):
    """
    Função legada para compatibilidade
    """
    with JogoBichoScraper() as scraper:
        return scraper.get_resultados()

def getDataAtual(sigla_procurada):
    """
    Obtém a sigla do horário atual baseado na sigla procurada
    """
    return dicHorario.get(sigla_procurada)




if __name__ == "__main__":
    import sys
    
    # Verifica se o modo de scraping foi solicitado
    modo_scraping = len(sys.argv) > 1 and sys.argv[1] == "--scraping"
    
    with get_connection() as conn: 
        init_db(conn)
        
        if modo_scraping:
            print("Iniciando modo scraping...")
            try:
                resultados = getInfoResult()
                if resultados:
                    salvar_resultados_no_banco(conn, resultados)
                    print("Scraping concluído com sucesso!")
                else:
                    print("Nenhum resultado encontrado no scraping")
            except Exception as e:
                print(f"Erro durante scraping: {e}")
        else:
            # Modo teste (comportamento original)
            print("Inserindo dados de teste...")
            
            # Obtém data atual formatada
            now = datetime.now()
            data = now.strftime("%d/%m/%Y")
            
            # Define sigla fixa para teste
            sigla_hora = 'PT'
            horario = dicHorario.get(sigla_hora, '14:00')

            # Inserir dados com relacionamentos corretos
            data_id = insert_datajogo(conn, data, horario, sigla_hora)
            result_id = insert_numero(conn, data_id, "0123", "123", "23")
            insert_grupo(conn, data_id, result_id, "1º", "avestruz")
            
            print(f"Dados inseridos para {data} - {sigla_hora} ({horario}). Resultados no banco:")
            print(fetch_results(conn))
