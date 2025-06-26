import streamlit as st
import pandas as pd
import plotly.express as px
from data import load_data

st.set_page_config(
    page_title="Estatísticas de Imóveis",
    page_icon="📊",
    layout="wide",
)

st.title("Estatísticas e Análises de Imóveis")

df = load_data()

if df.empty:
    st.info("Nenhum imóvel cadastrado ainda para gerar estatísticas.")
else:
    st.subheader("Estatísticas Básicas")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Imóveis", len(df))
    with col2:
        st.metric("Preço Médio do Aluguel (R$)", f"{df['Preço do Aluguel (R$)'].mean():,.2f}")
    with col3:
        st.metric("Tamanho Médio (m²)", f"{df['Tamanho (m²)'].mean():,.2f}")

    st.subheader("Distribuição de Preços por Qualidade")
    fig_price_quality = px.box(
        df,
        x="Qualidade",
        y="Preço do Aluguel (R$)",
        title="Distribuição de Preços por Qualidade",
        labels={
            "Qualidade": "Qualidade (estrelas)",
            "Preço do Aluguel (R$)": "Preço do Aluguel (R$)"
        }
    )
    st.plotly_chart(fig_price_quality, use_container_width=True)

    st.subheader("Contagem de Imóveis por Número de Quartos")
    fig_quartos = px.histogram(
        df,
        x="Quartos",
        title="Contagem de Imóveis por Número de Quartos",
        labels={
            "Quartos": "Número de Quartos",
            "count": "Contagem"
        },
        category_orders={"Quartos": sorted(df["Quartos"].unique())}
    )
    st.plotly_chart(fig_quartos, use_container_width=True)

    st.subheader("Ranking dos Imóveis Mais Bem Avaliados")
    df_sorted_quality = df.sort_values(by="Qualidade", ascending=False)
    st.dataframe(df_sorted_quality[["Endereço", "Qualidade", "Preço do Aluguel (R$)", "Tamanho (m²)"]].head(10))

    # Estatísticas sobre URLs
    if "URL" in df.columns:
        st.subheader("📊 Estatísticas sobre URLs")
        col1, col2 = st.columns(2)
        
        with col1:
            # Contagem de imóveis com URL
            imoveis_com_url = df["URL"].notna() & (df["URL"] != "")
            st.metric("Imóveis com URL", f"{imoveis_com_url.sum()}")
            st.metric("Imóveis sem URL", f"{len(df) - imoveis_com_url.sum()}")
        
        with col2:
            # Porcentagem de imóveis com URL
            percentual_com_url = (imoveis_com_url.sum() / len(df)) * 100
            st.metric("Percentual com URL", f"{percentual_com_url:.1f}%")
            
            # Imóveis com URL por qualidade
            if imoveis_com_url.sum() > 0:
                df_com_url = df[imoveis_com_url]
                qualidade_media_url = df_com_url["Qualidade"].mean()
                st.metric("Qualidade Média (com URL)", f"{qualidade_media_url:.1f} ⭐")
        
        # Lista de imóveis com URL
        if imoveis_com_url.sum() > 0:
            st.subheader("🔗 Imóveis com URL Cadastrada")
            df_com_url = df[imoveis_com_url]
            for idx, row in df_com_url.iterrows():
                with st.expander(f"📍 {row['Endereço']} - R$ {row['Preço do Aluguel (R$)']:,.0f}"):
                    st.write(f"**URL:** [{row['URL']}]({row['URL']})")
                    st.write(f"**Qualidade:** {row['Qualidade']} ⭐")
                    st.write(f"**Tamanho:** {row['Tamanho (m²)']} m²")
                    st.write(f"**Quartos:** {row['Quartos']} | **Banheiros:** {row['Banheiros']}")
                    if row['Observações']:
                        st.write(f"**Observações:** {row['Observações']}")


