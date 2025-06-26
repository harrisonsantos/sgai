import requests
import streamlit as st
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

def geocode_address(address):
    """
    Converte um endereço em coordenadas de latitude e longitude usando a API Nominatim.
    """
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    
    # Headers required by Nominatim to avoid 403 errors
    headers = {
        'User-Agent': 'SistemaAnotacaoImoveis/1.0 (https://github.com/user/sistema-anotacao-imoveis; user@example.com)',
        'Accept': 'application/json',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
    }
    
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        
        # Check if we got a successful response
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon
            else:
                st.warning(f"Endereço não encontrado: {address}. Por favor, verifique o endereço.")
                return None, None
        else:
            # If we get a 403 but the response contains data, try to parse it anyway
            if response.status_code == 403 and response.text:
                try:
                    data = response.json()
                    if data:
                        lat = float(data[0]["lat"])
                        lon = float(data[0]["lon"])
                        st.info("Geocodificação realizada com sucesso!")
                        return lat, lon
                except:
                    pass
            
            st.error(f"Erro ao conectar à API de geocodificação: {response.status_code} {response.reason}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar à API de geocodificação: {e}")
        return None, None
    except Exception as e:
        st.error(f"Erro inesperado durante a geocodificação: {e}")
        return None, None



