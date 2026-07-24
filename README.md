# EHS Waste Control - Monitoramentos

Desenvolvido para resolver dores críticas de indústrias químicas e manufaturas: a conformidade com auditorias ambientais (FEPAM/IBAMA) e a otimização de custos logísticos no transporte de resíduos perigosos (Classe I).

# O Problema de Negócio
O controle manual de Manifestos de Transporte de Resíduos (MTRs) frequentemente resulta em infrações fiscais por perda de prazos e fretes ineficientes. Este sistema atua cruzando dados de emissão de MTRs com contratos de frete para fornecer inteligência de dados previsível.

# Funcionalidades Principais
- Core Engine Analítico: Processamento de MTRs industriais com identificação automática de gargalos (ex: MTRs em transporte há mais de 7 dias).
- Alerta de Compliance Automático: Prevenção de multas da FEPAM/IBAMA através de painéis visuais que exigem ação imediata.
- Otimização Logística: Cálculo do custo médio BÁSICO de frete por tonelada, base para redirecionamento tático para plantas de coprocessamento mais próximas.
- Dashboard Interativo: Interface Web gerencial limpa e de fácil leitura para a tomada de decisão rápida.

# Stack Tecnológica (Arquitetura)
- Backend & Data Processing: Python 3.12+, Pandas, Pydantic
- Interface do Usuário (UI): Streamlit
- Banco de Dados: SQLite (gerenciado via SQLAlchemy ORM para fácil escalabilidade)
- Segurança & DevOps: Python-dotenv, Git (Conventional Commits), .gitignore estruturado.

## Como executar o projeto localmente

1. Clone o repositório:
   bash
   git clone https://github.com/leandroveigadev/mvp-ehs-waste.git
   cd mvp-ehs-waste
   [![Contato para parcerias e estudos](https://img.shields.io/badge/Acesse_Meu_Site-0A66C2?style=for-the-badge&logo=googlechrome&logoColor=white)](https://www.leandroveiga.com.br/)