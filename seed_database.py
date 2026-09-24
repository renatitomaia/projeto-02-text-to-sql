import sqlite3
import os

# Garantir que a pasta database existe
os.makedirs("database", exist_ok=True)
db_path = os.path.join("database", "db_obra.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Tabela Dimensão Obra
cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_obra (
    id_obra INTEGER PRIMARY KEY,
    nome_obra TEXT NOT NULL,
    orcamento_total REAL NOT NULL,
    cidade TEXT
);
''')

# 2. Tabela Dimensão Serviço
cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_servico (
    id_servico INTEGER PRIMARY KEY,
    nome_servico TEXT NOT NULL,
    categoria TEXT NOT NULL,
    orcamento_servico REAL NOT NULL
);
''')

# 3. Tabela Fato Planejamento
cursor.execute('''
CREATE TABLE IF NOT EXISTS fato_planejamento (
    id_planejamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_obra INTEGER,
    id_servico INTEGER,
    ano_mes TEXT,
    valor_previsto REAL,
    avanco_fisi_previsto_pct REAL,
    FOREIGN KEY(id_obra) REFERENCES dim_obra(id_obra),
    FOREIGN KEY(id_servico) REFERENCES dim_servico(id_servico)
);
''')

# 4. Tabela Fato Execução
cursor.execute('''
CREATE TABLE IF NOT EXISTS fato_execucao (
    id_execucao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_obra INTEGER,
    id_servico INTEGER,
    ano_mes TEXT,
    custo_realizado REAL,
    avanco_fisi_realizado_pct REAL,
    FOREIGN KEY(id_obra) REFERENCES dim_obra(id_obra),
    FOREIGN KEY(id_servico) REFERENCES dim_servico(id_servico)
);
''')

# Inserir Dados Demonstrativos
cursor.execute("DELETE FROM dim_obra;")
cursor.execute("DELETE FROM dim_servico;")
cursor.execute("DELETE FROM fato_planejamento;")
cursor.execute("DELETE FROM fato_execucao;")

cursor.execute("INSERT INTO dim_obra VALUES (1, 'Residencial Atlântico', 10500000.0, 'Fortaleza');")

servicos = [
    (101, 'Escavações', 'Fundações', 1318840.58),
    (102, 'Estrutura Concreto', 'Estrutura', 2130434.78),
    (103, 'Alvenaria de Vedação', 'Alvenaria', 862318.84),
    (104, 'Instalações Elétricas', 'Instalações', 500000.00),
    (105, 'Instalações Hidráulicas', 'Instalações', 500000.00),
    (106, 'Pisos e Revestimentos', 'Acabamentos', 507246.38),
]

cursor.executemany("INSERT INTO dim_servico VALUES (?, ?, ?, ?);", servicos)

# Inserções de Teste para Execução Financeira/Física
execucoes = [
    (1, 101, '2026-01', 150000.00, 10.0),
    (1, 102, '2026-01', 250000.00, 5.0),
    (1, 101, '2026-02', 200000.00, 25.0),
    (1, 103, '2026-02', 80000.00, 8.0),
    (1, 104, '2026-03', 120000.00, 15.0),
    (1, 106, '2026-03', 95000.00, 12.0)
]

cursor.executemany("""
INSERT INTO fato_execucao (id_obra, id_servico, ano_mes, custo_realizado, avanco_fisi_realizado_pct) 
VALUES (?, ?, ?, ?, ?);
""", execucoes)

conn.commit()
conn.close()

print("✅ Banco de dados SQLite de testes 'db_obra.db' criado e populado com sucesso!")