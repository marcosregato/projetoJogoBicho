import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import screenScraping

class TestScreenScrapingMock(unittest.TestCase):

    @patch('screenScraping.fatiaNumero')
    def test_getInfoResult_com_mock(self, mock_fatiaNumero):
        """
        Testa a função getInfoResult simulando o Selenium WebDriver.
        Verifica se os dados são extraídos corretamente da tabela HTML simulada
        e passados para a função fatiaNumero.
        """
        # 1. Configurar o Mock do Driver e Elementos
        mock_driver = MagicMock()
        mock_table = MagicMock()
        mock_row_header = MagicMock()
        mock_row_data = MagicMock()
        
        # Configurar retorno do find_element para a tabela
        mock_driver.find_element.return_value = mock_table
        
        # Configurar retorno do find_elements para as linhas (tr)
        # Vamos simular 2 linhas: uma de cabeçalho e uma de dados
        mock_table.find_elements.return_value = [mock_row_header, mock_row_data]
        
        # Configurar células da linha 1 (Cabeçalho - th)
        # O código tenta 'td' primeiro, se vazio tenta 'th'
        col_h1 = MagicMock()
        col_h1.text = "Prêmio"
        col_h2 = MagicMock()
        col_h2.text = "Milhar"
        
        def side_effect_header(by, tag):
            if tag == "td": return []
            if tag == "th": return [col_h1, col_h2]
            return []
            
        mock_row_header.find_elements.side_effect = side_effect_header
        
        # Configurar células da linha 2 (Dados - td)
        col_d1 = MagicMock()
        col_d1.text = "1º"
        col_d2 = MagicMock()
        col_d2.text = "1234"
        
        # Para dados, 'td' retorna direto (comportamento padrão do mock se não definir side_effect)
        mock_row_data.find_elements.return_value = [col_d1, col_d2]

        # 2. Executar a função com o driver mockado
        screenScraping.getInfoResult(driver=mock_driver)

        # 3. Asserções
        # Verifica se buscou a tabela correta
        mock_driver.find_element.assert_called_with(By.XPATH, "//table[@class='twelve']")
        
        # Verifica se fatiaNumero foi chamado com a lista de listas esperada
        expected_list = [
            ['Prêmio', 'Milhar'],
            ['1º', '1234']
        ]
        mock_fatiaNumero.assert_called_once_with(expected_list)

    @patch('builtins.print')
    def test_getInfoResult_tabela_nao_encontrada(self, mock_print):
        """
        Testa o tratamento de exceção quando a tabela não é encontrada.
        """
        mock_driver = MagicMock()
        mock_driver.find_element.side_effect = NoSuchElementException

        screenScraping.getInfoResult(driver=mock_driver)

        mock_print.assert_any_call("Erro: Tabela de resultados não encontrada.")

if __name__ == '__main__':
    unittest.main()