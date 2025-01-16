
# Roleplay: Ferramenta de Feedback para Aprendizado de Inglês

O **Roleplay** é uma aplicação que utiliza modelos de linguagem para oferecer feedback personalizado em frases em inglês. Ele foi projetado para ajudar no aprendizado e prática de situações do dia a dia, oferecendo sugestões e correções de forma interativa. A interface foi desenvolvida com **Streamlit**.

## Estrutura do Projeto

```
├── adapters/
│   ├── llm_adapter.py
│   ├── maritaca_adapter.py
│   └── openai_adapter.py
├── services/
│   └── roleplay_feedback_service.py
├── venv/
├── .env
├── .gitignore
├── app_streamlit.py
├── README.md
└── requirements.txt
```

### Descrição dos Módulos

#### 1. **`adapters/`**
Contém adaptadores para integração com APIs externas e modelos de linguagem:
- **`llm_adapter.py`**: Adapta a interação com diferentes provedores de modelos de linguagem.
- **`maritaca_adapter.py`**: Integra com o modelo Maritaca para feedback de frases.
- **`openai_adapter.py`**: Adaptador para a API da OpenAI.

#### 2. **`services/`**
Contém serviços que fornecem a lógica principal do projeto:
- **`roleplay_feedback_service.py`**: Processa frases em inglês e retorna feedback detalhado, incluindo correções e sugestões.

#### 3. **`app_streamlit.py`**
Interface interativa desenvolvida com **Streamlit**, permitindo que os usuários insiram frases e recebam feedback de maneira intuitiva.

#### 4. **`requirements.txt`**
Lista de dependências necessárias para executar o projeto.

---

## Principais Funcionalidades

- **Correção gramatical**: Identificação de erros e sugestões de melhoria.
- **Sugestões de variações**: Oferece frases alternativas em contextos formais e amigáveis.
- **Interface interativa**: Usuários podem inserir frases e receber feedback em tempo real.

---

## Como Executar o Projeto

### 1. Clonar o Repositório

```bash
git clone https://github.com/tuliofranco/Roleplay.git
cd Roleplay
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

Crie um arquivo `.env` com as configurações necessárias, como chaves de API.

### 5. Executar o Aplicativo Streamlit

```bash
streamlit run app_streamlit.py
```

---

## Exemplo de Uso

1. Insira uma frase em inglês na interface do **Roleplay**.
2. Receba um feedback objetivo, com:
   - Correções gramaticais.
   - Sugestões de variações formais e informais.
3. Use o feedback para aprimorar sua comunicação em inglês.

---

**Autor:** Túlio Ferreira Franco Carvalho  
**Licença:** MIT  
