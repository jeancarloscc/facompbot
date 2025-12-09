"""
Módulo de configuração e inicialização do ADK Runner
"""
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.apps.app import App


def create_runner(router_agent):
    """
    Cria e configura o ADK Runner com App e SessionService

    Args:
        router_agent: Agente raiz (RouterAgent) do sistema

    Returns:
        tuple (runner, session_service) configurados
    """
    # Criar app
    facompbot_app = App(
        name="agents",
        root_agent=router_agent.agent
    )

    # Criar session service
    session_service = InMemorySessionService()

    # Criar runner
    facompbot_runner = Runner(
        app=facompbot_app,
        session_service=session_service
    )

    return facompbot_runner, session_service
