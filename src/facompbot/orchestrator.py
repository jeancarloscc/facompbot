"""
Orquestrador de Agentes - Execução paralela, sequencial e em loop
Implementa padrões de coordenação entre múltiplos agentes
"""
import asyncio
from typing import List, Dict, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
from google.adk.runners import Runner


class AgentOrchestrator:
    """
    Orquestrador para coordenar execução de múltiplos agentes

    Suporta três padrões principais:
    - Paralelo: Executa múltiplos agentes simultaneamente
    - Sequencial: Encadeia agentes onde output de um alimenta o próximo
    - Loop: Executa agentes iterativamente até condição de parada
    """

    def __init__(self, runner: Runner, session_service, memory_bank=None):
        """
        Inicializa o orquestrador

        Args:
            runner: Runner do ADK configurado
            session_service: Serviço de sessão do ADK
            memory_bank: MemoryBank opcional para persistência
        """
        self.runner = runner
        self.session_service = session_service
        self.memory_bank = memory_bank

    async def run_parallel(
        self,
        agents: List[Any],
        prompt: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa múltiplos agentes em paralelo e agrega resultados

        Args:
            agents: Lista de agentes FacompBotAgent
            prompt: Prompt a ser enviado para todos os agentes
            session_id: ID da sessão (opcional)

        Returns:
            Dicionário com respostas de cada agente
        """
        print(f"🔄 Executando {len(agents)} agentes em paralelo...")

        # Criar tasks assíncronas para cada agente
        tasks = []
        for agent in agents:
            task = self._run_agent_async(agent, prompt, session_id)
            tasks.append(task)

        # Executar todos em paralelo
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Agregar resultados
        aggregated = {}
        for agent, result in zip(agents, results):
            if isinstance(result, Exception):
                aggregated[agent.name] = {"error": str(result)}
            else:
                aggregated[agent.name] = result

        # Salvar em memória se disponível
        if self.memory_bank:
            self.memory_bank.store(
                f"parallel_execution_{session_id or 'default'}",
                aggregated,
                metadata={"type": "parallel", "prompt": prompt}
            )

        print(f"✅ Execução paralela concluída: {len(aggregated)} respostas")
        return aggregated

    async def _run_agent_async(self, agent, prompt: str, session_id: Optional[str]):
        """
        Executa um agente de forma assíncrona

        Args:
            agent: FacompBotAgent
            prompt: Prompt a enviar
            session_id: ID da sessão

        Returns:
            Resposta do agente
        """
        loop = asyncio.get_event_loop()

        # Executar em thread pool para não bloquear
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor,
                self._execute_agent,
                agent,
                prompt,
                session_id
            )

        return result

    def _execute_agent(self, agent, prompt: str, session_id: Optional[str]) -> str:
        """
        Executa um agente de forma síncrona (helper interno)

        Args:
            agent: FacompBotAgent
            prompt: Prompt a enviar
            session_id: ID da sessão

        Returns:
            Texto da resposta do agente
        """
        try:
            # Criar/obter sessão
            if not session_id:
                session_id = self.session_service.create_session()

            # Executar agente via runner modificando temporariamente o root_agent
            # (alternativa: usar agent.agent.send() diretamente se disponível)
            original_root = self.runner.app.root_agent
            self.runner.app.root_agent = agent.agent

            events = self.runner.run(
                session_id=session_id,
                new_message=prompt
            )

            # Restaurar root original
            self.runner.app.root_agent = original_root

            # Extrair resposta
            response_text = self._extract_response(events)
            return response_text

        except Exception as e:
            return f"Erro ao executar {agent.name}: {str(e)}"

    def _extract_response(self, events) -> str:
        """
        Extrai texto da resposta dos eventos do runner

        Args:
            events: Lista de eventos do ADK

        Returns:
            Texto da resposta
        """
        for event in events:
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            return part.text
        return "[Sem resposta]"

    def run_sequential(
        self,
        agents: List[Any],
        initial_prompt: str,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executa agentes sequencialmente (pipeline)
        Output de cada agente alimenta o próximo

        Args:
            agents: Lista ordenada de agentes
            initial_prompt: Prompt inicial para o primeiro agente
            session_id: ID da sessão

        Returns:
            Lista de resultados de cada etapa
        """
        print(
            f"⚙️ Executando pipeline sequencial com {len(agents)} agentes...")

        if not session_id:
            session_id = self.session_service.create_session()

        results = []
        current_prompt = initial_prompt

        for i, agent in enumerate(agents, 1):
            print(f"  [{i}/{len(agents)}] Executando {agent.name}...")

            response = self._execute_agent(agent, current_prompt, session_id)

            result = {
                "agent": agent.name,
                "input": current_prompt,
                "output": response
            }
            results.append(result)

            # Output vira input do próximo
            current_prompt = response

        # Salvar pipeline em memória
        if self.memory_bank:
            self.memory_bank.store(
                f"sequential_execution_{session_id}",
                results,
                metadata={"type": "sequential",
                          "initial_prompt": initial_prompt}
            )

        print(f"✅ Pipeline concluído: {len(results)} etapas")
        return results

    def run_loop(
        self,
        agent: Any,
        initial_prompt: str,
        condition: Callable[[str], bool],
        max_iterations: int = 10,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Executa um agente em loop até condição de parada

        Args:
            agent: Agente a executar
            initial_prompt: Prompt inicial
            condition: Função que recebe resposta e retorna True para parar
            max_iterations: Número máximo de iterações
            session_id: ID da sessão

        Returns:
            Lista de iterações com prompts e respostas
        """
        print(
            f"🔁 Executando {agent.name} em loop (max {max_iterations} iterações)...")

        if not session_id:
            session_id = self.session_service.create_session()

        iterations = []
        current_prompt = initial_prompt

        for i in range(max_iterations):
            print(f"  Iteração {i+1}/{max_iterations}...")

            response = self._execute_agent(agent, current_prompt, session_id)

            iteration = {
                "iteration": i + 1,
                "prompt": current_prompt,
                "response": response
            }
            iterations.append(iteration)

            # Verificar condição de parada
            if condition(response):
                print(f"✅ Condição de parada atingida na iteração {i+1}")
                break

            # Preparar próximo prompt (pode ser customizado)
            current_prompt = f"Refine a resposta anterior: {response}"

        # Salvar loop em memória
        if self.memory_bank:
            self.memory_bank.store(
                f"loop_execution_{session_id}",
                iterations,
                metadata={"type": "loop", "total_iterations": len(iterations)}
            )

        print(f"✅ Loop concluído: {len(iterations)} iterações")
        return iterations


# Funções helper para condições de parada comuns
def stop_on_keyword(keyword: str):
    """
    Retorna função de condição que para quando keyword aparece na resposta

    Args:
        keyword: Palavra-chave a procurar

    Returns:
        Função de condição
    """
    def condition(response: str) -> bool:
        return keyword.lower() in response.lower()
    return condition


def stop_on_length(min_length: int):
    """
    Retorna função de condição que para quando resposta atinge tamanho mínimo

    Args:
        min_length: Tamanho mínimo da resposta

    Returns:
        Função de condição
    """
    def condition(response: str) -> bool:
        return len(response) >= min_length
    return condition
