"""
Módulo de gerenciamento de eventos do ADK
Funções para processar aprovações e respostas
"""
from google.genai import types


def check_for_approval(events):
    """
    Verifica se os eventos contêm uma solicitação de aprovação

    Args:
        events: Lista de eventos do runner

    Returns:
        dict com detalhes da aprovação ou None
    """
    for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if (
                    part.function_call
                    and part.function_call.name == "adk_request_confirmation"
                ):
                    return {
                        "approval_id": part.function_call.id,
                        "invocation_id": event.invocation_id,
                    }
    return None


def create_approval_response(approval_info, approved):
    """
    Cria mensagem de resposta de aprovação

    Args:
        approval_info: Dicionário com approval_id e invocation_id
        approved: Boolean indicando se foi aprovado

    Returns:
        Content com a resposta de aprovação
    """
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )
