from fastapi import FastAPI
import yfinance as yf
from datetime import datetime

app = FastAPI()

# Taxa esperada
taxa_esperada = 0.06

@app.get("/preco_teto/{ticker}")
def calcular_preco_teto(ticker: str):
    try:
        ticker_obj = yf.Ticker(f"{ticker}.SA")
        dividendos = ticker_obj.dividends
        cotacao_atual = ticker_obj.history(period="1d")['Close'].iloc[0]

        dividendos_por_ano = dividendos.resample('Y').sum()

        ano_atual = datetime.now().year
        dividendos_filtrados = dividendos_por_ano[dividendos_por_ano.index.year < ano_atual]

        ultimos_5_anos = dividendos_filtrados.tail(5)

        media_dividendos = ultimos_5_anos.mean()

        preco_teto = media_dividendos / taxa_esperada

        resultado = {
            "cotacao_atual": round(cotacao_atual, 2),
            "dividendos_ultimos_5_anos": {ano.year: round(valor, 2) for ano, valor in ultimos_5_anos.items()},
            "dy_medio": round(media_dividendos, 2),
            "preco_teto": round(preco_teto, 2)
        }

        return resultado

    except Exception as e:
        return {"error": str(e)}
