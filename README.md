# Projeto de Recomendação de Estoque de Cilindros

Este projeto utiliza Machine Learning para analisar dados de estoque, pedidos e enchimentos, fornecendo recomendações de estoque mínimas para cilindros de gás. A aplicação inclui uma interface interativa desenvolvida com Streamlit.

## Estrutura do Projeto

```
├── adapters/
│   └── matraca_adapter.py
├── data/
│   ├── enchimento.py
│   ├── pedidos.py
│   └── controleCilindros.py
|   └── gasType.py
├── services/
│   └── inventory_recommendation_service.py
├── app_streamlit.py
└── requirements.txt
```

### 1. **`adapters/matraca_adapter.py`**

Implementa a classe `MatracaAdapter` para integração com o modelo MariTalk. Esta classe é responsável por gerar respostas baseadas em prompts fornecidos.

#### Principais métodos:
- `__init__(self, api_key, model_name)`: Inicializa a conexão com o modelo MariTalk.
- `generate_response(self, prompt, max_tokens)`: Gera a resposta baseada no prompt fornecido.

### 2. **`data/`**

Contém os dados usados para análise e recomendação:
- **`enchimento.py`**: Dados históricos de enchimento de cilindros.
- **`pedidos.py`**: Histórico de pedidos de cilindros.
- **`controleCilindros.py`**: Informações sobre o estoque atual de cilindros.
- **`gasType.py`**: Informações sobre o tipos de gas existente.

### 3. **`services/inventory_recommendation_service.py`**

Fornece o serviço de recomendação de estoque com base nos dados analisados. Utiliza o `MatracaAdapter` para gerar respostas personalizadas.

#### Principais métodos:
- `analysis(self)`: Analisa os dados de pedidos, controle de cilindros e enchimentos.
- `get_stock_recommendation(self, selected_informations)`: Gera a recomendação de estoque mínimo.
- `format_response(recommendation_text)`: Formata a resposta da LLM para melhor leitura.

### 4. **`app_streamlit.py`**

Interface do usuário construída com Streamlit, permitindo selecionar o tipo de gás e o tamanho do cilindro para gerar recomendações de estoque.

#### Fluxo:
1. O usuário seleciona o tipo de gás.
2. Escolhe o tamanho do cilindro.
3. Clica em "Obter recomendação da LLM" para receber a recomendação.

### 5. **`requirements.txt`**

Lista as dependências necessárias para rodar o projeto.

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone <url_do_repositorio>
cd smart-stock
```

### 2. Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o aplicativo Streamlit

```bash
streamlit run app_streamlit.py
```

## Exemplo de Uso

1. Selecione o tipo de gás (por exemplo, "Oxigênio").
2. Escolha o tamanho do cilindro (por exemplo, "50L").
3. Clique em "Obter recomendação da LLM" para visualizar a recomendação de estoque mínimo.

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias para o projeto.

---

**Autor:** Túlio Ferreira Franco Carvalho

