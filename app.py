import streamlit as st
import pandas as pd

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================
st.set_page_config(
    page_title="LTD 60 Premium",
    layout="wide"
)

# ==============================
# TÍTULO
# ==============================
st.title("📊 LTD 60 Premium – Jogos do Dia")
st.caption("Pré-live | Método conservador | Filtro automático Gol até 60’")

st.divider()

# ==============================
# DADOS (BASE ESTÁVEL)
# ==============================
dados = [
    ["14:00", "Premier League", "Arsenal x Fulham", 74, 72, 34],
    ["15:30", "La Liga", "Villarreal x Getafe", 69, 71, 36],
    ["16:45", "Serie A", "Atalanta x Lecce", 81, 78, 31],
    ["17:00", "Bundesliga", "Leverkusen x Mainz", 77, 74, 33],
    ["19:00", "Ligue 1", "Lyon x Metz", 61, 66, 41],
]

df = pd.DataFrame(
    dados,
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
# FILTRO LTD 60 (CONSERVADOR)
# ==============================
df_filtrado = df[
    (df["% Gol até 60"] >= 65) &
    (df["Over 0.5 HT"] >= 65) &
    (df["Min médio 1º Gol"] <= 38)
]

# ==============================
# MÉTRICA DE SCORE
# ==============================
df_filtrado["Score LTD 60"] = (
    df_filtrado["% Gol até 60"] * 0.5 +
    df_filtrado["Over 0.5 HT"] * 0.3 +
    (40 - df_filtrado["Min médio 1º Gol"]) * 0.2
).round(1)

# ==============================
# EXIBIÇÃO
# ==============================
st.subheader("✅ Jogos que encaixam no LTD 60")

if df_filtrado.empty:
    st.warning("Nenhum jogo passou no filtro hoje.")
else:
    st.dataframe(
        df_filtrado.sort_values("Score LTD 60", ascending=False),
        use_container_width=True
    )

st.divider()

# ==============================
# RODAPÉ
# ==============================
st.caption(
    "⚠️ Uso educacional | Método LTD 60 | Gestão conservadora | Pré-live"
)
