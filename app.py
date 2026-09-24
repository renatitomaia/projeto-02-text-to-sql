import sys
import os
import io

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_db_schema, execute_query
from llm_agent import generate_sql, explain_results

# Configuração da página
st.set_page_config(
    page_title="Analytics Obra | Assistente SQL", 
    page_icon="🏗️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Avançada
st.markdown("""
<style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Estilização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Cartões KPI de Topo */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-title {
        font-size: 13px;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 20px;
        color: #0f172a;
        font-weight: 700;
    }

    /* Caixa de Resumo do Executivo */
    .ai-box {
        background-color: #ffffff;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        margin-bottom: 24px;
    }
    .ai-box-title {
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 8px;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .ai-box-content {
        color: #334155;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Botões de Atalho */
    .stButton > button {
        width: 100%;
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        font-weight: 500;
        padding: 8px 12px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
        background-color: #eff6ff;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/construction.png", width=64)
    st.title("Enterprise Analytics")
    st.caption("Painel de Controlo & Assistente de Dados")
    st.markdown("---")
    
    st.subheader("🗄️ Estrutura da Base de Dados")
    schema = get_db_schema()
    st.code(schema, language="sql")
    
    st.markdown("---")
    st.caption("Versão do Agente: **Gemini 3.6 Flash**")

# --- CABEÇALHO PRINCIPAL ---
st.title("🏗️ Plataforma de Inteligência de Obras")
st.markdown("Consulte indicadores operacionais e financeiros em linguagem natural com geração autónoma de SQL.")

# Cartões de Estado do Sistema (KPIs de topo)
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
with col_kpi1:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Motor de IA</div>
            <div class="kpi-value" style="color: #16a34a;">● Ativo</div>
        </div>
    """, unsafe_allow_html=True)
with col_kpi2:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Base de Dados</div>
            <div class="kpi-value">SQLite Local</div>
        </div>
    """, unsafe_allow_html=True)
with col_kpi3:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Modo de Operação</div>
            <div class="kpi-value">Text-to-SQL</div>
        </div>
    """, unsafe_allow_html=True)
with col_kpi4:
    st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Acesso</div>
            <div class="kpi-value">Gestão de Engenharia</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA DE CONSULTA ---
st.subheader("💬 Faça uma Pergunta de Negócio")

# Atalhos Rápidos
col_a, col_b, col_c = st.columns(3)
example_q = None

if col_a.button("📊 Custo Total por Categoria"):
    example_q = "Qual o custo total realizado por categoria de serviço?"
if col_b.button("🔝 Top 5 Serviços Mais Caros"):
    example_q = "Quais são os 5 serviços com maior orçamento cadastrado?"
if col_c.button("📅 Custos do Mês 2026-01"):
    example_q = "Mostre todos os custos realizados no mês de 2026-01 com o nome dos serviços."

# Campo de pesquisa estilo pesquisa executiva
question = st.text_input("", value=example_q if example_q else "", placeholder="Exemplo: Qual o orçamento total previsto para a estrutura da obra?")

if question:
    with st.spinner("A analisar a base de dados e a compilar a resposta..."):
        try:
            # 1. Geração SQL
            sql_query = generate_sql(question, schema)
            
            # 2. Execução
            df, error = execute_query(sql_query)
            
            if error:
                st.error(f"⚠️ Não foi possível executar a consulta: {error}")
            else:
                # 3. Explicação IA
                explanation = explain_results(question, df)
                
                st.markdown(f"""
                <div class="ai-box">
                    <div class="ai-box-title">💡 Diagnóstico e Síntese Executiva</div>
                    <div class="ai-box-content">{explanation}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Divisão do Resultado em Separadores (Tabs)
                tab_dash, tab_data, tab_sql = st.tabs(["📈 Dashboard Executivo", "📋 Tabela de Dados", "💻 Consulta SQL Gerada"])
                
                with tab_dash:
                    if df is not None and df.shape[1] >= 2 and df[df.columns[1]].dtype in ['int64', 'float64']:
                        col_x = df.columns[0]
                        col_y = df.columns[1]
                        
                        fig = px.bar(
                            df, 
                            x=col_x, 
                            y=col_y, 
                            title=f"Análise de {col_y} por {col_x}", 
                            text_auto='.2f',
                            color_discrete_sequence=['#2563eb']
                        )
                        fig.update_layout(
                            paper_bgcolor='#ffffff',
                            plot_bgcolor='#f8fafc',
                            font=dict(color="#0f172a", size=13),
                            margin=dict(l=20, r=20, t=50, b=20)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Esta consulta não gerou uma visualização gráfica automática. Utilize a aba 'Tabela de Dados'.")
                
                with tab_data:
                    st.dataframe(df, use_container_width=True)
                    
                    # Botões de Exportação
                    c_exp1, c_exp2, _ = st.columns([1, 1, 2])
                    
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    c_exp1.download_button("📄 Exportar CSV", data=csv_data, file_name="relatorio_obra.csv", mime="text/csv")
                    
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Análise')
                    excel_data = buffer.getvalue()
                    
                    c_exp2.download_button(
                        "📊 Exportar Excel (.xlsx)", 
                        data=excel_data, 
                        file_name="relatorio_obra.xlsx", 
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                with tab_sql:
                    st.markdown("A instrução SQL abaixo foi traduzida automaticamente pelo agente:")
                    st.code(sql_query, language="sql")

        except Exception as e:
            st.error(f"Erro no processamento da requisição: {e}")