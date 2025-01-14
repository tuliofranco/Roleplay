import logging
from typing import Optional
import requests
import maritalk

# Configurando o sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MatracaAdapter:
    def __init__(self, api_key: Optional[str] = "105855156863753623897_69913f9219ab786e", model_name: str = "sabia-3"):
        """
        Inicializa o adaptador Matraca para integração com o modelo MariTalk.

        Args:
            api_key (Optional[str]): Chave da API para autenticação no MariTalk.
            model_name (str): Nome do modelo a ser utilizado.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model = maritalk.MariTalk(key=self.api_key, model=self.model_name)

    def generate_response(self, prompt: str, max_tokens: int = 8000) -> str:
        """
        Gera uma resposta do modelo MariTalk com base no prompt fornecido.

        Args:
            prompt (str): O texto de entrada para o modelo.
            max_tokens (int): Número máximo de tokens na resposta.

        Returns:
            str: Resposta gerada pelo modelo ou mensagem de erro em caso de falha.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("O prompt deve ser uma string não vazia.")

        try:
            response = self.model.generate(prompt, max_tokens=max_tokens)
            answer = response.get("answer", "Resposta não disponível.")
            logging.info("Resposta gerada com sucesso.")
            return answer

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
            return f"Erro na requisição: {http_err}"

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Erro na requisição: {req_err}")
            return f"Erro na requisição: {req_err}"

        except Exception as err:
            logging.error(f"Erro inesperado: {err}")
            return f"Erro inesperado: {err}"
