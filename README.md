# Smart-Stock: Recomendador de Estoque de Cilindros

Este projeto utiliza Machine Learning para analisar dados de estoque, pedidos e enchimentos, fornecendo recomendações de estoque mínimas para cilindros de gás. A interface interativa é desenvolvida com Streamlit.

## Estrutura do Projeto

```
├── adapters/
│   ├── llm_adapter.py
│   ├── matraca_adapter.py
│   └── openai_adapter.py
├── data/
│   ├── controleCilindros.py
│   ├── enchimento.py
│   ├── gasType.py
│   └── pedidos.py
├── services/
│   └── inventory_recommendation_service.py
├── app_streamlit.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

### Descrição dos Módulos

#### 1. **`adapters/`**
Contém adaptadores para integração com modelos de linguagem e APIs externas:
- **`llm_adapter.py`**: Adapta a interação com modelos de linguagem para diferentes provedores.
- **`matraca_adapter.py`**: Integra o modelo MariTalk, gerando respostas baseadas em prompts.
- **`openai_adapter.py`**: Adaptador para a API da OpenAI.

#### 2. **`data/`**
Armazena dados e funções relacionadas ao gerenciamento de cilindros:
- **`controleCilindros.py`**: Informações sobre o estoque atual.
- **`enchimento.py`**: Dados históricos de enchimento.
- **`gasType.py`**: Tipos de gás disponíveis.
- **`pedidos.py`**: Histórico de pedidos.

#### 3. **`services/`**
Contém serviços de backend para análise e recomendação:
- **`inventory_recommendation_service.py`**: Analisa dados e fornece recomendações de estoque mínimo com base nos inputs fornecidos.

#### 4. **`app_streamlit.py`**
Implementa a interface do usuário utilizando Streamlit. Permite a seleção de tipo de gás e tamanho do cilindro para gerar recomendações de estoque.

#### 5. **`requirements.txt`**
Lista todas as dependências do projeto.

### Principais Funcionalidades

- Seleção do tipo de gás e tamanho do cilindro.
- Recomendacão automatizada de estoque mínimo.
- Integração com modelos de linguagem para análises detalhadas.

## Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone <url_do_repositorio>
cd smart-stock
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` com suas chaves de API e configurações necessárias.

### 5. Executar o Aplicativo Streamlit

```bash
streamlit run app_streamlit.py
```

## Exemplo de Uso

1. Selecione o tipo de gás (por exemplo, "Oxigênio").
2. Escolha o tamanho do cilindro (por exemplo, "50L").
3. Clique em "Obter recomendação da LLM" para visualizar a recomendação.

---

**Autor:** Túlio Ferreira Franco Carvalho

