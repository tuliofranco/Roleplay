from data.enchimento import data_enchimento
from data.pedidos import data_pedidos
from data.controleCilindros import data_controle_cilindros
from adapters.matraca_adapter import MatracaAdapter
import pandas as pd
import logging

# Configurando o sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InventoryRecommendationService:
    def __init__(self, llm_adapter=None):
        """
        Inicializa o serviço de recomendação de estoque.

        Args:
            llm_adapter (callable, optional): Classe ou função para gerar respostas com LLM.
                                              Default é MatracaAdapter.
        """
        self.llm = llm_adapter() if llm_adapter else MatracaAdapter()

    def analysis(self):
        """
        Analisa os dados de pedidos, controle de cilindros e enchimentos para gerar insights adicionais.

        Returns:
            dict: Estatísticas calculadas a partir dos dados fornecidos.
        """
        # Análise de pedidos
        pedidos_df = pd.DataFrame(data_pedidos)
        daily_consumption = pedidos_df.groupby('data_pedido')['quantity'].sum()
        pedidos_summary = {
            "Consumo diário": daily_consumption.to_dict(),
            "Média diária": daily_consumption.mean(),
            "Desvio padrão": daily_consumption.std(),
            "Consumo total": daily_consumption.sum(),
        }
        logging.info("Análise de pedidos concluída.")

        # Análise de controle de cilindros
        controle_df = pd.DataFrame(data_controle_cilindros)
        controle_summary = controle_df.groupby(['gasTypeId', 'size', 'status_cilindro', 'status_gas']).size().reset_index(name='count')
        logging.info("Análise de controle de cilindros concluída.")

        # Análise de enchimentos
        enchimentos_df = pd.DataFrame(data_enchimento)
        enchimentos_df['data_inicio'] = pd.to_datetime(enchimentos_df['data_inicio'])
        enchimentos_df['data_final'] = pd.to_datetime(enchimentos_df['data_final'])
        enchimentos_df['duracao_dias'] = (enchimentos_df['data_final'] - enchimentos_df['data_inicio']).dt.days
        enchimentos_summary = enchimentos_df.groupby(['gasTypeId', 'size']).agg(
            duracao_media=('duracao_dias', 'mean'),
            duracao_total=('duracao_dias', 'sum'),
            num_enchimentos=('duracao_dias', 'count')
        ).reset_index()
        logging.info("Análise de enchimentos concluída.")

        return {
            'pedidos_summary': pedidos_summary,
            'controle_summary': controle_summary,
            'enchimentos_summary': enchimentos_summary
        }

    def get_stock_recommendation(self, selected_informations) -> str:
        """
        Gera uma recomendação de estoque com base nos dados analisados.

        Args:
            selected_informations (list): Informações selecionadas para gerar a recomendação.

        Returns:
            str: Recomendação de nível mínimo de estoque (safety stock).
        """
        # Obter dados analisados
        analysis_data = self.analysis()
        media_diaria = analysis_data['pedidos_summary']['Média diária']
        duracao_enchimento = analysis_data['enchimentos_summary'].loc[analysis_data['enchimentos_summary']['size'] == 5, 'duracao_media'].values[0]
        estoque_minimo = int(media_diaria * duracao_enchimento)

        # Construir o prompt
        prompt = (
            f"Com base nos dados analisados, a média diária de consumo de cilindros de {selected_informations[0]} de {selected_informations[1]} é {media_diaria:.2f}. "
            f"Considerando que o tempo médio de enchimento é de {duracao_enchimento:.2f} dias, "
            f"recomende a quantidade mínima de cilindros de estoque necessária para evitar faltas. "
            "Gostaria que analisasse os dados de pedido e com base no histórico, pudesse fazer alguma recomendação, por exemplo, identificar a sazonalidade de pedidos e recomendar um estoque minimo um pouco maior ou menor. "
            "Evite realizar calculos na resposta, mostre apenas os valores. "
            f"A resposta deve seguir o formato: "
            f"A média diária de cilindros de {selected_informations[0]} de {selected_informations[1]} metros cúbicos vendidos foi de {media_diaria:.2f}, "
            f"tendo em vista que é necessário {duracao_enchimento:.2f} dias para fazer o enchimento do mesmo, a quantidade de estoque mínima recomendada é {estoque_minimo}. Explicar a sazonalidade:"
            "- Periodos em que há menor sazonalidade:"
            "-Valores do estoque sem sazonalidade:"
            "- Periodos em que há maior sazonalidade:"
            "-Valores do estoque com sazonalidade:"
        )

        # Gerar resposta com a LLM
        try:
            recommendation_text = self.llm.generate_response(prompt)
            logging.info("Recomendação gerada com sucesso.")
            return recommendation_text
        except Exception as e:
            logging.error(f"Erro ao gerar recomendação: {e}")
            return f"Erro ao gerar recomendação: {str(e)}"

    @staticmethod
    def format_response(recommendation_text: str) -> str:
        """
        Formata a resposta gerada pela LLM para um padrão mais legível e estruturado.

        Args:
            recommendation_text (str): Texto cru retornado pela LLM.

        Returns:
            str: Texto formatado com as recomendações detalhadas.
        """
        return recommendation_text.strip()
