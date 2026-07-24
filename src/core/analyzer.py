import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# 1. CONEXÃO COM O BANCO DE DADOS
DB_PATH = "sqlite:///ehs_waste_mvp.db"

def load_data():
    """Conecta no banco SQLite e carrega a tabela MTR inteira para a memória."""
    engine = create_engine(DB_PATH)
    # Lê a tabela inteira e transforma em um DataFrame (tabela virtual do Pandas)
    df = pd.read_sql("SELECT * FROM mtrs_emitidos", engine)
    return df

def analyze_compliance_and_costs(df):
    """Aplica as regras de negócio EHS e analisa custos logísticos."""
    
    # Converte as strings de data do banco para objetos de Data do Pandas
    hoje = pd.to_datetime(datetime.now().date())
    df['data_emissao'] = pd.to_datetime(df['data_emissao'])
    
    # Calcula quantos dias o resíduo está em trânsito/emitido
    df['dias_em_transito'] = (hoje - df['data_emissao']).dt.days

    # REGRA CRÍTICA DE NEGÓCIO 1: Compliance FEPAM/IBAMA
    # Filtra MTRs que estão 'Em Transporte' há MAIS de 7 dias (Risco Alto de Multa)
    alertas_multa = df[(df['status'] == 'Em Transporte') & (df['dias_em_transito'] > 7)]

    # REGRA DE NEGÓCIO 2: Otimização Logística
    # Calcula a métrica de Custo por Tonelada para encontrar ineficiências
    df['custo_por_tonelada'] = df['custo_frete'] / df['peso_toneladas']
    custo_medio_ton = df['custo_por_tonelada'].mean()

    # Gera o Relatório no Terminal
    print("\n" + "="*50)
    print(" 🏭 RELATÓRIO DE AUDITORIA EHS E LOGÍSTICA")
    print("="*50)
    print(f"Total de MTRs processados: {len(df)}")
    print(f"Custo médio de frete da planta: R$ {custo_medio_ton:.2f} por Tonelada.")
    
    print("\n" + "!"*50)
    print(f" 🚨ALERTAS CRÍTICOS DE COMPLIANCE: {len(alertas_multa)} MTR(s) em risco!")
    print("!"*50)
    
    return alertas_multa

if __name__ == "__main__":
    print("Iniciando varredura de dados...")
    df_mtrs = load_data()
    
    # Executa a análise
    alertas = analyze_compliance_and_costs(df_mtrs)
    
    # Se houver multas potenciais, exibe os detalhes para ação imediata
    if not alertas.empty:
        print("\nDetalhamento dos MTRs com risco de autuação (Em Transporte > 7 dias):")
        # Mostra apenas as colunas mais importantes dos MTRs problemáticos
        colunas_criticas = ['numero_mtr', 'codigo_ibama', 'dias_em_transito', 'distancia_km']
        print(alertas[colunas_criticas].to_string(index=False))