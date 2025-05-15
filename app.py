import streamlit as st
import pandas as pd
import folium
from folium import Marker, PolyLine
from streamlit_folium import st_folium

# Tytuł aplikacji
st.set_page_config(page_title="Mapa Polski - Trasa między miejscowościami", layout="wide")
st.title("🗺️ Trasa między miejscowościami w Polsce")

# Wczytaj dane miejscowości z pliku CSV
@st.cache_data
def load_data():
    return pd.read_csv("miejscowosci_gus_sample.csv")

df = load_data()

# Lista dostępnych miejscowości
miejscowosci = df["Nazwa"].tolist()

# Formularz wyboru
col1, col2 = st.columns(2)
with col1:
    z_miejscowosc = st.selectbox("Wybierz miejscowość początkową (Z):", miejscowosci)
with col2:
    do_miejscowosc = st.selectbox("Wybierz miejscowość docelową (Do):", miejscowosci)

# Pobierz współrzędne
z_coords = df[df["Nazwa"] == z_miejscowosc][["Lat", "Lon"]].values[0]
do_coords = df[df["Nazwa"] == do_miejscowosc][["Lat", "Lon"]].values[0]

# Środek mapy
map_center = [(z_coords[0] + do_coords[0]) / 2, (z_coords[1] + do_coords[1]) / 2]

# Tworzenie mapy
m = folium.Map(location=map_center, zoom_start=6)
Marker(z_coords, popup=f"Z: {z_miejscowosc}", icon=folium.Icon(color="green")).add_to(m)
Marker(do_coords, popup=f"Do: {do_miejscowosc}", icon=folium.Icon(color="red")).add_to(m)
PolyLine([z_coords, do_coords], color="blue", weight=4.5, opacity=0.8).add_to(m)

# Wyświetl mapę
st_folium(m, width=1000, height=600)
