import streamlit as st
import pandas as pd
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
    brent_data = fetch_futures("BZ=F", start_date, end_date)
    usd_brl_data = fetch_futures("USDBRL=X", start_date, end_date)

    # Consolidar em uma única tabela
    consolidated_data = pd.concat(
        [
            sp500_data.assign(Variável="S&P 500"),
            dowjones_data.assign(Variável="Dow Jones"),
            pbr_data.assign(Variável="Petrobras (PBR)"),
            vale_data.assign(Variável="Vale (VALE)"),
            brent_data.assign(Variável="Petróleo Brent"),
            usd_brl_data.assign(Variável="USD/BRL"),
        ]
    )

    # Exibir a tabela consolidada
    st.subheader("Análise Consolidada")
    st.write(consolidated_data)
