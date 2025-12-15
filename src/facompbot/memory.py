"""
MemoryBank - Sistema de memória de longo prazo para agentes
Armazena e recupera informações persistentes em formato JSON
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class MemoryBank:
    """
    Gerenciador de memória de longo prazo com persistência em JSON

    Permite armazenar contexto, histórico de interações e dados
    que devem persistir entre sessões do agente.
    """

    def __init__(self, storage_path: str = "data/memory_bank.json"):
        """
        Inicializa o MemoryBank

        Args:
            storage_path: Caminho do arquivo JSON para persistência
        """
        self.storage_path = Path(storage_path)
        self.memory: Dict[str, Any] = {}

        # Criar diretório se não existir
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Carregar memória existente
        self._load()

    def _load(self):
        """Carrega memória do arquivo JSON"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                print(f"✅ MemoryBank carregado: {len(self.memory)} entradas")
            except Exception as e:
                print(f"⚠️ Erro ao carregar MemoryBank: {e}")
                self.memory = {}
        else:
            print("📝 MemoryBank inicializado (vazio)")
            self.memory = {}

    def _save(self):
        """Salva memória no arquivo JSON"""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Erro ao salvar MemoryBank: {e}")

    def store(self, key: str, value: Any, metadata: Optional[Dict] = None):
        """
        Armazena um valor na memória

        Args:
            key: Chave única para identificar o valor
            value: Valor a ser armazenado (deve ser serializável em JSON)
            metadata: Metadados opcionais (ex: timestamp, categoria, tags)
        """
        entry = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        self.memory[key] = entry
        self._save()
        print(f"💾 Armazenado em MemoryBank: '{key}'")

    def retrieve(self, key: str) -> Optional[Any]:
        """
        Recupera um valor da memória pela chave

        Args:
            key: Chave do valor a recuperar

        Returns:
            Valor armazenado ou None se não existir
        """
        entry = self.memory.get(key)
        if entry:
            return entry.get("value")
        return None

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Busca entradas que contenham a query no key ou value

        Args:
            query: Termo de busca
            limit: Número máximo de resultados

        Returns:
            Lista de dicionários com {key, value, timestamp, metadata}
        """
        results = []
        query_lower = query.lower()

        for key, entry in self.memory.items():
            # Buscar em key
            if query_lower in key.lower():
                results.append({
                    "key": key,
                    "value": entry.get("value"),
                    "timestamp": entry.get("timestamp"),
                    "metadata": entry.get("metadata", {})
                })
                continue

            # Buscar em value (se for string)
            value = entry.get("value")
            if isinstance(value, str) and query_lower in value.lower():
                results.append({
                    "key": key,
                    "value": value,
                    "timestamp": entry.get("timestamp"),
                    "metadata": entry.get("metadata", {})
                })

        return results[:limit]

    def delete(self, key: str) -> bool:
        """
        Remove uma entrada da memória

        Args:
            key: Chave a remover

        Returns:
            True se removido, False se não existia
        """
        if key in self.memory:
            del self.memory[key]
            self._save()
            print(f"🗑️ Removido do MemoryBank: '{key}'")
            return True
        return False

    def clear(self):
        """Limpa toda a memória"""
        self.memory = {}
        self._save()
        print("🧹 MemoryBank limpo")

    def list_all(self) -> Dict[str, Any]:
        """
        Retorna todas as entradas

        Returns:
            Dicionário completo da memória
        """
        return self.memory.copy()

    def stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas da memória

        Returns:
            Dicionário com estatísticas (total, tamanho, etc)
        """
        return {
            "total_entries": len(self.memory),
            "storage_path": str(self.storage_path),
            "file_size_bytes": self.storage_path.stat().st_size if self.storage_path.exists() else 0
        }
