"""
Módulo de configuração do FacompBot
Gerencia variáveis de ambiente e configurações da API
"""
import os
from dotenv import load_dotenv


def setup_environment():
    """
    Configura as variáveis de ambiente e valida a API key

    Raises:
        ValueError: Se GOOGLE_API_KEY não estiver configurada
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("❌ Configure GOOGLE_API_KEY no arquivo .env")

    os.environ["GOOGLE_API_KEY"] = api_key
    return api_key


# Configurações do modelo
DEFAULT_MODEL = "gemini-2.5-flash"
DATA_DIRECTORY = "data"
