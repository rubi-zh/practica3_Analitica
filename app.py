import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NBA Dashboard", layout="wide")

st.title("Dashboard NBA")

#dataset
@st.cache_data
def load_data():
    df = pd.read_csv("nba_all_elo.csv")
    df = df.dropna(subset=["team_id", "year_id", "game_result"])
    df["date_game"] = pd.to_datetime(df["date_game"])
    return df
df = load_data()

#barra lateral
st.sidebar.header("Filtros")
años = sorted(df["year_id"].unique(), reverse=True)
año_seleccionado = st.sidebar.selectbox("Selecciona año", años)

equipo = sorted(df["team_id"].unique())
equipo_seleccionado = st.sidebar.selectbox("Selecciona equipo", equipo)

tipo_juego = st.sidebar.radio(
    "Tipo de juego",
    ("Regular", "Playoffs", "Ambos"))

df_fil = df[(df["year_id"] == año_seleccionado) & (df["team_id"] == equipo_seleccionado)]

if tipo_juego == "Temporada Regular":
    df_fil = df_fil[df_fil["is_playoffs"] == 0]
elif tipo_juego == "Playoffs":
    df_fil = df_fil[df_fil["is_playoffs"] == 1]

st.subheader(f"Rendimiento de {equipo_seleccionado} en {año_seleccionado}")

if df_fil.empty:
    st.warning("No hay datos disponibles para este equipo y año")
else:
    df_fil["ganados"] = (df_fil["game_result"] == "W").cumsum()
    df_fil["perdidos"] = (df_fil["game_result"] == "L").cumsum()

    #gráfica 1
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_fil["date_game"], df_fil["ganados"], label="Juegos Ganados", color="#1447E6")
    ax.plot(df_fil["date_game"], df_fil["perdidos"], label="Juegos Perdidos", color="#C11007")
    ax.set_xlabel("Fecha del juego")
    ax.set_ylabel("Juegos acumulados")
    ax.legend()
    st.pyplot(fig)

    #gráfica 2
    st.subheader("Porcentaje de juegos ganados vs perdidos")
    win_count = (df_fil["game_result"] == "W").sum()
    loss_count = (df_fil["game_result"] == "L").sum()

    fig2, ax2 = plt.subplots(figsize=(2, 2)) 
    ax2.pie(
        [win_count, loss_count],
        labels=["Ganados", "Perdidos"],
        autopct="%1.1f%%",
        colors=["#1447E6", "#C11007"])
    ax2.axis("equal")  
    st.pyplot(fig2, use_container_width=False)











