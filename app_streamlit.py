import streamlit as st
from services.roleplay_feedback_service import RoleplayFeedbackService
import logging

# Configurando o sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Navegação simulada
page = st.sidebar.radio("Navegação", ["Home", "Roleplay ideas"])

if page == "Home":
    # Título do aplicativo
    st.title("Roleplay Mood - Practice your English")

    # Sugestões de limites de caracteres para cada entrada
    situation_limit = 270  # Aproximadamente 62 tokens
    phrase_pt_limit = 100  # Aproximadamente 25 tokens
    phrase_en_limit = 100  # Aproximadamente 25 tokens

    # Entrada para descrição da situação
    situation = st.text_area(
        f"Descreva a situação do roleplay (máximo {situation_limit} caracteres):",
        help=f"Ex: Estou em um restaurante tentando pedir uma refeição. (Máximo de {situation_limit} caracteres)"
    )

    # Validação do limite de caracteres para a situação
    if len(situation) > situation_limit:
        st.error(f"A descrição da situação ultrapassa o limite de {situation_limit} caracteres. Você usou {len(situation)} caracteres.")

    # Entrada para frase traduzida (em inglês)
    phrase_en = st.text_area(
        f"Escreva a frase como você a diria em inglês (máximo {phrase_en_limit} caracteres):",
        help=f"Ex: Could you please bring me a glass of water? (Máximo de {phrase_en_limit} caracteres)"
    )

    # Validação do limite de caracteres para a frase em inglês
    if len(phrase_en) > phrase_en_limit:
        st.error(f"A frase em inglês ultrapassa o limite de {phrase_en_limit} caracteres. Você usou {len(phrase_en)} caracteres.")

    # Entrada para frase em português
    phrase_pt = st.text_area(
        f"Escreva o que você deseja dizer em português (máximo {phrase_pt_limit} caracteres):",
        help=f"Ex: Por favor, poderia me trazer um copo d'água? (Máximo de {phrase_pt_limit} caracteres)"
    )

    # Validação do limite de caracteres para a frase em português
    if len(phrase_pt) > phrase_pt_limit:
        st.error(f"A frase em português ultrapassa o limite de {phrase_pt_limit} caracteres. Você usou {len(phrase_pt)} caracteres.")

    # Seleção da IA
    selected_ai = st.selectbox(
        "Escolha a IA para obter feedback:",
        ["OpenAI", "MaritacaAI"]
    )

    # Botão para enviar a solicitação
    if st.button("Obter Feedback"):
        if len(situation) > situation_limit:
            st.error("Por favor, reduza a descrição da situação para no máximo 250 caracteres antes de prosseguir.")
        elif len(phrase_pt) > phrase_pt_limit:
            st.error("Por favor, reduza a frase em português para no máximo 100 caracteres antes de prosseguir.")
        elif len(phrase_en) > phrase_en_limit:
            st.error("Por favor, reduza a frase em inglês para no máximo 100 caracteres antes de prosseguir.")
        else:
            try:
                # Inicializa o serviço com o adaptador selecionado
                service = RoleplayFeedbackService(selected_ai)

                # Obtém o feedback
                feedback = service.get_feedback(situation, phrase_en, phrase_pt)

                # Exibe o feedback
                if feedback:
                    st.success("Feedback recebido:")
                    st.write(feedback)
                else:
                    st.error("Nenhuma resposta foi recebida da IA.")
            except Exception as e:
                logging.error(f"Erro ao obter feedback da IA: {e}")
                st.error("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.")

elif page == "Roleplay ideas":
    st.title("Roleplay ideas generator")
    # Entrada para descrição da situação

        # Sugestões de limites de caracteres para cada entrada
    situation_idea = 270  # Aproximadamente 62 tokens
    phrase_pt_limit = 100  # Aproximadamente 25 tokens
    phrase_en_limit = 100  # Aproximadamente 25 tokens

    situation = st.text_area(
        f"Descreva a situação do roleplay (máximo {situation_idea} caracteres):",
        help=f"Ex: Estou em um restaurante tentando pedir uma refeição. (Máximo de {situation_idea} caracteres)"
    )

    # Seleção da IA
    selected_ai = st.selectbox(
        "Escolha a IA para obter feedback:",
        ["OpenAI", "MaritacaAI"]
    )

    # Botão para enviar a solicitação
    if st.button("Obter Feedback"):
        if len(situation) > situation_idea:
            st.error("Por favor, reduza a descrição da situação para no máximo 250 caracteres antes de prosseguir.")
        else:
            try:
                # Inicializa o serviço com o adaptador selecionado
                service = RoleplayFeedbackService(selected_ai)

                # Obtém o feedback
                feedback = service.get_idea(situation)

                # Exibe o feedback
                if feedback:
                    st.success("Feedback recebido:")
                    st.write(feedback)
                else:
                    st.error("Nenhuma resposta foi recebida da IA.")
            except Exception as e:
                logging.error(f"Erro ao obter feedback da IA: {e}")
                st.error("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.")
