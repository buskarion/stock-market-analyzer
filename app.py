import streamlit as st
import pandas as pd
from data_fetcher import fetch_futures, fetch_adrs, calculate_probability

# Título e descrição da aplicação
st.title("Análise de Variáveis da Madrugada - Mini Índice")
st.write("Ferramenta para analisar as variáveis que influenciam o comportamento do Mini-Índice na abertura do mercado.")

# Seção para seleção de data ou intervalo de datas
st.sidebar.header("Configurações de análise")
start_date = st.sidebar.date_input("Data inicial")
end_date = st.sidebar.date_input("Data final")

# Criar lista para armazenar os resultados
results = []

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

    # ✅ Garantir que 'Data e Hora' seja convertida corretamente antes de acessar `.dt`
    for df in [sp500_data, dowjones_data, pbr_data, vale_data, brent_data, usd_brl_data]:
        if 'Data e Hora' in df.columns:
            # 🔹 Garantir que 'Data e Hora' seja Pandas Series, convertendo explicitamente
            df['Data e Hora'] = pd.Series(df['Data e Hora']).astype(str)

            # 🔹 Converter para datetime, garantindo que seja datetime64[ns, UTC]
            df['Data e Hora'] = pd.to_datetime(df['Data e Hora'], errors='coerce', utc=True)

            # 🔹 Criar a coluna 'Data' se ainda não existir
            df['Data'] = df['Data e Hora']


    # Calcular a probabilidade de alta
    for index, row in sp500_data.iterrows():
        try:
            probability = calculate_probability(
                sp500=row['Variação (%)'],
                dowjones=dowjones_data.loc[index, 'Variação (%)'] if index in dowjones_data.index else 0,
                adrs=((pbr_data.loc[index, 'Variação (%)'] if index in pbr_data.index else 0) + 
                      (vale_data.loc[index, 'Variação (%)'] if index in vale_data.index else 0)) / 2,
                commodities=brent_data.loc[index, 'Variação (%)'] if index in brent_data.index else 0,
                forex=usd_brl_data.loc[index, 'Variação (%)'] if index in usd_brl_data.index else 0
            )

            if probability is None:
                probability = 0  # Define um valor padrão

            # Adicionar resultado formatado corretamente
            results.append({
                'Data': row['Data'],  # ✅ Agora corrigido
                'Probabilidade de Alta (%)': round(probability, 2),
                'Decisão': "Comprar" if probability >= 70 else "Vender" if probability <= 30 else "Não Entrar"
            })

        except Exception as e:
            st.write(f"Erro ao processar dados para {index}: {e}")

    # Exibir tabela consolidada
    results_df = pd.DataFrame(results)
    st.subheader("Análise de Probabilidade de Alta")
    st.write(results_df)

