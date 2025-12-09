"""
FacompBot - Sistema Multi-Agente para FACOMP/UFPA
"""

__version__ = "0.1.0"

# Exportar componentes principais
from facompbot.agent import FacompBotAgent
from facompbot.config import setup_environment, DEFAULT_MODEL, DATA_DIRECTORY
from facompbot.agents_factory import create_agents, print_agents_summary
from facompbot.runner import create_runner
from facompbot.events import check_for_approval, create_approval_response
from facompbot.document_tools import load_documents, upload_pdf_to_gemini, create_document_context

__all__ = [
    "FacompBotAgent",
    "setup_environment",
    "DEFAULT_MODEL",
    "DATA_DIRECTORY",
    "create_agents",
    "print_agents_summary",
    "create_runner",
    "check_for_approval",
    "create_approval_response",
    "load_documents",
    "upload_pdf_to_gemini",
    "create_document_context",
]
