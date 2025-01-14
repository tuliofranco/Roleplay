import streamlit as st
from data.gasType import gas_list
from data.controleCilindros import data_controle_cilindros
from adapters.openai_adapter import OpenAIAdapter
from adapters.matraca_adapter import MatracaAdapter
from services.inventory_recommendation_service import InventoryRecommendationService
import logging

# Configurando o sistema de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Título do aplicativo
st.title("Recomendações de Estoque de Cilindros")

# Função para obter tamanhos disponíveis para o tipo de gás selecionado
def get_available_sizes(gas_type_id):
    """
    Retorna os tamanhos disponíveis para o tipo de gás selecionado.

    Args:
        gas_type_id (int): ID do tipo de gás.

    Returns:
        list: Lista de tamanhos disponíveis, ordenada.
    """
    sizes = {cylinder['size'] for cylinder in data_controle_cilindros if cylinder['gasTypeId'] == gas_type_id}
    return sorted(sizes)

# Mapeia os nomes e IDs dos gases
gas_names = {gas['gasName']: gas['id'] for gas in gas_list}

# Input do tipo de gás
selected_gas_name = st.selectbox(
    "Escolha o tipo de gás:",
    list(gas_names.keys())
)

# Obtém o ID do gás selecionado
selected_gas_id = gas_names[selected_gas_name]

# Obtém os tamanhos disponíveis para o gás selecionado
available_sizes = get_available_sizes(selected_gas_id)

# Input do tamanho do cilindro
cylinder_size = st.selectbox(
    "Escolha o tamanho do cilindro:",
    available_sizes
)

# Input para escolher a IA
selected_ai = st.selectbox(
    "Escolha a IA para obter recomendações:",
    ["OpenAI", "MatracaAI"]
)
ia = 0
# Botão para chamada à API
if st.button("Obter recomendação"):
    try:
        # Seleciona o adaptador de IA com base na escolha do usuário
        if selected_ai == "OpenAI":
            ai_adapter = OpenAIAdapter
        elif selected_ai == "MatracaAI":
            ai_adapter = MatracaAdapter
        else:
            st.error("IA selecionada inválida.")
            raise ValueError("IA selecionada inválida.")
        
        # Gera o prompt com base nas seleções
        selected_informations = [selected_gas_name, cylinder_size]

        # Serviço de recomendação com o adaptador escolhido
        service = InventoryRecommendationService(ai_adapter)
        response = service.get_stock_recommendation(selected_informations)
        
        # Exibe o retorno da IA
        if response:
            st.success(response)
        else:
            st.error("Nenhuma resposta foi recebida da IA.")
    except Exception as e:
        logging.error(f"Erro ao obter recomendação: {e}")
        st.error("Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente.")
