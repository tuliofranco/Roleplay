import os
import logging
import requests
import maritalk

from adapters.llm_adapter import LLMAdapter

# Configurando o sistema de logging (caso queira manter local)
# Você também pode configurar isso em outro lugar do seu sistema
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MaritacaAdapter(LLMAdapter):
    """
    Adaptador para o modelo MariTalk, possibilitando a geração de respostas
    a partir de prompts utilizando a biblioteca maritalk.
    """

    def __init__(self, model_name: str = "sabia-3"):
        """
        Inicializa o adaptador Matraca para integração com o modelo MariTalk.

        Args:
            model_name (str): Nome do modelo a ser utilizado.
        """
        self.api_key = os.getenv("MARITACA_API_KEY")
        if not self.api_key:
            logging.warning("Variável de ambiente 'MARITACA_API_KEY' não foi definida. "
                            "Certifique-se de que a API key esteja configurada.")
        
        self.model_name = model_name
        self.model = maritalk.MariTalk(key=self.api_key, model=self.model_name)
        logging.info(f"MatracaAdapter inicializado com o modelo '{self.model_name}'.")

    def generate_response(self, prompt: str, max_tokens: int = 8000) -> str:
        """
        Gera uma resposta do modelo MariTalk com base no prompt fornecido.

        Args:
            prompt (str): O texto de entrada para o modelo.
            max_tokens (int): Número máximo de tokens na resposta.

        Returns:
            str: Resposta gerada pelo modelo ou mensagem de erro em caso de falha.

        Raises:
            ValueError: Se o prompt não for uma string ou estiver vazio.
            ValueError: Se max_tokens for menor ou igual a zero.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("O prompt deve ser uma string não vazia.")

        if max_tokens <= 0:
            raise ValueError("max_tokens deve ser maior que zero.")

        try:
            logging.debug(f"Enviando prompt para MariTalk: {prompt[:50]}...")
            response = self.model.generate(prompt, max_tokens=max_tokens)

            # Extrai o campo 'answer' da resposta; fornece fallback se não existir
            answer = response.get("answer", "Resposta não disponível.")
            logging.info("Resposta gerada com sucesso.")
            return answer

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao gerar resposta: {http_err}")
            return f"Erro na requisição (HTTP): {http_err}"

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro na requisição ao gerar resposta: {req_err}")
            return f"Erro na requisição: {req_err}"

        except Exception as err:
            logging.error(f"Erro inesperado ao gerar resposta: {err}")
            return f"Erro inesperado: {err}"
