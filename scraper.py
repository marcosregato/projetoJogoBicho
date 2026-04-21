"""
Módulo de web scraping para resultados do Jogo do Bicho
"""

from datetime import datetime
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config import BASE_URL, IMPLICIT_WAIT, DIC_HORARIO, DIC_GRUPO_BICHOS


class JogoBichoScraper:
    """
    Classe responsável por extrair resultados do Jogo do Bicho
    """
    
    def __init__(self, headless: bool = True):
        """
        Inicializa o scraper
        """
        self.driver = None
        self.headless = headless
        self._init_driver()
    
    def _init_driver(self):
        """
        Inicializa o WebDriver Chrome
        """
        try:
            options = webdriver.ChromeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            self.driver = webdriver.Chrome(options=options)
            self.driver.implicitly_wait(IMPLICIT_WAIT)
        except Exception as e:
            raise Exception(f"Erro ao inicializar WebDriver: {e}")
    
    def get_resultados(self) -> Optional[List[Dict]]:
        """
        Extrai resultados do site e retorna dados estruturados
        """
        if not self.driver:
            self._init_driver()
        
        try:
            self.driver.get(BASE_URL)
            return self._extract_table_data()
        except TimeoutException:
            print("Timeout ao carregar a página")
            return None
        except Exception as e:
            print(f"Erro ao acessar site: {e}")
            return None
    
    def _extract_table_data(self) -> Optional[List[Dict]]:
        """
        Extrai dados da tabela de resultados
        """
        try:
            table = self.driver.find_element(By.XPATH, "//table[@class='twelve']")
            rows = table.find_elements(By.TAG_NAME, "tr")
            print(f"Encontradas {len(rows)} linhas na tabela")
        except NoSuchElementException:
            print("Erro: Tabela de resultados não encontrada.")
            return None
        except Exception as e:
            print(f"Erro inesperado ao encontrar tabela: {e}")
            return None
        
        resultados = []
        
        for i, row in enumerate(rows):
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if not cols:
                    cols = row.find_elements(By.TAG_NAME, "th")

                row_data = [cell.text.strip() for cell in cols if cell.text.strip()]
                
                if row_data:
                    resultado = self._processar_linha_resultado(row_data)
                    if resultado:
                        resultados.append(resultado)
            except Exception as e:
                print(f"Erro ao processar linha {i}: {e}")
                continue
        
        return resultados
    
    def _processar_linha_resultado(self, row_data: List[str]) -> Optional[Dict]:
        """
        Processa uma linha de resultado e extrai dados estruturados
        """
        if len(row_data) < 2:
            return None
        
        try:
            premio = row_data[0] if row_data[0] else ""
            resultado_completo = row_data[1] if len(row_data) > 1 else ""
            animal = row_data[2] if len(row_data) > 2 else ""
            
            # Extrai números do resultado (formato: "1234 - 56")
            if " - " in resultado_completo:
                partes = resultado_completo.split(" - ")
                milhar = partes[0].strip()
                grupo_num = partes[1].strip() if len(partes) > 1 else ""
                
                # Valida e formata números
                if milhar.isdigit() and len(milhar) == 4:
                    centena = milhar[1:4]
                    dezena = milhar[2:4]
                    
                    # Determina o animal baseado no grupo
                    animal_determinado = self._determinar_animal(grupo_num)
                    
                    return {
                        'premio': premio,
                        'milhar': milhar,
                        'centena': centena,
                        'dezena': dezena,
                        'animal': animal or animal_determinado,
                        'grupo': grupo_num
                    }
        except Exception as e:
            print(f"Erro ao processar linha {row_data}: {e}")
        
        return None
    
    def _determinar_animal(self, grupo_numero: str) -> Optional[str]:
        """
        Determina o animal baseado no número do grupo (00-99)
        """
        if not grupo_numero or not grupo_numero.isdigit():
            return None
        
        grupo = int(grupo_numero) % 100
        
        # Mapeamento reverso: encontrar o animal baseado no grupo
        for animal, numeros in DIC_GRUPO_BICHOS.items():
            if grupo in numeros:
                return animal
        
        return None
    
    def get_horario_atual(self) -> Optional[str]:
        """
        Determina o horário/sigla atual baseado na hora atual
        """
        agora = datetime.now()
        hora_atual = agora.strftime("%H:%M")
        
        for sigla, horario in DIC_HORARIO.items():
            if horario == hora_atual:
                return sigla
        
        # Lógica para encontrar o horário mais próximo
        horas_ordenadas = sorted(DIC_HORARIO.items(), key=lambda x: x[1])
        
        for sigla, horario in horas_ordenadas:
            if hora_atual <= horario:
                return sigla
        
        # Se passar de todos os horários, retorna o primeiro do dia seguinte
        return horas_ordenadas[0][0] if horas_ordenadas else None
    
    def close(self):
        """
        Fecha o WebDriver
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def salvar_resultados_no_banco(conn, resultados: List[Dict], sigla_hora: str = 'PT'):
    """
    Salva os resultados extraídos no banco de dados
    """
    from database import insert_datajogo, insert_numero, insert_grupo
    
    if not resultados:
        print("Nenhum resultado para salvar")
        return
    
    data_atual = datetime.now().strftime("%d/%m/%Y")
    horario = DIC_HORARIO.get(sigla_hora, '14:00')
    
    try:
        # Inserir registro na tabela datajogo
        data_id = insert_datajogo(conn, data_atual, horario, sigla_hora)
        
        # Inserir cada resultado
        for resultado in resultados:
            result_id = insert_numero(
                conn, data_id, 
                resultado['milhar'], 
                resultado['centena'], 
                resultado['dezena']
            )
            
            insert_grupo(
                conn, data_id, result_id,
                resultado['premio'], 
                resultado['animal']
            )
        
        print(f"Salvos {len(resultados)} resultados para {data_atual} - {sigla_hora}")
        
    except Exception as e:
        print(f"Erro ao salvar resultados no banco: {e}")
        conn.rollback()
        raise
