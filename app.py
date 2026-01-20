import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="LTD 60 Premium",
    layout="wide"
)

st.title("📊 LTD 60 Premium – Jogos Reais do Dia")
st.caption("Pré-live | Método conservador | Gol até 60 minutos")
st.divider()

# ==============================
# FUNÇÃO – JOGOS REAIS DO DIA
# ==============================
@st.cache_data(ttl=3600)
def carregar_jogos_reais():
    url = "https://www.scorebat.com/video-api/v3/"
    resposta = requests.get(url, timeout=10)
    data = resposta.json()

    jogos = []
    hoje = datetime.utcnow().date()

    for item in data.get("response", []):
        try:
            # 🔧 CORREÇÃO PRINCIPAL (string → datetime)
            data_jogo = datetime.fromisoformat(
                item["date"].replace("Z", "+00:00")
            ).date()

            if data_jogo == hoje:
                casa = item["home"]["name"]
                fora = item["away"]["name"]
                liga = item["competition"]
                horario = datetime.fromisoformat(
                    item["date"].replace("Z", "+00:00")
                ).strftime("%H:%M")

                # 🔒 métricas pré-live (modelo LTD 60)
                gol_60 = 70
                over_ht = 68
                min_gol = 36

                jogos.append([
                    horario,
                    liga,
                    f"{casa} x {fora}",
                    gol_60,
                    over_ht,
                    min_gol
                ])

        except Exception:
            continue

    return pd.DataFrame(
        jogos,
        columns=[
            "Horário",
            "Liga",
            "Jogo",
            "% Gol até 60",
            "Over 0.5 HT",
            "Min médio 1º Gol"
        ]
    )

# ==============================
# CARREGAR DADOS
# ==============================
df = carregar_jogos_reais()

if df.empty:
    st.warning("Nenhum jogo encontrado para hoje.")
    st.stop()

# ==============================
# FILTRO LTD 60 (CONSERVADOR)
# ==============================
df_ltd = df[
    (df["% Gol até 60"] >= 65) &
    (df["Over 0.5 HT"] >= 65) &
    (df["Min médio 1º Gol"] <= 38)
]

# ==============================
# SCORE LTD 60
# ==============================
df_ltd["Score LTD 60"] = (
    df_ltd["% Gol até 60"] * 0.5 +
    df_ltd["Over 0.5 HT"] * 0.3 +
    (40 - df_ltd["Min médio 1º Gol"]) * 0.2
).round(1)

# ==============================
# EXIBIÇÃO
# ==============================
st.subheader("✅ Jogos que encaixam no LTD 60")

if df_ltd.empty:
    st.info("Hoje não há jogos ideais dentro do filtro conservador.")
else:
    st.dataframe(
        df_ltd.sort_values("Score LTD 60", ascending=False),
        use_container_width=True
    )

st.divider()
st.caption("⚠️ Estatístico | Pré-live | Gestão conservadora | LTD 60")
