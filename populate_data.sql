-- Arquivo: populate_data.sql
-- Descrição: Script para popular o banco de dados com 300 registros fictícios.
-- Uso: sqlite3 resultados.db < populate_data.sql

BEGIN TRANSACTION;

-- 1. Inserir 300 registros na tabela datajogo
-- Utiliza CTE recursiva para gerar uma sequência de 1 a 300 e datas retroativas
WITH RECURSIVE sequence(i) AS (
    SELECT 1
    UNION ALL
    SELECT i + 1 FROM sequence WHERE i < 300
)
INSERT INTO datajogo (dt_jogo, sigla_hora)
SELECT 
    strftime('%d/%m/%Y', date('now', '-' || i || ' days')),
    CASE (i % 6)
        WHEN 0 THEN 'PPT'
        WHEN 1 THEN 'PTM'
        WHEN 2 THEN 'PT'
        WHEN 3 THEN 'PTV'
        WHEN 4 THEN 'PTN'
        ELSE 'COR'
    END
FROM sequence;

-- 2. Inserir registros na tabela resultjogo para cada datajogo inserida
-- Gera números aleatórios para Milhar, Centena e Dezena
-- Gera Milhar aleatório e deriva Centena e Dezena para consistência
INSERT INTO resultjogo (data_id, numMilhar, numCentena, numDezena)
SELECT 
    id,
    m,
    substr(m, 2, 3), -- Centena (digitos 2,3,4 do milhar)
    substr(m, 3, 2)  -- Dezena (digitos 3,4 do milhar)
FROM (
    SELECT 
        id, 
        printf('%04d', abs(random()) % 10000) as m 
    FROM datajogo
);

-- 3. Inserir registros na tabela grupo para cada resultjogo
-- Seleciona um animal aleatório para o 1º Prêmio
INSERT INTO grupo (data_id, result_id, premio, animal)
SELECT 
    data_id,
    id,
    '1º Premio',
    CASE (abs(random()) % 25)
        WHEN 0 THEN 'Avestruz'
        WHEN 1 THEN 'Águia'
        WHEN 2 THEN 'Burro'
        WHEN 3 THEN 'Borboleta'
        WHEN 4 THEN 'Cachorro'
        WHEN 5 THEN 'Cabra'
        WHEN 6 THEN 'Carneiro'
        WHEN 7 THEN 'Camelo'
        WHEN 8 THEN 'Cobra'
        WHEN 9 THEN 'Coelho'
        WHEN 10 THEN 'Cavalo'
        WHEN 11 THEN 'Elefante'
        WHEN 12 THEN 'Galo'
        WHEN 13 THEN 'Gato'
        WHEN 14 THEN 'Jacaré'
        WHEN 15 THEN 'Leão'
        WHEN 16 THEN 'Macaco'
        WHEN 17 THEN 'Porco'
        WHEN 18 THEN 'Pavão'
        WHEN 19 THEN 'Peru'
        WHEN 20 THEN 'Touro'
        WHEN 21 THEN 'Tigre'
        WHEN 22 THEN 'Urso'
        WHEN 23 THEN 'Veado'
        ELSE 'Vaca'
    END
FROM resultjogo;

COMMIT;