# Sistema de Anotação de Imóveis

Este é um aplicativo Streamlit para gerenciar e visualizar informações de imóveis que você está visitando para aluguel.

## Funcionalidades:

- **Cadastro de Imóveis**: Formulário para inserir dados detalhados do imóvel, incluindo endereço, tamanho, número de quartos/banheiros, preço, observações, qualidade (1-5 estrelas), data da visita.
- **Visualização em Mapa**: Exibe todos os imóveis cadastrados em um mapa interativo (Folium), com marcadores coloridos baseados na qualidade e popups com informações resumidas. Inclui filtros por preço, quartos e qualidade.
- **Geocodificação Automática**: Converte endereços em coordenadas de latitude e longitude usando a API Nominatim (OpenStreetMap).
- **Gestão de Dados**: Armazena os dados em um arquivo CSV local (`imoveis.csv`). Permite editar e excluir imóveis cadastrados através de uma interface de tabela.
- **Análises e Relatórios**: Apresenta estatísticas básicas (preço médio, tamanho médio, total de imóveis) e gráficos (distribuição de preços por qualidade, contagem de imóveis por quartos), além de um ranking dos imóveis mais bem avaliados.

## Requisitos:

Certifique-se de ter Python 3.7+ instalado.

## Instalação:

1. Clone este repositório (ou crie os arquivos manualmente):
   ```bash
   git clone <URL_DO_REPOSITORIO> # Se este fosse um repositório git
   cd imoveis_app
   ```

2. Instale as dependências necessárias. Você pode encontrar a lista no arquivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Conteúdo de `requirements.txt`:
   ```
   streamlit
   folium
   streamlit-folium
   pandas
   requests
   plotly
   ```

## Como Executar:

Após a instalação das dependências, navegue até o diretório `imoveis_app` e execute o aplicativo Streamlit:

```bash
streamlit run app.py
```

Isso abrirá o aplicativo no seu navegador padrão (geralmente `http://localhost:8501`).

## Estrutura do Projeto:

```
imoveis_app/
├── app.py             # Página principal e navegação
├── data.py            # Funções para carregar e salvar dados (CSV)
├── utils.py           # Funções utilitárias, incluindo geocodificação
├── requirements.txt   # Dependências do projeto
└── pages/
    ├── cadastro.py    # Página para cadastrar novos imóveis
    ├── mapa.py        # Página com o mapa interativo dos imóveis
    ├── lista.py       # Página para listar, editar e excluir imóveis
    └── estatisticas.py # Página com análises e gráficos
```

## Observações:

- Os dados são persistidos em um arquivo `imoveis.csv` no mesmo diretório da aplicação.
- A geocodificação utiliza a API pública do Nominatim (OpenStreetMap), que possui limites de uso. Para uso intensivo, considere configurar seu próprio servidor Nominatim ou usar uma API comercial.


