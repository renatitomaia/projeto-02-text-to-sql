# Projeto 02 | Assistente Inteligente Text-to-SQL para Gestão de Obras

> Aplicação web em Python (Streamlit) integrada a modelos de Linguagem (LLM) para tradução de perguntas em linguagem natural em consultas SQL e dashboards interativos.

## 📌 Visão Geral

Este projeto apresenta uma solução de **Text-to-SQL / IA Generativa aplicada à Análise de Dados**, focada no acompanhamento físico e financeiro de obras na construção civil. 

A ferramenta permite que gestores e engenheiros façam perguntas em português (ex: *"Qual o custo total realizado por categoria?"*) e recebam instantaneamente:
1. O comando **SQL gerado** e otimizado pela IA.
2. Os dados filtrados direto do banco de dados em formato tabular.
3. Visualizações gráficas automáticas e opção de exportação dos dados.

## 🎯 Problema de Negócio

Profissionais de gestão muitas vezes dependem de analistas de dados para extrair informações específicas do banco de dados SQL. Este assistente democratiza o acesso aos dados da obra, permitindo consultas ad-hoc rápidas sem a necessidade de conhecimento prévio em sintaxe SQL.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Web:** Streamlit
- **Banco de Dados Relacional:** SQLite3 e SQLAlchemy
- **IA Generativa / LLM:** Google GenAI SDK (Gemini API)
- **Manipulação e Análise de Dados:** Pandas
- **Visualização de Dados:** Plotly Express
- **Gestão de Variáveis:** Python-Dotenv

## 🔄 Fluxo da Solução

```text
  [ Pergunta do Usuário ]
            │
            ▼
┌───────────────────────┐      ┌─────────────────────────┐
│  Interface Streamlit  │ ───► │   Módulo Agente (LLM)   │ ◄── Schema do Banco
└───────────────────────┘      └────────────┬────────────┘
                                            │
                                            ▼ (Query SQL Gerada)
┌───────────────────────┐      ┌─────────────────────────┐
│ Tabela & Gráficos     │ ◄─── │ Engine Executora SQLite │
│ (Plotly / Pandas)     │      └─────────────────────────┘
└───────────────────────┘
```

## 🧱 Estrutura do Banco de Dados

O projeto utiliza um modelo dimensional em estrela (Star Schema) voltado ao contexto de engenharia civil:

dim_obra: Informações cadastrais e orçamentárias da obra.

dim_servico: Serviços, categorias e orçamentos unitários.

fato_planejamento: Cronograma e avanço físico/financeiro previsto.

fato_execucao: Apontamentos de custos realizados e avanço físico real.

## 📁 Estrutura do Repositório
```
projeto-02-text-to-sql/
├── database/
│   ├── db_obra.db        # Banco de dados SQLite local
│   └── seed_database.py  # Script de criação e povoamento das tabelas
├── src/
│   ├── __init__.py
│   ├── database.py       # Funções de leitura do schema e execução de queries
│   └── llm_agent.py      # Agente LLM para tradução de linguagem natural em SQL
├── .env.example          # Modelo para configuração das variáveis de ambiente
├── .gitignore            # Arquivo para ignorar dependências e arquivos sensíveis
├── app.py                # Aplicação principal em Streamlit
├── requirements.txt      # Dependências do projeto Python
└── README.md             # Documentação do repositório
```

## 🚀 Como Executar o Projeto
Pré-requisitos
Python 3.10 ou superior instalado.

Chave de API do Google Gemini (obtida gratuitamente no Google AI Studio).

Passo a Passo

1. Clonar o repositório:
```bash
git clone [https://github.com/renatitomaia/projeto-02-text-to-sql.git](https://github.com/renatitomaia/projeto-02-text-to-sql.git)
cd projeto-02-text-to-sql
```

2. Criar e ativar o ambiente virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
```
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instalar as dependências:
```bash
pip install -r requirements.txt
```

4. Configurar as Variáveis de Ambiente:
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave de API:
```bash
GEMINI_API_KEY=sua_chave_api_aqui
```

6. Gerar e popular o Banco de Dados local:
```bash
python database/seed_database.py
```

6. Iniciar a aplicação Streamlit:
```bash
streamlit run app.py
```

O navegador abrirá automaticamente no endereço http://localhost:8501.

## 📸 Funcionalidades da Aplicação
Consultas em Linguagem Natural: Tradução imediata de dúvidas para SQL.

Botões de Atalho (Perguntas Rápidas): Exemplos pré-configurados de consultas de negócios.

Visualização de Schema: Painel lateral contendo a estrutura completa do banco de dados em tempo real.

Gráficos Dinâmicos: Geração automática de gráficos de barras para colunas numéricas agregadas.

Exportação de Dados: Download dos resultados filtrados em formato .csv.

## 👤 Autor
Renato Maia

Portfólio em Análise de Dados, Engenharia e Inteligência Artificial.

LinkedIn: [text](https://www.linkedin.com/in/renato-maia-4b6733b2/)

GitHub: [text](https://github.com/renatitomaia)

