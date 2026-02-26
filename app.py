import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

# --- CONFIGURAÇÕES DO VEÍCULO (Sandero 1.6 8v) ---
PRECO_GNV = 5.40
CONS_MEDIO = 12.0
CUSTO_KM_MANUT = 0.25 # Reserva p/ pneus, óleo, correia
PARCELA_CARRO = 1100.00
SEGURO_MENSAL = 265.00
CUSTO_FIXO_DIA = (PARCELA_CARRO + SEGURO_MENSAL) / 22

st.set_page_config(page_title="Sandero 1.6 Pro", layout="wide", page_icon="🚗")

# --- INICIALIZAÇÃO DE DADOS (Persistência na Sessão) ---
if 'db_ganhos' not in st.session_state:
    st.session_state.db_ganhos = pd.DataFrame(columns=['Data', 'Dia', 'Faturamento', 'KM', 'Lucro_Real'])
if 'km_odometro' not in st.session_state:
    st.session_state.km_odometro = 100000.0 # Ajuste para o KM real do seu carro aqui

# --- SIDEBAR: LANÇAMENTO DIÁRIO ---
st.sidebar.header("📥 Lançar Dia de Trabalho")
with st.sidebar.form("form_dia"):
    data_t = st.date_input("Data", datetime.now())
    fat_t = st.number_input("Ganho Total no App (R$)", min_value=0.0)
    km_t = st.number_input("KM Total Rodado Hoje", min_value=1.0)
    
    if st.form_submit_button("💾 Salvar no Histórico"):
        custo_gnv = (km_t / CONS_MEDIO) * PRECO_GNV
        custo_total = (km_t * CUSTO_KM_MANUT) + custo_gnv + CUSTO_FIXO_DIA
        lucro_calc = fat_t - custo_total
        
        novo_registro = pd.DataFrame([[data_t, data_t.strftime('%A'), fat_t, km_t, lucro_calc]], 
                                    columns=['Data', 'Dia', 'Faturamento', 'KM', 'Lucro_Real'])
        st.session_state.db_ganhos = pd.concat([st.session_state.db_ganhos, novo_registro], ignore_index=True)
        st.session_state.km_odometro += km_t
        st.sidebar.success("Dados salvos!")

# --- CORPO DO APP ---
st.title("🚀 Gestor de Ganhos - Sandero 1.6")

# --- SEÇÃO 1: ALERTAS DE MANUTENÇÃO ---
st.subheader("🚨 Alertas de Manutenção (Odômetro: {:.0f} km)".format(st.session_state.km_odometro))
c1, c2, c3 = st.columns(3)

# Lógica de Alerta Simples (Troca a cada 10k óleo, 50k correia, 30k velas)
with c1:
    st.metric("Troca de Óleo", "A cada 10.000km")
    st.progress(0.7) # Exemplo de barra de vida do óleo
with c2:
    st.metric("Correia Dentada", "A cada 50.000km")
    st.info("Foco: Motor K7M 1.6")
with c3:
    st.metric("Sistema GNV/Velas", "A cada 30.000km")
    st.success("GNV a R$ 5,40")

st.divider()

# --- SEÇÃO 2: GRÁFICOS E TABELAS ---
tab1, tab2, tab3 = st.tabs(["📊 Desempenho", "📅 Histórico Completo", "📥 Exportar Excel"])

with tab1:
    if not st.session_state.db_ganhos.empty:
        fig = px.bar(st.session_state.db_ganhos, x='Dia', y='Lucro_Real', color='Lucro_Real', 
                     title="Lucro Real por Dia da Semana", color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Preencha os dados na lateral para ver seu gráfico de lucro.")

with tab2:
    st.dataframe(st.session_state.db_ganhos, use_container_width=True)

with tab3:
    st.subheader("Baixar Relatório para Comprovação de Renda")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        st.session_state.db_ganhos.to_excel(writer, index=False, sheet_name='Ganhos')
    
    st.download_button(
        label="📥 Baixar Planilha Excel",
        data=output.getvalue(),
        file_name="relatorio_motorista_2026.xlsx",
        mime="application/vnd.ms-excel"
    )
