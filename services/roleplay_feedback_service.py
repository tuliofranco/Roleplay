from adapters.maritaca_adapter import MaritacaAdapter
from adapters.openai_adapter import OpenAIAdapter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RoleplayFeedbackService:
    def __init__(self, selected_ai):
        """
        Inicializa o serviço de feedback de roleplay.

        Args:
            selected_ai (str): Nome do adaptador de IA selecionado ("OpenAI" ou "MaritacaAI").
        """
        if selected_ai == "OpenAI":
            self.llm = OpenAIAdapter()
        elif selected_ai == "MaritacaAI":
            self.llm = MaritacaAdapter()
        else:
            raise ValueError("Adaptador de IA inválido. Escolha 'OpenAI' ou 'MaritacaAI'.")

    def get_feedback(self, situation: str,  phrase_en: str, phrase_pt: str) -> str:
        """
        Gera um feedback de roleplay com base na situação e nas frases fornecidas.

        Args:
            situation (str): Descrição da situação do roleplay.
            phrase_pt (str): Frase em português.
            phrase_en (str): Frase em inglês.

        Returns:
            str: Feedback detalhado da IA.
        """
        # Criação do prompt para a IA
        prompt = (
            f"Situação: {situation}\n"
            f"Frase em português: {phrase_pt}\n"
            f"Frase em inglês: {phrase_en}\n"
            "Forneça um feedback objetivo e organizado sobre a frase em inglês, seguindo o formato abaixo:"
            "\n- Feedback: Explique se a frase está correta e por quê."
            "\n- Correção: Indique possíveis ajustes gramaticais ou de estilo."
            "\n- Variação:"
            "\n      - Para um contexto mais formal...\n"
            "\n              - Exemplo 1:"
            "\n      - Para um contexto mais amigável...\n"
            "\n              - Exemplo 2:"
            " Limite a resposta a 500 caracteres."
        )

        try:
            # Envia o prompt para a IA e retorna a resposta
            response = self.llm.generate_response(prompt)
            return response
        except Exception as e:
            logging.error(f"Erro ao obter feedback da IA: {e}")
            return "Ocorreu um erro ao gerar o feedback. Por favor, tente novamente."
        
    def get_idea(self, situation: str) -> str:
        """
        Gera um ideias de roleplay com base na situação.

        Args:
            situation (str): Descrição da situação que pretende que seja gerada

        Returns:
            str: Ideias de situações.
        """
        prompt = (
            f"Assuma a seguinte contexto: {situation}\n"
            f"Forneça 3 situações objetivas e organizadas em ingles, seguindo o formato abaixo:"
            "- Context 1: "
            "   - situação 1: ..."
            "   - situação 2: ..."
            "   - situação 3: ..."
            "- Context 2: "
            "   - situação 1: ..."
            "   - situação 2: ..."
            "   - situação 3: ..."
        )
        
        try:
            # Envia o prompt para a IA e retorna a resposta
            response = self.llm.generate_response(prompt)
            return response
        
        except Exception as e:
            logging.error(f"Erro ao obter feedback da IA: {e}")
            return "Ocorreu um erro ao gerar o feedback. Por favor, tente novamente."
        
    def get_context(self, word: str, sentence: str) -> str:
        """
        Busca informações de contexto para uma palavra em uma frase fornecida.

        Args:
            word (str): Palavra a ser buscada.
            sentence (str): Frase onde a palavra aparece.

        Returns:
            str: Informações de contexto geradas pela IA.
        """
        prompt = (
            f"Palavra: {word}\n"
            f"Frase: {sentence}\n"
            "Explique o significado da palavra no contexto da frase. Forneça exemplos adicionais de uso em situações similares."
            "A resposta deve seguir o seguinte padrão:"
            "- Significado da palavra:"
            "- Significado da naquele contexto:"
            "- Exemplos adicionais: Forneça 5 exemplos"
        )

        try:
            # Envia o prompt para a IA e retorna a resposta
            response = self.llm.generate_response(prompt)
            return response
        except Exception as e:
            logging.error(f"Erro ao buscar o contexto: {e}")
            return "Ocorreu um erro ao buscar o contexto. Por favor, tente novamente."



