import yfinance as yf
import pandas as pd
from datetime import timedelta

def fetch_futures(ticker, start_date, end_date, hour_cutoff="08:50"):
    """
    Coleta os dados de contratos futuros para o ticker fornecido.
    Filtra apenas o valor mais próximo das 8h50 de cada dia.
    """
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    print(f"Buscando dados de {ticker} entre {start_date} e {end_date}, horário de corte: {hour_cutoff}...")

    try:
        # Coletar dados horários
        data = yf.download(ticker, start=start_date, end=end_date, interval="1h", progress=False)

        # Verificar se os dados são válidos
        if data is None or data.empty:
            raise ValueError(f"Nenhum dado encontrado para o ticker {ticker} no intervalo especificado.")

        # Selecionar a coluna 'Close'
        if 'Close' not in data.columns:
            raise ValueError(f"A coluna 'Close' não está presente nos dados retornados para {ticker}.")

        # Converter o índice para datetime e filtrar os dados antes das 8h50
        data.index = pd.to_datetime(data.index)  # Converter índice para DatetimeIndex
        data = data.between_time("00:00", hour_cutoff)

        # Agrupar os dados por dia e pegar o último registro antes das 8h50
        data['Date'] = data.index.to_series().dt.date  # Extrair apenas a data do índice
        data = data.groupby('Date').tail(1)  # Pegar o último registro por dia

        # Calcular a variação percentual
        data['Variation (%)'] = data['Close'].pct_change() * 100

        # Resetar índice e renomear colunas
        data = data.reset_index()
        data = data[['Datetime', 'Close', 'Variation (%)']]
        data.columns = ['Data e Hora', 'Fechamento', 'Variação (%)']

        return data

    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados para {ticker}: {e}")
        return pd.DataFrame()  # Retorna tabela vazia em caso de erro


def fetch_adrs(ticker, start_date, end_date):
    """
    Coleta os dados das ADRs para o ticker fornecido.
    Recupera os dados das 18h30 do dia anterior.
    """
    # Ajustar datas para capturar o dia anterior
    start_date = (start_date - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (end_date - timedelta(days=1)).strftime("%Y-%m-%d")
    hour_cutoff = "18:30"

    print(f"Buscando dados de {ticker} entre {start_date} e {end_date}, horário de corte: {hour_cutoff}...")

    try:
        # Coletar dados horários
        data = yf.download(ticker, start=start_date, end=end_date, interval="1h", progress=False)

        # Verificar se os dados são válidos
        if data is None or data.empty:
            raise ValueError(f"Nenhum dado encontrado para o ticker {ticker} no intervalo especificado.")

        # Selecionar a coluna 'Close'
        if 'Close' in data.columns:
            data['Close'] = data['Close']
        else:
            raise ValueError(f"A coluna 'Close' não está presente nos dados retornados para {ticker}.")

        # Filtrar os dados até as 18h30 do dia anterior
        data = data.between_time(hour_cutoff, hour_cutoff)

        # Pegar o último registro às 18h30
        if data.empty:
            raise ValueError(f"Não foram encontrados dados para {ticker} às {hour_cutoff}.")

        # Calcular a variação percentual
        data['Variation (%)'] = data['Close'].pct_change() * 100

        # Resetar índice e renomear colunas
        data = data.reset_index()
        data = data[['Datetime', 'Close', 'Variation (%)']]
        data.columns = ['Data e Hora', 'Fechamento', 'Variação (%)']

        return data

    except Exception as e:
        print(f"Ocorreu um erro ao buscar os dados para {ticker}: {e}")
        return pd.DataFrame()  # Retorna tabela vazia em caso de erro

def calculate_probability(sp500, dowjones, adrs, commodities, forex):
    """
    Calcula a probabilidade de alta com base nos pesos das variáveis.
    """
    try:
        # Pesos atribuídos às variáveis
        weights = {
            'sp500': 0.4,
            'dowjones': 0.4,
            'adrs': 0.3,
            'commodities': 0.2,
            'forex': 0.1
        }

        # Calcular a probabilidade de alta
        probability = (
            (sp500 * weights['sp500']) +
            (dowjones * weights['dowjones']) +
            (adrs * weights['adrs']) +
            (commodities * weights['commodities']) +
            (forex * weights['forex'])
        )

        # Garantir que o resultado esteja no intervalo de 0 a 100%
        return max(0, min(100, probability))

    except Exception as e:
        print(f"Erro ao calcular a probabilidade de alta: {e}")
        return None

