"""
FacompBot - Sistema Multi-Agente usando Google ADK

Sistema com agentes especializados para responder perguntas sobre FACOMP/UFPA:
- FAQAgent: Perguntas frequentes e respostas diretas
- ConteudoAgent: Explicações detalhadas sobre regulamentos
- EstagioAgent: Especialista em estágio obrigatório
- ACCAgent: Especialista em Atividades Complementares

Uso: python main.py
"""
import asyncio
import uuid
import time
from google.genai import types

# Imports dos módulos do projeto
from facompbot.config import setup_environment, DEFAULT_MODEL, DATA_DIRECTORY
from facompbot.document_tools import load_documents
from facompbot.agents_factory import create_agents, print_agents_summary
from facompbot.runner import create_runner
from facompbot.events import check_for_approval, create_approval_response

# Configurar ambiente
setup_environment()

# Carregar documentos
print("📚 Carregando documentos...")
uploaded_files = load_documents(DATA_DIRECTORY)
print(f"✅ {len(uploaded_files)} arquivo(s) carregado(s)\n")

# Criar agentes especializados
agents = create_agents(DEFAULT_MODEL)
print_agents_summary(agents)

# Criar runner, session service e memory bank
facompbot_runner, session_service, memory_bank = create_runner(
    agents["router"])

print("\n💬 FacompBot Multi-Agente iniciado! Digite 'sair' para encerrar.\n")

# ===== LOOP INTERATIVO =====


async def main():
    """Função principal async para executar o loop interativo"""
    session_id = uuid.uuid4().hex[:8]

    await session_service.create_session(app_name="agents", user_id="test_user", session_id=session_id)

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

            # Sistema de retry para erros 503 (modelo sobrecarregado)
            max_retries = 3
            retry_delay = 2  # segundos

            for attempt in range(max_retries):
                try:
                    events = []
                    response_texts = []  # Lista para acumular todas as respostas

                    # Executar com runner (async)
                    async for event in facompbot_runner.run_async(
                        user_id="test_user", session_id=session_id, new_message=query_content
                    ):
                        events.append(event)
                        # Coletar respostas de texto
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    response_texts.append(part.text)

                    # Se chegou aqui, sucesso - sair do loop de retry
                    break

                except Exception as retry_error:
                    error_msg = str(retry_error)
                    # Verificar se é erro 503 (overload)
                    if "503" in error_msg or "overloaded" in error_msg.lower():
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (attempt + 1)
                            print(
                                f"⚠️ Modelo sobrecarregado. Tentando novamente em {wait_time}s... (tentativa {attempt + 2}/{max_retries})")
                            time.sleep(wait_time)
                        else:
                            print(
                                f"\n❌ Erro após {max_retries} tentativas: Modelo Gemini está sobrecarregado.")
                            print(
                                "💡 Dica: Aguarde alguns minutos e tente novamente.\n")
                            continue  # Volta para o início do loop principal
                    else:
                        # Outro tipo de erro - propagar
                        raise retry_error

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
                            if hasattr(part, 'text') and part.text:
                                print(f"✅ Resposta:\n{part.text}\n")
            else:
                # Exibir todas as respostas coletadas
                if response_texts:
                    print("\n✅ Resposta:")
                    for response_text in response_texts:
                        # Remover prefixo do agente se existir
                        if ":" in response_text and response_text.split(":")[0].endswith("Agent"):
                            response_text = response_text.split(":", 1)[
                                1].strip()
                        print(f"{response_text}")
                    print()  # Linha em branco no final
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
