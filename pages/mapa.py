import streamlit as st
import folium
from streamlit_folium import st_folium
from data import load_data
import pandas as pd

st.set_page_config(
    page_title="Mapa de Imóveis",
    page_icon="🗺️",
    layout="wide",
)

st.title("Mapa de Imóveis")

df = load_data()

if not df.empty:
    st.sidebar.header("Filtros do Mapa")

    # Filtro por preço
    min_price, max_price = float(df["Preço do Aluguel (R$)"].min()), float(df["Preço do Aluguel (R$)"].max())
    
    # Ensure min_value is less than max_value for sliders
    if min_price == max_price:
        # If all properties have the same price, create a range around it
        price_range = (min_price - 100, min_price + 100)
        st.sidebar.info(f"Todos os imóveis têm o mesmo preço: R$ {min_price:,.0f}")
    else:
        price_range = st.sidebar.slider(
            "Faixa de Preço (R$)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=1000.0
        )

    # Filtro por número de quartos
    min_quartos, max_quartos = int(df["Quartos"].min()), int(df["Quartos"].max())
    
    if min_quartos == max_quartos:
        # If all properties have the same number of rooms, create a range around it
        quartos_range = (max(0, min_quartos - 1), min_quartos + 1)
        st.sidebar.info(f"Todos os imóveis têm {min_quartos} quarto(s)")
    else:
        quartos_range = st.sidebar.slider(
            "Número de Quartos",
            min_value=min_quartos,
            max_value=max_quartos,
            value=(min_quartos, max_quartos),
            step=1
        )

    # Filtro por avaliação de qualidade
    min_qualidade, max_qualidade = int(df["Qualidade"].min()), int(df["Qualidade"].max())
    
    if min_qualidade == max_qualidade:
        # If all properties have the same quality, create a range around it
        qualidade_range = (max(1, min_qualidade - 1), min(5, max_qualidade + 1))
        st.sidebar.info(f"Todos os imóveis têm {min_qualidade} estrela(s)")
    else:
        qualidade_range = st.sidebar.slider(
            "Avaliação de Qualidade (estrelas)",
            min_value=min_qualidade,
            max_value=max_qualidade,
            value=(min_qualidade, max_qualidade),
            step=1
        )

    # Aplicar filtros
    filtered_df = df[
        (df["Preço do Aluguel (R$)"] >= price_range[0]) &
        (df["Preço do Aluguel (R$)"] <= price_range[1]) &
        (df["Quartos"] >= quartos_range[0]) &
        (df["Quartos"] <= quartos_range[1]) &
        (df["Qualidade"] >= qualidade_range[0]) &
        (df["Qualidade"] <= qualidade_range[1])
    ]

    if not filtered_df.empty:
        # Centralizar o mapa na média das coordenadas dos imóveis filtrados
        map_center = [filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()]
        m = folium.Map(location=map_center, zoom_start=12)

        for index, row in filtered_df.iterrows():
            # Build popup HTML with URL if available
            popup_html = f"""
                <b>Endereço:</b> {row["Endereço"]}<br>
                <b>Preço:</b> R$ {row["Preço do Aluguel (R$)"]:,}<br>
                <b>Quartos:</b> {int(row["Quartos"])}<br>
                <b>Banheiros:</b> {int(row["Banheiros"])}<br>
                <b>Qualidade:</b> {int(row["Qualidade"])} estrelas
            """
            
            # Add URL to popup if available
            if "URL" in row and pd.notna(row["URL"]) and row["URL"] != "":
                popup_html += f'<br><b>URL:</b> <a href="{row["URL"]}" target="_blank">Ver anúncio</a>'
            
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color="blue" if row["Qualidade"] >= 4 else "green" if row["Qualidade"] >= 2 else "red")
            ).add_to(m)

        st_folium(m, width=1000, height=600)
    else:
        st.info("Nenhum imóvel encontrado com os filtros selecionados.")
else:
    st.info("Nenhum imóvel cadastrado ainda. Cadastre um imóvel para vê-lo no mapa.")


