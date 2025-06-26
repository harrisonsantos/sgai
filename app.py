import streamlit as st

st.set_page_config(
    page_title="Sistema de Anotação de Imóveis",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Sistema de Anotação de Imóveis")

st.write("Bem-vindo ao Sistema de Anotação de Imóveis!")
st.write("Use os botões abaixo para navegar entre as funcionalidades.")

# Navigation menu in main screen
st.subheader("📋 Menu de Navegação")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🗺️ Mapa de Imóveis", use_container_width=True):
        st.switch_page("app.py")

with col2:
    if st.button("✏️ Cadastrar Imóvel", use_container_width=True):
        st.switch_page("pages/cadastro.py")

with col3:
    if st.button("📋 Listar Imóveis", use_container_width=True):
        st.switch_page("pages/lista.py")

with col4:
    if st.button("📊 Estatísticas", use_container_width=True):
        st.switch_page("pages/estatisticas.py")

st.markdown("---")

# Main content area
st.subheader("🚀 Comece Agora")
st.write("**Para começar:**")
st.write("1. 📝 **Cadastre um novo imóvel** - Adicione informações sobre propriedades que você visitou")
st.write("2. 🗺️ **Visualize no mapa** - Veja todos os imóveis em um mapa interativo")
st.write("3. 📋 **Gerencie a lista** - Edite ou exclua imóveis cadastrados")
st.write("4. 📊 **Analise estatísticas** - Veja gráficos e análises dos seus dados")

st.markdown("---")

# Quick stats if data exists
try:
    from data import load_data
    df = load_data()
    if not df.empty:
        st.subheader("📈 Resumo Rápido")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Imóveis", len(df))
        with col2:
            st.metric("Preço Médio", f"R$ {df['Preço do Aluguel (R$)'].mean():,.0f}")
        with col3:
            st.metric("Melhor Avaliação", f"{df['Qualidade'].max()} ⭐")
except:
    pass



