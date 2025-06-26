import requests
from bs4 import BeautifulSoup
from groq import Groq
import json
import os
from datetime import date

def get_page_content(url: str) -> str:
    """Fetches the content of a web page and extracts its plain text."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.extract()
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while processing {url}: {e}")
        return ""

def extract_property_data(text_content: str, groq_api_key: str) -> dict:
    """
    Uses Groq LLM to extract property data from text content.
    """
    if not text_content:
        return {}

    client = Groq(api_key=groq_api_key)

    prompt = f"""
    You are an expert real estate data extractor. Your task is to extract specific property details from the provided text content.
    The text content may come from various sources like OLX, Facebook Marketplace, or other Brazilian retail pages.
    Extract the following information and return it as a JSON object.
    If a piece of information is not found, use a sensible default or null if no default is applicable.

    Required Fields:
    - "Endereço": Full address of the property. Be as specific as possible.
    - "Tamanho (m²)": Size of the property in square meters. Extract only the number.
    - "Quartos": Number of bedrooms. Extract only the number.
    - "Banheiros": Number of bathrooms. Extract only the number.
    - "Preço do Aluguel (R$)": Rent price in Brazilian Reais. Extract only the number.
    - "Observações": Any additional relevant details or descriptions about the property.
    - "Qualidade": A quality rating from 1 to 5 stars, inferring from the description. Default to 3 if not clear.
    - "Data da Visita": The date of the visit or listing date. Default to today's date if not specified. Format as YYYY-MM-DD.

    Example JSON Output:
    {{
        "Endereço": "Rua da Paz, 123, Centro, São Paulo - SP",
        "Tamanho (m²)": 150.0,
        "Quartos": 3,
        "Banheiros": 2,
        "Preço do Aluguel (R$)": 2500.00,
        "Observações": "Apartamento reformado, próximo ao metrô, com varanda gourmet.",
        "Qualidade": 4,
        "Data da Visita": "2023-10-26"
    }}

    Text Content:
    {text_content}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192", # Using a smaller, faster model for extraction
            response_format={"type": "json_object"},
            temperature=0.0, # Keep temperature low for factual extraction
        )
        response_content = chat_completion.choices[0].message.content
        extracted_data = json.loads(response_content)

        # Ensure numerical fields are correctly typed
        for key in ["Tamanho (m²)", "Preço do Aluguel (R$)"]:
            if key in extracted_data and extracted_data[key] is not None:
                try:
                    extracted_data[key] = float(extracted_data[key])
                except (ValueError, TypeError):
                    extracted_data[key] = None # Or a default value

        for key in ["Quartos", "Banheiros", "Qualidade"]:
            if key in extracted_data and extracted_data[key] is not None:
                try:
                    extracted_data[key] = int(extracted_data[key])
                except (ValueError, TypeError):
                    extracted_data[key] = None # Or a default value

        # Ensure Data da Visita is in YYYY-MM-DD format
        if "Data da Visita" not in extracted_data or not extracted_data["Data da Visita"]:
            extracted_data["Data da Visita"] = date.today().strftime("%Y-%m-%d")
        
        # Ensure Qualidade is within 1-5 range
        if "Qualidade" in extracted_data and extracted_data["Qualidade"] is not None:
            extracted_data["Qualidade"] = max(1, min(5, extracted_data["Qualidade"]))
        else:
            extracted_data["Qualidade"] = 3 # Default quality

        return extracted_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from LLM response: {e}")
        print(f"LLM Raw Response: {response_content}")
        return {}
    except Exception as e:
        print(f"Error during LLM extraction: {e}")
        return {}

if __name__ == "__main__":
    # Example Usage (replace with a real URL and your API key)
    # You should set your GROQ_API_KEY as an environment variable
    # For testing, you can temporarily set it like:
    # os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
    
    test_url = "https://www.olx.com.br/imoveis/anuncio/apartamento-3-quartos-centro-sp-123456789" # Replace with a real URL
    groq_key = os.getenv("GROQ_API_KEY")

    if not groq_key:
        print("GROQ_API_KEY environment variable not set. Please set it to run the example.")
    else:
        print(f"Fetching content from: {test_url}")
        content = get_page_content(test_url)
        if content:
            print("\n--- Extracted Text Content (first 500 chars) ---")
            print(content[:500])
            print("\n--- Extracting Property Data ---")
            property_data = extract_property_data(content, groq_key)
            print("\n--- Extracted Property Data ---")
            print(json.dumps(property_data, indent=2, ensure_ascii=False))
        else:
            print("Failed to get page content.")
