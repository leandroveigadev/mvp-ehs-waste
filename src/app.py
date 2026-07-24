import streamlit as st
import pandas as pd
from database.seed_data import DB_PATH
from sqlalchemy import create_engine
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA STREAMLIT
st.set_page_config(page_title="EHS Waste Control", page_icon="♻️", layout="wide")

# 2. FUNÇÕES DE CARREGAMENTO (Com Cache para performance)
@st.cache_data
def carregar_dados_banco():
    """Carrega os dados do banco SQLite para a interface web."""
    engine = create_engine(DB_PATH)
    return pd.read_sql("SELECT * FROM mtrs_emitidos", engine)

# 3. INTERFACE DO USUÁRIO
st.title("♻️ Painel Gerencial: Rastreabilidade e Compliance Ambiental")
st.markdown("Monitoramento inteligente de MTRs (FEPAM/IBAMA) e otimização de fretes para indústrias químicas.")
st.divider()

# Carregando os dados
df = carregar_dados_banco()

# Processamento rápido para os cards de indicadores
hoje = pd.to_datetime(datetime.now().date())
df['data_emissao'] = pd.to_datetime(df['data_emissao'])
df['dias_em_transito'] = (hoje - df['data_emissao']).dt.days

custo_total = df['custo_frete'].sum()
toneladas_totais = df['peso_toneladas'].sum()
custo_medio_ton = custo_total / toneladas_totais

alertas_multa = df[(df['status'] == 'Em Transporte') & (df['dias_em_transito'] > 7)]

# 4. EXIBIÇÃO DE KPIS (Indicadores Chave)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de MTRs Registrados", value=len(df))
with col2:
    st.metric(label="Custo Médio (R$/Tonelada)", value=f"R$ {custo_medio_ton:.2f}")
with col3:
    st.metric(label="🚨 MTRs Críticos (Risco de Multa)", value=len(alertas_multa), delta="- Ação Imediata", delta_color="inverse")

st.divider()

# 5. DASHBOARDS E TABELAS
st.subheader("Auditoria Contínua: Alertas de Conformidade")

if not alertas_multa.empty:
    st.error("Atenção! Os seguintes manifestos ultrapassaram o limite de 7 dias em trânsito e configuram infração ambiental.")
    # Exibe a tabela formatada na tela com a nova sintaxe do Streamlit
    st.dataframe(
        alertas_multa[['numero_mtr', 'codigo_ibama', 'dias_em_transito', 'distancia_km', 'custo_frete']],
        width="stretch",
        hide_index=True
    )
else:
    st.success("Excelente! Nenhum manifesto em atraso. Operação em total conformidade.")

st.subheader("Visão Geral do Balanço de Massa")
# Atualizado com a nova sintaxe
st.dataframe(df, width="stretch", height=300)