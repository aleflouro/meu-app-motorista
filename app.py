import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÕES TÉCNICAS (Sandero 1.6 8v GNV) ---
CUSTO_KM_GNV = 0.42
CUSTO_KM_MANUT = 0.23
CUSTO_OPERACIONAL_TOTAL = CUSTO_KM_GNV + CUSTO_KM_MANUT
PARCELA_CARRO = 1100.00
SEGURO_MENSAL = 265.00
CUSTO_FIXO_MENSAL = PARCELA_CARRO + SEGURO_MENSAL
META_LUCRO_DESEJADO = 5000.00

st.set_page_config(page_title="Gestão de Motorista Pro", page_icon="🚕", layout="wide")

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: LANÇAMENTO DIÁRIO ---
st.sidebar.header("📝 Lançar Ganhos do Dia")
data_atual = st.sidebar.date_input("Data", datetime.now())
faturamento_bruto = st.sidebar.number_input("Faturamento Bruto (R$)", min_value=0.0, step=10.0)
km_rodado = st.sidebar.number_input("KM Total Rodado (Painel)", min_value=0.1, step=1.0)
horas_online = st.sidebar.number_input("Horas Online", min_value=0.1, step=0.5)

# --- CÁLCULOS PRINCIPAIS ---
gasto_combustivel_manut = km_rodado * CUSTO_OPERACIONAL_TOTAL
diaria_fixos = CUSTO_FIXO_MENSAL / 22 # Base 22 dias trab/mês
lucro_liquido_dia = faturamento_bruto - gasto_combustivel_manut - diaria_fixos
ganho_por_km = faturamento_bruto / km_rodado
ganho_por_hora = faturamento_bruto / horas_online

# --- DASHBOARD PRINCIPAL ---
st.title("🚕 Painel de Controle: Sandero 1.6 GNV")
st.subheader(f"Resumo do Dia: {data_atual.strftime('%d/%m/%Y')}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Lucro Líquido Real", f"R$ {lucro_liquido_dia:.2f}")
with col2:
    st.metric("R$ por KM", f"R$ {ganho_por_km:.2f}", delta="Ideal: > R$ 1.60")
with col3:
    st.metric("Custo de Rodagem", f"R$ {gasto_combustivel_manut:.2f}", delta_color="inverse")
with col4:
    st.metric("R$ por Hora", f"R$ {ganho_por_hora:.2f}")

st.divider()

# --- ABA DE METAS E DOCUMENTAÇÃO ---
tab1, tab2, tab3 = st.tabs(["🎯 Meta R$ 5k", "📋 Tabela de Decisão", "📅 Documentos 2026"])

with tab1:
    st.subheader("Progresso para o Lucro de R$ 5.000,00")
    meta_bruta_mes = 9965.00  # Calculado anteriormente
    progresso = min((faturamento_bruto * 22) / meta_bruta_mes, 1.0) # Simulação mensal baseada no dia
    st.progress(progresso)
    st.write(f"Se todos os dias forem como hoje, você atingirá **{progresso*100:.1f}%** da sua meta mensal.")
    
    st.info("""**Dica para o Sandero 1.6:** Para sobrar R$ 5k limpo, você precisa faturar em média 
            **R$ 453,00 por dia** e não rodar mais que **280km**.""")

with tab2:
    st.subheader("Vale a pena aceitar?")
    decisao_data = {
        "Valor por KM": ["Abaixo de R$ 1,20", "R$ 1,30 a R$ 1,50", "Acima de R$ 1,60", "Acima de R$ 2,00"],
        "Resultado": ["🔴 PREJUÍZO (Não aceite)", "🟡 ACEITÁVEL (Só sem trânsito)", "🟢 BOM (Padrão de lucro)", "💎 EXCELENTE (Prioridade)"]
    }
    st.table(pd.DataFrame(decisao_data))

with tab3:
    st.subheader("Calendário Detran/GNV 2026")
    docs = {
        "Item": ["Vistoria GNV (CSV)", "Licenciamento (GRT)", "IPVA 2026", "Correia Dentada (Preventiva)"],
        "Prazo": ["Março/2026", "Abril/2026", "Janeiro/2026", "A cada 40k KM"],
        "Valor Est.": ["R$ 350,00", "R$ 190,00", "R$ 480,00", "R$ 750,00"]
    }
    st.dataframe(pd.DataFrame(docs), use_container_width=True)
    
    # Calculadora de Reserva
    st.warning("⚠️ **Reserva de Emergência:** Guarde **R$ 12,00 por dia** trabalhado para cobrir esses custos sem sustos.")

# --- RODAPÉ INFORMATIVO ---
st.sidebar.divider()
st.sidebar.markdown(f"""
**Configuração Ativa:**
- Consumo GNV: 12km/m³
- Preço GNV: R$ 4,99
- Manutenção: R$ 0,23/km
- Financiamento: R$ 1.100,00
""")
