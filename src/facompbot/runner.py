"""
Módulo de configuração e inicialização do ADK Runner
"""
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.apps.app import App
from facompbot.memory import MemoryBank


def create_runner(router_agent, memory_path: str = "data/memory_bank.json"):
    """
    Cria e configura o ADK Runner com App, SessionService e MemoryBank

    Args:
        router_agent: Agente raiz (RouterAgent) do sistema
        memory_path: Caminho para arquivo de persistência do MemoryBank

    Returns:
        tuple (runner, session_service, memory_bank) configurados
    """
    # Criar app
    facompbot_app = App(
        name="agents",
        root_agent=router_agent.agent
    )

    # Criar session service
    session_service = InMemorySessionService()

    # Criar memory bank
    memory_bank = MemoryBank(storage_path=memory_path)

    # Criar runner
    facompbot_runner = Runner(
        app=facompbot_app,
        session_service=session_service
    )

    return facompbot_runner, session_service, memory_bank
