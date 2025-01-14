import yfinance as yf

def fetch_futures(ticker, start_date, end_date, hour_cutoff="08:00"):
    """
    Coleta os dados dos futuros do S&P 500 entre as datas fornecidas.
    Filtra apenas os dados até o horário de corte (ex.: 08:00 da manhã).
    """
    sp500_futures_ticker = ticker

    # Garantir formato ISO para datas
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    print(f"Buscando dados de {sp500_futures_ticker} entre {start_date} e {end_date}...")

    try:
        # Coletar dados horários
        data = yf.download(ticker, start=start_date, end=end_date, interval="1h", progress=False)

        # Verificar se os dados são válidos
        if data is None or data.empty:
            raise ValueError(f"Erro: Nenhum dado foi retornado para o ticker {sp500_futures_ticker}.")

        # Selecionar a coluna 'Close'
        if 'Close' in data.columns:
            data['Close'] = data['Close']
        else:
            raise ValueError(f"A coluna 'Close' não está presente nos dados retornados.")

        # Filtrar os dados até o horário de corte
        data = data.between_time("00:00", hour_cutoff)

        # Calcular a variação percentual
        data['Variation (%)'] = data['Close'].pct_change() * 100

        # Resetar índice e renomear colunas
        data = data.reset_index()
        data = data[['Datetime', 'Close', 'Variation (%)']]
        data.columns = ['Data e Hora', 'Fechamento', 'Variação (%)']

        return data

    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados: {e}")
        raise


