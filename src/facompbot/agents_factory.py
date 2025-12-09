"""
Factory para criação dos agentes especializados do FacompBot
"""
from facompbot.agent import FacompBotAgent
from facompbot.prompts import SYSTEM_INSTRUCTION
from google.adk.tools import google_search
from facompbot.document_tools import search_from_link

# link_tool = [{
#     "name": "search_from_link",
#     "description": "Use esta ferramenta para buscar informações específicas de um link fornecido pelo usuário.",
#     "function": search_from_link
# }]


def create_agents(model: str):
    """
    Cria todos os agentes especializados do sistema

    Args:
        model: Nome do modelo Gemini a ser utilizado

    Returns:
        dict com todos os agentes criados (faq, conteudo, estagio, acc, router)
    """

    faq_agent = FacompBotAgent(
        name="FAQAgent",
        model=model,
        instruction="Você é especialista em responder perguntas frequentes sobre Faculdade de Computação (FACOMP) da Universidade Federal do Pará (UFPA). Seja objetivo e direto.",
        output_key="faq_response",
        tools=[search_from_link]
    )

    conteudo_agent = FacompBotAgent(
        name="ConteudoAgent",
        model=model,
        instruction=f"{SYSTEM_INSTRUCTION}\n\nForneça explicações detalhadas sobre regulamentos e procedimentos.",
        output_key="conteudo_response"
    )

    estagio_agent = FacompBotAgent(
        name="EstagioAgent",
        model=model,
        instruction="Você é especialista em estágio obrigatório da FACOMP/UFPA. Responda sobre: carga horária, documentação, prazos, orientação.",
        output_key="estagio_response"
    )

    acc_agent = FacompBotAgent(
        name="ACCAgent",
        model=model,
        instruction="Você é especialista em Atividades Complementares (ACC) da FACOMP/UFPA. Responda sobre: horas necessárias, tipos de atividades, validação, documentação.",
        output_key="acc_response"
    )

    router_agent = FacompBotAgent(
        name="RouterAgent",
        model=model,
        instruction="""Você é um roteador inteligente que analisa perguntas e responde diretamente.
Baseado na pergunta, use o conhecimento apropriado:
- FAQAgent: Perguntas simples e diretas
- ConteudoAgent: Explicações detalhadas
- EstagioAgent: Dúvidas sobre estágio obrigatório
- ACCAgent: Dúvidas sobre Atividades Complementares

Responda em português de forma clara e objetiva.""",
        output_key="router_response"
    )

    return {
        "faq": faq_agent,
        "conteudo": conteudo_agent,
        "estagio": estagio_agent,
        "acc": acc_agent,
        "router": router_agent
    }


def print_agents_summary(agents):
    """
    Exibe resumo dos agentes criados

    Args:
        agents: Dicionário com os agentes
    """
    print("✅ Agentes criados:")
    print(f"  • {agents['faq'].name} - Perguntas frequentes")
    print(f"  • {agents['conteudo'].name} - Conteúdo detalhado")
    print(f"  • {agents['estagio'].name} - Estágio obrigatório")
    print(f"  • {agents['acc'].name} - Atividades Complementares")
    print(f"  • {agents['router'].name} - Roteamento inteligente")
