"""
FacompBot - Sistema Multi-Agente usando Google ADK

Sistema com agentes especializados para responder perguntas sobre FACOMP/UFPA:
- FAQAgent: Perguntas frequentes e respostas diretas
- ConteudoAgent: Explicações detalhadas sobre regulamentos
- EstagioAgent: Especialista em estágio obrigatório
- ACCAgent: Especialista em Atividades Complementares

Uso: python main.py
"""
import os
import asyncio
import uuid
from dotenv import load_dotenv
from google.genai import types
from google.adk.sessions import InMemorySessionService
from facompbot.document_tools import load_documents
from facompbot.prompts import SYSTEM_INSTRUCTION
from facompbot.agent import FacompBotAgent
from google.adk.runners import Runner
from google.adk.apps.app import App, ResumabilityConfig

# Configurar ambiente
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ Configure GOOGLE_API_KEY no arquivo .env")
os.environ["GOOGLE_API_KEY"] = api_key

# Carregar documentos
print("📚 Carregando documentos...")
uploaded_files = load_documents("data")
print(f"✅ {len(uploaded_files)} arquivo(s) carregado(s)\n")

# ===== CRIAR AGENTES ESPECIALIZADOS =====

model = "gemini-2.5-flash"

faq_agent = FacompBotAgent(
    name="FAQAgent",
    model=model,
    instruction="Você é especialista em responder perguntas frequentes sobre FACOMP/UFPA. Seja objetivo e direto.",
    output_key="faq_response"
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

print("✅ Agentes criados:")
print(f"  • {faq_agent.name} - Perguntas frequentes")
print(f"  • {conteudo_agent.name} - Conteúdo detalhado")
print(f"  • {estagio_agent.name} - Estágio obrigatório")
print(f"  • {acc_agent.name} - Atividades Complementares")
print(f"  • {router_agent.name} - Roteamento inteligente")

# Criar app e runner
facompbot_app = App(
    name="agents",
    root_agent=router_agent.agent
)

session_service = InMemorySessionService()

facompbot_runner = Runner(
    app=facompbot_app,
    session_service=session_service
)

print("\n💬 FacompBot Multi-Agente iniciado! Digite 'sair' para encerrar.\n")


def check_for_approval(events):
    """Check if events contain an approval request.

    Returns:
        dict with approval details or None
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
    """Create approval response message."""
    confirmation_response = types.FunctionResponse(
        id=approval_info["approval_id"],
        name="adk_request_confirmation",
        response={"confirmed": approved},
    )
    return types.Content(
        role="user", parts=[types.Part(function_response=confirmation_response)]
    )


print("✅ Helper functions defined")
# ===== LOOP INTERATIVO =====


async def main():
    """Função principal async para executar o loop interativo"""
    session_id = uuid.uuid4().hex[:8]

    await session_service.create_session(app_name="facompbot", user_id="test_user", session_id=session_id)

    while True:
        try:
            pergunta = input("❓ Pergunta: ").strip()

            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo!")
                break

            if not pergunta:
                continue

            print("🤖 Processando...")
            query_content = types.Content(
                role="user", parts=[types.Part(text=pergunta)])
            events = []

            # Executar com runner (async)
            async for event in facompbot_runner.run_async(
                user_id="test_user", session_id=session_id, new_message=query_content
            ):
                events.append(event)
                # Exibir resposta em tempo real
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text = part.text

            approval_info = check_for_approval(events)
            if approval_info:
                print("🔔 Aprovação necessária para continuar.")
                print(
                    f"Decisão Humana: {'APROVADO ✅' if True else 'REJEITADO ❌'}")

                async for event in facompbot_runner.run_async(
                    user_id="test_user",
                    session_id=session_id,
                    new_message=create_approval_response(
                        approval_info=approval_info, approved=True),
                    invocation_id=approval_info["invocation_id"],
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                print(f"✅ Resposta:\n{part.text}\n")
            else:
                # Exibir resposta já processada
                if response_text:
                    # Remover prefixo do agente se existir
                    if ":" in response_text and response_text.split(":")[0].endswith("Agent"):
                        response_text = response_text.split(":", 1)[1].strip()
                    print(f"\n✅ Resposta:\n{response_text}\n")
                else:
                    print("\n⚠️ Nenhuma resposta recebida.\n")
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")

# Executar loop async
if __name__ == "__main__":
    asyncio.run(main())
