from abc import ABC, abstractmethod


class LLMAdapter(ABC):
    """
    Classe abstrata que define a interface para adaptadores de modelos de linguagem.
    """

    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 8000) -> str:
        """
        Gera uma resposta baseada no prompt fornecido.

        Args:
            prompt (str): O texto de entrada.
            max_tokens (int): Número máximo de tokens na resposta.

        Returns:
            str: Resposta gerada.
        """
        pass