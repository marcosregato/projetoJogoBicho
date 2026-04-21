"""
Configurações e constantes do sistema Jogo do Bicho
"""

from pathlib import Path

# Configurações do banco de dados
DB_PATH = Path(__file__).parent / "resultados.db"

# URLs e configurações de scraping
BASE_URL = "https://www.ojogodobicho.com/deu_no_poste.htm"
SCRAPING_TIMEOUT = 10
IMPLICIT_WAIT = 10

# Dicionários de dados do jogo
DIC_HORARIO = {
    'PPT': '9:00',
    'PTM': '11:00',
    'PT': '14:00',
    'PTV': '16:00',
    'PTN': '18:00',
    'COR': '21:00'
}

DIC_BICHOS = {
    1: 'avestruz', 2: 'aguia', 3: 'burro', 4: 'borboleta', 5: 'cachorro',
    6: 'cabra', 7: 'carneiro', 8: 'camelo', 9: 'cobra', 10: 'coelho',
    11: 'cavalo', 12: 'elefante', 13: 'galo', 14: 'gato', 15: 'jacare',
    16: 'leao', 17: 'macaco', 18: 'porco', 19: 'pavao', 20: 'peru',
    21: 'touro', 22: 'tigre', 23: 'urso', 24: 'veado', 25: 'vaca'
}

DIC_GRUPO_BICHOS = {
    'avestruz': [1, 2, 3, 4], 'aguia': [5, 6, 7, 8], 'burro': [9, 10, 11, 12],
    'borboleta': [13, 14, 15, 16], 'cachorro': [17, 18, 19, 20], 'cabra': [21, 22, 23, 24],
    'carneiro': [25, 26, 27, 28], 'camelo': [29, 30, 31, 32], 'cobra': [33, 34, 35, 36],
    'coelho': [37, 38, 39, 40], 'cavalo': [41, 42, 43, 44], 'elefante': [45, 46, 47, 48],
    'galo': [49, 50, 51, 52], 'gato': [53, 54, 55, 56], 'jacare': [57, 58, 59, 60],
    'leao': [61, 62, 63, 64], 'macaco': [65, 66, 67, 68], 'porco': [69, 70, 71, 72],
    'pavao': [73, 74, 75, 76], 'peru': [77, 78, 79, 80], 'touro': [81, 82, 83, 84],
    'tigre': [85, 86, 87, 88], 'urso': [89, 90, 91, 92], 'veado': [93, 94, 95, 96],
    'vaca': [97, 98, 99, 00]
}

# Horários disponíveis para scraping
SIGLA_HORARIO = ['PPT', 'PTM', 'PT', 'PTV', 'PTN', 'COR']
