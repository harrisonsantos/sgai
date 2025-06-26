import streamlit as st
from datetime import date
from utils import geocode_address
from data import load_data, save_data
from scraper import get_page_content, extract_property_data
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Cadastrar Imóvel",
    page_icon="✏️",
    layout="wide",
)

st.title("Cadastrar Novo Imóvel")

# Initialize session state for form fields
if "endereco" not in st.session_state:
    st.session_state.endereco = ""
if "tamanho" not in st.session_state:
    st.session_state.tamanho = 1.0
if "quartos" not in st.session_state:
    st.session_state.quartos = 0
if "banheiros" not in st.session_state:
    st.session_state.banheiros = 0
if "preco_aluguel" not in st.session_state:
    st.session_state.preco_aluguel = 0.0
if "observacoes" not in st.session_state:
    st.session_state.observacoes = ""
if "qualidade" not in st.session_state:
    st.session_state.qualidade = 3
if "data_visita" not in st.session_state:
    st.session_state.data_visita = date.today()
if "url_imovel" not in st.session_state:
    st.session_state.url_imovel = ""

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.warning("GROQ_API_KEY environment variable not set. Auto-fill feature will be disabled.")

url_input = st.text_input("URL da Página do Imóvel (Opcional)", help="Cole o link de uma página de imóvel para preencher automaticamente.")
auto_fill_button = st.button("Preencher Automaticamente", disabled=not groq_api_key)

if auto_fill_button and url_input:
    with st.spinner("Extraindo dados da página..."):
        text_content = get_page_content(url_input)
        if text_content:
            extracted_data = extract_property_data(text_content, groq_api_key)
            if extracted_data:
                st.session_state.endereco = extracted_data.get("Endereço", "")
                st.session_state.tamanho = extracted_data.get("Tamanho (m²)", 1.0)
                st.session_state.quartos = extracted_data.get("Quartos", 0)
                st.session_state.banheiros = extracted_data.get("Banheiros", 0)
                st.session_state.preco_aluguel = extracted_data.get("Preço do Aluguel (R$)", 0.0)
                st.session_state.observacoes = extracted_data.get("Observações", "")
                st.session_state.qualidade = extracted_data.get("Qualidade", 3)
                st.session_state.url_imovel = url_input  # Save the URL
                
                # Handle date conversion
                date_str = extracted_data.get("Data da Visita")
                if date_str:
                    try:
                        st.session_state.data_visita = date.fromisoformat(date_str)
                    except ValueError:
                        st.session_state.data_visita = date.today()
                else:
                    st.session_state.data_visita = date.today()

                st.success("Dados extraídos e formulário preenchido! Revise as informações antes de cadastrar.")
            else:
                st.error("Não foi possível extrair os dados da página. Verifique a URL ou tente preencher manualmente.")
        else:
            st.error("Não foi possível carregar o conteúdo da página. Verifique a URL ou sua conexão.")

with st.form("cadastro_imovel_form"):
    endereco = st.text_input("Endereço Completo", value=st.session_state.endereco, help="Ex: Rua da Paz, 123, Centro, São Paulo - SP", key="form_endereco")
    tamanho = st.number_input("Tamanho (m²)", min_value=1.0, format="%.2f", value=st.session_state.tamanho, key="form_tamanho")
    quartos = st.number_input("Número de Quartos", min_value=0, step=1, value=st.session_state.quartos, key="form_quartos")
    banheiros = st.number_input("Número de Banheiros", min_value=0, step=1, value=st.session_state.banheiros, key="form_banheiros")
    preco_aluguel = st.number_input("Preço do Aluguel (R$)", min_value=0.0, format="%.2f", value=st.session_state.preco_aluguel, key="form_preco_aluguel")
    observacoes = st.text_area("Observações Gerais", value=st.session_state.observacoes, key="form_observacoes")
    qualidade = st.slider("Marcador de Qualidade (1-5 estrelas)", min_value=1, max_value=5, step=1, value=st.session_state.qualidade, key="form_qualidade")
    data_visita = st.date_input("Data da Visita", value=st.session_state.data_visita, key="form_data_visita")

    # TODO: Adicionar upload de fotos

    submitted = st.form_submit_button("Cadastrar Imóvel")

    if submitted:
        # Update session state with current form values before processing
        st.session_state.endereco = endereco
        st.session_state.tamanho = tamanho
        st.session_state.quartos = quartos
        st.session_state.banheiros = banheiros
        st.session_state.preco_aluguel = preco_aluguel
        st.session_state.observacoes = observacoes
        st.session_state.qualidade = qualidade
        st.session_state.data_visita = data_visita

        if st.session_state.endereco:
            lat, lon = geocode_address(st.session_state.endereco)
            if lat is not None and lon is not None:
                df = load_data()
                new_imovel = {
                    "Endereço": st.session_state.endereco,
                    "Tamanho (m²)": st.session_state.tamanho,
                    "Quartos": st.session_state.quartos,
                    "Banheiros": st.session_state.banheiros,
                    "Preço do Aluguel (R$)": st.session_state.preco_aluguel,
                    "Observações": st.session_state.observacoes,
                    "Qualidade": st.session_state.qualidade,
                    "Data da Visita": st.session_state.data_visita.strftime("%Y-%m-%d"),
                    "Latitude": lat,
                    "Longitude": lon,
                    "URL": st.session_state.url_imovel
                }
                # Use pandas.concat instead of deprecated _append
                new_df = pd.DataFrame([new_imovel])
                df = pd.concat([df, new_df], ignore_index=True)
                save_data(df)
                st.success("Imóvel cadastrado com sucesso!")
                # Clear form fields after successful submission
                st.session_state.endereco = ""
                st.session_state.tamanho = 1.0
                st.session_state.quartos = 0
                st.session_state.banheiros = 0
                st.session_state.preco_aluguel = 0.0
                st.session_state.observacoes = ""
                st.session_state.qualidade = 3
                st.session_state.data_visita = date.today()
                st.session_state.url_imovel = ""
            else:
                st.error("Não foi possível geocodificar o endereço. Por favor, tente novamente com um endereço mais específico.")
        else:
            st.error("Por favor, preencha o campo Endereço Completo.")
