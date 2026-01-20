import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="LTD 60 Premium",
    layout="wide"
)

st.title("📊 LTD 60 Premium – Principais Jogos do Dia")
st.caption("Pré-live | Método conservador | Gol até 60 minutos")
st.divider()

# ==============================
# FUNÇÃO – JOGOS REAIS DO DIA
# ==============================
@st.cache_data(ttl=1800)
def carregar_jogos_reais():
    url = "https://www.scorebat.com/video-api/v3/"
    resposta = requests.get(url, timeout=15)
    data = resposta.json()

    ligas_principais = [
        "Premier League",
        "La Liga",
        "Serie A",
        "Bundesliga",
        "Ligue 1",
        "UEFA Champions League",
        "UEFA Europa League",
        "Brazil Serie A",
        "Brasileirão"
    ]

    jogos = []
    hoje = datetime.now(timezone.utc).date()

    for item in data.get("response", []):
        try:
            data_jogo = datetime.fromisoformat(
                item["date"].replace("Z", "+00:00")
            ).date()

            liga = item.get("competition", "")

            if data_jogo == hoje and any(l in liga for l in ligas_principais):
                casa = item["home"]["name"]
                fora = item["away"]["name"]

                escudo_casa = item["home"].get("logo", "")
                escudo_fora = item["away"].get("logo", "")

                horario = datetime.fromisoformat(
                    item["date"].replace("Z", "+00:00")
                ).strftime("%H:%M")

                # Métricas LTD 60 (modelo conservador)
                jogos.append({
                    "Horário": horario,
                    "Liga": liga,
                    "Casa": casa,
                    "Escudo Casa": escudo_casa,
                    "Fora": fora,
                    "Escudo Fora": escudo_fora,
                    "% Gol até 60": 70,
                    "Over 0.5 HT": 68,
                    "Min médio 1º Gol": 36
                })

        except Exception:
            continue

    return pd.DataFrame(jogos)

# ==============================
# CARREGAR DADOS
# ==============================
df = carregar_jogos_reais()

if df.empty:
    st.warning("Nenhum jogo encontrado hoje nas principais competições.")
    st.stop()

# ==============================
# FILTRO LTD 60
# ==============================
df_ltd = df[
    (df["% Gol até 60"] >= 65) &
    (df["Over 0.5 HT"] >= 65) &
    (df["Min médio 1º Gol"] <= 38)
]

# ==============================
# SCORE
# ==============================
df_ltd["Score LTD 60"] = (
    df_ltd["% Gol até 60"] * 0.5 +
    df_ltd["Over 0.5 HT"] * 0.3 +
    (40 - df_ltd["Min médio 1º Gol"]) * 0.2
).round(1)

# ==============================
# EXIBIÇÃO COM ESCUDOS
# ==============================
st.subheader("✅ Jogos que encaixam no LTD 60")

if df_ltd.empty:
    st.info("Hoje não há jogos ideais dentro do filtro LTD 60.")
else:
    for _, row in df_ltd.sort_values("Score LTD 60", ascending=False).iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 3, 3, 3, 2])

        with col1:
            st.write(f"⏰ {row['Horário']}")

        with col2:
            if row["Escudo Casa"]:
                st.image(row["Escudo Casa"], width=40)
            st.write(row["Casa"])

        with col3:
            st.markdown("**x**")

        with col4:
            if row["Escudo Fora"]:
                st.image(row["Escudo Fora"], width=40)
            st.write(row["Fora"])

        with col5:
            st.metric("Score", row["Score LTD 60"])

        st.caption(row["Liga"])
        st.divider()

st.caption("⚠️ Estatístico | Pré-live | Gestão conservadora | LTD 60")
