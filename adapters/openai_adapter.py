import logging
import openai
from openai import OpenAIError
import os
from adapters.llm_adapter import LLMAdapter
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Desativa possíveis problemas relacionados ao PyTorch
os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"] = "1"

load_dotenv()

class OpenAIAdapter(LLMAdapter):
    def __init__(self, model_name: str = "gpt-4"):
        """
        Inicializa o adaptador para integração com a API da OpenAI.

        Args:
            model_name (str): Nome do modelo a ser utilizado (ex.: "gpt-4").
        """
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("A chave da API OpenAI não foi configurada nas variáveis de ambiente.")
        self.model_name = model_name
        openai.api_key = self.api_key


    def generate_response(self, prompt: str, max_tokens: int = 8000) -> str:
        """
        Gera uma resposta do modelo ChatGPT com base no prompt fornecido.

        Args:
            prompt (str): O texto de entrada para o modelo.
            max_tokens (int): Número máximo de tokens na resposta.

        Returns:
            str: Resposta gerada pelo modelo ou mensagem de erro em caso de falha.
        """
        if not prompt or not isinstance(prompt, str):
            raise ValueError("O prompt deve ser uma string não vazia.")

        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            answer = response.choices[0].message['content']
            logging.info("Resposta gerada com sucesso.")
            return answer

        except OpenAIError as openai_err:
            logging.error(f"Erro na API da OpenAI: {openai_err}")
            return f"Erro na API da OpenAI: {openai_err}"

        # except Exception as err:
        #     logging.error(f"Erro inesperado: {err}")
        #     return f"Erro inesperado: {err}"