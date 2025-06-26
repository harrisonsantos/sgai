import pandas as pd
import os

DATA_FILE = 'imoveis.csv'

def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Garantir que a coluna URL seja string
        if 'URL' in df.columns:
            df['URL'] = df['URL'].astype(str)
        return df
    return pd.DataFrame(columns=[
        'Endereço', 'Tamanho (m²)', 'Quartos', 'Banheiros', 'Preço do Aluguel (R$)',
        'Observações', 'Qualidade', 'Data da Visita', 'Latitude', 'Longitude', 'URL'
    ])

def save_data(df):
    # Garantir que a coluna URL seja string
    if 'URL' in df.columns:
        df['URL'] = df['URL'].astype(str)
    df.to_csv(DATA_FILE, index=False)



