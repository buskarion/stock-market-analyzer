import streamlit as st

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

