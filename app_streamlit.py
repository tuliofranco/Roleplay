import streamlit as st
from services.roleplay_feedback_service import RoleplayFeedbackService
from services.word_list_service import WordListService
import pandas as pd
import logging

# Configurando o sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Navegação
page = st.sidebar.radio("Navegação", ["Home", "Roleplay ideas", "Context dictionary", "Words list", "Words input"])

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
        ["MaritacaAI", "OpenAI" ]
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
    situation_idea = 270  # Aproximadamente 62 tokens

    situation = st.text_area(
        f"Descreva a situação do roleplay (máximo {situation_idea} caracteres):",
        help=f"Ex: Estou em um restaurante tentando pedir uma refeição. (Máximo de {situation_idea} caracteres)"
    )

    # Seleção da IA
    selected_ai = st.selectbox(
        "Escolha a IA para obter feedback:",
        ["MaritacaAI","OpenAI"]
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

elif page == "Context dictionary":
    st.title("Context Dictionary")

    # Campo para inserir a palavra
    word = st.text_input("Digite a palavra que deseja procurar:", help="Ex: success")

    # Campo para inserir a frase que contém a palavra
    sentence = st.text_area(
        "Digite a frase completa onde a palavra aparece:", 
        help="Ex: Hard work is the key to success."
    )
    
    # Seleção da IA
    selected_ai = st.selectbox(
        "Escolha a IA para obter feedback:",
        ["MaritacaAI","OpenAI"]
    )

    # Botão para processar a solicitação
    if st.button("Procurar no Dicionário"):
        if not word:
            st.error("Por favor, insira uma palavra antes de prosseguir.")
        elif not sentence:
            st.error("Por favor, insira uma frase contendo a palavra antes de prosseguir.")
        else:
            try:
                # Inicializa o serviço com a palavra e a frase
                service = RoleplayFeedbackService(selected_ai)
                context_info = service.get_context(word, sentence)

                # Exibe o contexto
                if context_info:
                    st.success("Contexto encontrado:")
                    st.write(context_info)
                else:
                    st.error("Nenhum contexto foi encontrado para a palavra informada.")
            except Exception as e:
                logging.error(f"Erro ao buscar o contexto: {e}")
                st.error("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.")



elif page == "Words list":
    st.title("Words List - Gerador de Palavras")

    # Campo para receber o número de palavras a serem adicionadas
    num_words = st.number_input("Quantas palavras você gostaria de adicionar hoje?", min_value=1, max_value=100, step=1, value=20)
    word_list_service = WordListService()
    # Botão para gerar as palavras
    if st.button("Gerar palavras"):
        
        result = word_list_service.add_words_for_today(int(num_words))
        result = word_list_service.add_words_for_today(int(num_words))

        st.success(result)

    # Exibir tabela de palavras já aprendidas
    st.subheader("Palavras")
    learning_words = word_list_service.get_learning_words()

    if isinstance(learning_words, list):
        df_learning = pd.DataFrame(learning_words, columns=["ID", "Word", "Translation", "Part_of_Speech", "Frequency", "Coor_qty", "Err_Qty", "Day"])
        st.dataframe(df_learning)
    else:
        st.error(learning_words)


elif page == "Words input":
    st.title("Words Input - Input a Word")

    # Inicializar o serviço
    word_list_service = WordListService()

    # Selecionar palavras do dia atual
    learning_words = word_list_service.get_learning_words()
    if isinstance(learning_words, list) and learning_words:
        word_options = [word[1] for word in learning_words]  # Lista de palavras do dia atual
        selected_word = st.selectbox("Escolha uma palavra gerada:", options=word_options)

        # Caixa de texto para criar uma frase
        sentence = st.text_area(f"Crie uma frase com a palavra '{selected_word}':")

        # Caixa de seleção para escolher o tempo verbal
        tense = st.selectbox(
            "Escolha o tempo verbal da frase:",
            options=["Simple Present", "Simple Past", "Simple Future", "Present Perfect", "Present Continuous"]
        )
        selected_ai = st.selectbox(
            "Escolha a IA para obter feedback:",
            ["MaritacaAI", "OpenAI"]
        )

        # Botão para verificar a frase
        if st.button("Verify"):
            if not sentence.strip():
                st.error("Por favor, escreva uma frase antes de verificar.")
            else:
                # Chamar o serviço para verificar a frase
                feedback = word_list_service.verify_phrase(selected_word, sentence, tense, selected_ai)

                # Exibir o feedback
                if feedback:
                    st.success("Feedback recebido:")
                    st.write(feedback)

                    # Capturar o estado do feedback com st.selectbox
                    feedback_state = st.selectbox(
                        "Como você classifica o feedback?",
                        options=["Selecione...", "Correct", "Wrong"]
                    )

                    # Valida a seleção antes de enviar
                    if feedback_state == "Selecione...":
                        st.warning("Por favor, selecione uma classificação para o feedback.")
                    elif st.button("Enviar Feedback"):
                        # Processa o feedback
                        if feedback_state == "Correct":
                            word_list_service.update_learning_word_feedback(selected_word, "Correct")
                            st.success(f"Você marcou o feedback como correto. A palavra '{selected_word}' foi atualizada.")
                        elif feedback_state == "Wrong":
                            word_list_service.update_learning_word_feedback(selected_word, "Wrong")
                            st.error(f"Você marcou o feedback como incorreto. A palavra '{selected_word}' foi atualizada.")
    else:
        st.warning("Nenhuma palavra disponível para o dia atual. Por favor, gere palavras na aba Words List.")