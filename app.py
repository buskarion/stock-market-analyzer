import streamlit as st
from data_fetcher import fetch_futures, fetch_adrs

# Título e descrição da aplicação
st.title("Análise de Variáveis da Madrugada - Mini Índice")
st.write(
    """
    Ferramenta para analisar as variáveis que influenciam o comportamento do Mini-Índice na abertura do mercado.
    """
)

# Seção para seleção de data ou intervalo de datas
st.sidebar.header("Configurações de análise")
start_date = st.sidebar.date_input("Data inicial")
end_date = st.sidebar.date_input("Data final")

# Botão para executar análise
if st.sidebar.button("Executar Análise"):
    st.write(f"Analisando dados de {start_date} até {end_date}...")

    # Coleta de dados
    sp500_data = fetch_futures("ES=F", start_date, end_date)
    dowjones_data = fetch_futures("YM=F", start_date, end_date)
    pbr_data = fetch_adrs("PBR", start_date, end_date)
    vale_data = fetch_adrs("VALE", start_date, end_date)

    # Exibição dos dados
    st.subheader("Futuros do S&P 500")
    st.write(sp500_data)

    st.subheader("Futuros do Dow Jones")
    st.write(dowjones_data)

    st.subheader("ADRs - Petrobras (PBR)")
    st.write(pbr_data)

    st.subheader("ADRs - Vale (VALE)")
    st.write(vale_data)
