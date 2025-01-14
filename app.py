import streamlit as st
from data_fetcher import fetch_futures

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

    # Coletar dados do S&P 500
    sp500_data = fetch_futures("ES=F", start_date, end_date)
    dowjones_data = fetch_futures("YM=F", start_date, end_date)

    # Exibir os dados coletados na interface
    st.subheader("Futuros do S&P 500")
    st.write(sp500_data)

    st.subheader("Futuros do Dow Jones")
    st.write(dowjones_data)
