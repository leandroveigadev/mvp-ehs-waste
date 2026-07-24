import os
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. CONFIGURAÇÃO DO BANCO DE DADOS
DB_PATH = "sqlite:///ehs_waste_mvp.db"
engine = create_engine(DB_PATH, echo=False)
Base = declarative_base()

# 2. DEFINIÇÃO DA TABELA (ORM)
class MTR(Base):
    __tablename__ = 'mtrs_emitidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_mtr = Column(String(50), unique=True, nullable=False)
    codigo_ibama = Column(String(20), nullable=False)
    descricao = Column(String(100), nullable=False)
    peso_toneladas = Column(Float, nullable=False)
    status = Column(String(30), nullable=False)
    data_emissao = Column(Date, nullable=False)
    distancia_km = Column(Float, nullable=False)
    custo_frete = Column(Float, nullable=False)
    tipo_destinacao = Column(String(50), nullable=False)

Base.metadata.create_all(engine)

# 3. GERAÇÃO DE DADOS SIMULADOS (SEEDING)
def generate_seed_data(num_records=500):
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(MTR).delete() # clear data

    residuos_padrao = [
        {"codigo": "08 01 11", "desc": "Resíduos de tintas/vernizes contendo solventes"},
        {"codigo": "08 01 13", "desc": "Borras de tintas contendo solventes orgânicos"}
    ]
    
    status_opcoes = ["Emitido", "Em Transporte", "Entregue", "Cancelado"]
    destinacoes = ["Coprocessamento", "Aterro Classe I", "Recuperação de Solventes"]

    data_atual = datetime.now()

    print(f"Gerando {num_records} registros de MTRs Industriais...")

    for i in range(num_records):
        residuo = random.choice(residuos_padrao)
        status = random.choice(status_opcoes)
        
        if status == "Em Transporte" and random.random() < 0.2:
            dias_atras = random.randint(8, 15)
        else:
            dias_atras = random.randint(0, 30)
            
        data_emissao = data_atual - timedelta(days=dias_atras)
        peso = round(random.uniform(0.5, 12.0), 2) # Peso em toneladas
        distancia = round(random.uniform(15.0, 350.0), 1) # Distância em km
        custo = round(150.0 + (distancia * 8.50), 2)

        novo_mtr = MTR(
            numero_mtr=f"RS-{data_emissao.strftime('%Y%m')}-{1000 + i}",
            codigo_ibama=residuo["codigo"],
            descricao=residuo["desc"],
            peso_toneladas=peso,
            status=status,
            data_emissao=data_emissao.date(),
            distancia_km=distancia,
            custo_frete=custo,
            tipo_destinacao=random.choice(destinacoes)
        )
        session.add(novo_mtr)

    # 4. SALVANDO NO BANCO DE DADOS
    session.commit()
    session.close()
    print("Seed finalizado com sucesso! Banco de dados populado.")

if __name__ == "__main__":
    generate_seed_data()