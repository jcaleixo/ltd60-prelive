import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="LTD 60 • Pré-Live",
    page_icon="⚽",
    layout="wide"
)

# =========================
# ESTILO (VERDE TRADER)
# =========================
st.markdown("""
<style>
body { background-color: #0e1b16; }
.block-container { padding-top: 2rem; }
h1, h2, h3, h4 { color: #2ecc71; }
p, span, div { color: #eafaf1; }
.stButton>button {
    background-color: #2ecc71;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
.card {
    background-color: #13251d;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("⚽ LTD 60 — Pré-Live")
st.caption("Seleção automática • Filtros equilibrados–conservadores • 100% gratuito")

# =========================
# DADOS (EXEMPLO PRÉ-LIVE)
# =========================
dados = [
    ["16:00", "Premier League", "Arsenal x Fulham", 74, 72, 34],
    ["17:30", "La Liga", "Villarreal x Getafe", 69, 71, 36],
    ["19:00", "Serie A", "Atalanta x Lecce", 81, 78, 31],
    ["21:45", "Ligue 1", "Lyon x Metz", 61, 66, 41],
]

df = pd.DataFrame(dados, columns=[
    "Horário", "Liga", "Jogo",
    "% Gol até 60", "Over 0.5 HT", "Min 1º Gol"
])

# =========================
# FILTRO LTD 60
# =========================
filtro = df[
    (df["% Gol até 60"] >= 68) &
    (df["Over 0.5 HT"] >= 70) &
    (df["Min 1º Gol"] <= 38)
]

# =========================
# EXIBIÇÃO
# =========================
st.subheader("📅 Jogos Aprovados")

if filtro.empty:
    st.warning("Nenhum jogo encaixa no método LTD 60 hoje.")
else:
    for _, row in filtro.iterrows():
        st.markdown(f"""
        <div class="card">
            ⏰ <b>{row['Horário']}</b> — 🏆 {row['Liga']}<br>
            ⚽ <b>{row['Jogo']}</b><br>
            📊 Gol até 60: <b>{row['% Gol até 60']}%</b> |
            ⏱️ Min 1º Gol: <b>{row['Min 1º Gol']}'</b><br>
            🟢 <b>APTO LTD 60</b>
        </div>
        """, unsafe_allow_html=True)

st.caption(f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
