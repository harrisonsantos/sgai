import streamlit as st
import pandas as pd
from data import load_data, save_data
from utils import geocode_address

st.set_page_config(
    page_title="Listar Imóveis",
    page_icon="📋",
    layout="wide",
)

st.title("Lista de Imóveis Cadastrados")

df = load_data()

if df.empty:
    st.info("Nenhum imóvel cadastrado ainda.")
else:
    st.dataframe(df)

    st.subheader("Editar ou Excluir Imóvel")

    # Selecionar imóvel para edição/exclusão
    options = [f"{i+1} - {row['Endereço']}" for i, row in df.iterrows()]
    selected_option = st.selectbox("Selecione o imóvel para editar ou excluir:", options)

    if selected_option:
        selected_index = int(selected_option.split(" ")[0]) - 1
        selected_imovel = df.iloc[selected_index]

        st.write(f"Você selecionou o imóvel: **{selected_imovel['Endereço']}**")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Editar Imóvel")
            with st.form("edit_imovel_form"):
                edit_endereco = st.text_input("Endereço Completo", value=selected_imovel["Endereço"])
                edit_tamanho = st.number_input("Tamanho (m²)", value=float(selected_imovel["Tamanho (m²)"]), format="%.2f")
                edit_quartos = st.number_input("Número de Quartos", value=int(selected_imovel["Quartos"]), step=1)
                edit_banheiros = st.number_input("Número de Banheiros", value=int(selected_imovel["Banheiros"]), step=1)
                edit_preco_aluguel = st.number_input("Preço do Aluguel (R$)", value=float(selected_imovel["Preço do Aluguel (R$)"]), format="%.2f")
                edit_observacoes = st.text_area("Observações Gerais", value=selected_imovel["Observações"])
                edit_qualidade = st.slider("Marcador de Qualidade (1-5 estrelas)", min_value=1, max_value=5, step=1, value=int(selected_imovel["Qualidade"]))
                edit_data_visita = st.date_input("Data da Visita", value=pd.to_datetime(selected_imovel["Data da Visita"]).date())
                edit_url = st.text_input("URL do Imóvel", value=selected_imovel.get("URL", ""), help="Link da página onde o imóvel foi encontrado")

                edited = st.form_submit_button("Salvar Alterações")

                if edited:
                    lat, lon = geocode_address(edit_endereco)
                    if lat is not None and lon is not None:
                        df.loc[selected_index] = {
                            "Endereço": edit_endereco,
                            "Tamanho (m²)": edit_tamanho,
                            "Quartos": edit_quartos,
                            "Banheiros": edit_banheiros,
                            "Preço do Aluguel (R$)": edit_preco_aluguel,
                            "Observações": edit_observacoes,
                            "Qualidade": edit_qualidade,
                            "Data da Visita": edit_data_visita.strftime("%Y-%m-%d"),
                            "Latitude": lat,
                            "Longitude": lon,
                            "URL": edit_url
                        }
                        save_data(df)
                        st.success("Imóvel atualizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Não foi possível geocodificar o endereço. Por favor, tente novamente com um endereço mais específico.")

        with col2:
            st.subheader("Excluir Imóvel")
            if st.button("Excluir Imóvel", key="delete_button"):
                df = df.drop(selected_index).reset_index(drop=True)
                save_data(df)
                st.success("Imóvel excluído com sucesso!")
                st.rerun()


