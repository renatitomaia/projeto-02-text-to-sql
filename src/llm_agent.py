import os
import re
import time
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def get_genai_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env!")
    return genai.Client(api_key=api_key)

def generate_sql(question: str, db_schema: str) -> str:
    """Gera uma consulta SQL a partir da pergunta em linguagem natural."""
    client = get_genai_client()

    prompt = f"""
Você é um especialista em SQL e Análise de Dados na Construção Civil.
Dada a estrutura do banco de dados SQLite abaixo, sua tarefa é converter a pergunta do usuário em uma única consulta SQL válida.

--- ESTRUTURA DO BANCO DE DADOS ---
{db_schema}

--- REGRAS OBRIGATÓRIAS ---
1. Responda APENAS com a instrução SQL. Não inclua explicações, comentários ou markdown adicional.
2. Não utilize caracteres de bloco de código como ```sql ou ``` no início/fim.
3. Garanta que os JOINs utilizem as chaves corretas (id_obra, id_servico).
4. Para agrupamentos por categoria ou nome, faça os JOINs necessários com dim_servico ou dim_obra.

--- PERGUNTA DO USUÁRIO ---
{question}
"""

    candidate_models = ["gemini-3.6-flash", "gemini-2.5-flash"]
    response = None
    last_exception = None

    for model_name in candidate_models:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0.0)
                )
                if response and response.text:
                    break
            except Exception as e:
                last_exception = e
                time.sleep(1)
                continue
        if response and response.text:
            break

    if not response or not response.text:
        raise RuntimeError(f"Serviço indisponível: {last_exception}")

    sql_query = response.text.strip()
    sql_query = re.sub(r"^```sql\s*", "", sql_query, flags=re.IGNORECASE)
    sql_query = re.sub(r"^```\s*", "", sql_query)
    sql_query = re.sub(r"```$", "", sql_query)
    
    return sql_query.strip()


def explain_results(question: str, df: pd.DataFrame) -> str:
    """Gera uma explicação em linguagem natural dos dados retornados da consulta."""
    if df is None or df.empty:
        return "Nenhum dado foi retornado para esta consulta."

    client = get_genai_client()

    # Limita o envio aos primeiros 10 registros para evitar consumo excessivo de tokens
    data_preview = df.head(10).to_markdown(index=False)

    prompt = f"""
Você é um Engenheiro de Planejamento e Analista de Dados Sênior.
Sua tarefa é explicar brevemente os resultados obtidos de uma consulta para a diretoria.

--- PERGUNTA DO GESTOR ---
{question}

--- DADOS OBTIDOS (Amostra) ---
{data_preview}

--- REGRAS ---
1. Escreva uma resposta direta, clara e profissional em português (2 a 4 frases).
2. Destaque os números, valores orçamentários ou totais mais relevantes.
3. Não cite código SQL ou detalhes técnicos de tabelas na sua resposta.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        return response.text.strip() if response and response.text else ""
    except Exception:
        return "Não foi possível gerar a síntese dos dados no momento."