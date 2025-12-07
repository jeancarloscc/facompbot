"""
Classe base para criar agentes usando Google ADK
"""
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini


class FacompBotAgent:
    """
    Agente usando Google ADK Agent
    """

    def __init__(self, name: str, model: str, instruction: str, tools=None, output_key=None):
        """
        Inicializa um agente

        Args:
            name: Nome do agente
            model: Nome do modelo Gemini (ex: "gemini-2.5-flash-lite")
            instruction: Instruções do sistema para o agente
            tools: Lista de tools (opcional)
            output_key: Chave para armazenar resultado no estado da sessão (opcional)
        """
        self.name = name
        self.model_name = model
        self.instruction = instruction.strip()
        self.tools = tools if tools is not None else []
        self.output_key = output_key

        # Criar o agente ADK
        self.agent = Agent(
            name=self.name,
            model=Gemini(model=self.model_name),
            instruction=self.instruction,
            tools=self.tools,
            output_key=self.output_key
        )
