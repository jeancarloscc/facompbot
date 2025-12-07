"""
Ferramentas customizadas para busca em documentos PDF usando Google Gemini File API

Este módulo centraliza todas as operações relacionadas ao upload e gerenciamento
de documentos PDF para o Gemini API.
"""
import google.generativeai as genai
import os
from pathlib import Path
import time
from typing import List, Optional


def upload_pdf_to_gemini(file_path: str) -> Optional[object]:
    """
    Faz upload de um arquivo PDF para o Gemini File API e aguarda o processamento

    Args:
        file_path: Caminho completo do arquivo PDF

    Returns:
        Objeto File do Gemini se sucesso, None se falhar
    """
    try:
        print(f"📤 Fazendo upload de {os.path.basename(file_path)}...")
        file = genai.upload_file(file_path)

        # Aguardar processamento completo
        while file.state.name == "PROCESSING":
            print("⏳ Processando...")
            time.sleep(2)
            file = genai.get_file(file.name)

        if file.state.name == "FAILED":
            raise ValueError(f"Falha ao processar {file_path}")

        print(f"✅ Upload concluído: {file.display_name}")
        return file
    except Exception as e:
        print(f"❌ Erro ao fazer upload de {file_path}: {e}")
        return None


def load_documents(data_dir: str = "data") -> List[object]:
    """
    Carrega todos os PDFs de um diretório e faz upload para o Gemini

    Args:
        data_dir: Diretório contendo os arquivos PDF (padrão: "data")

    Returns:
        Lista de objetos File do Gemini processados com sucesso
    """
    # Buscar arquivos PDF
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"⚠️ Diretório {data_dir} não existe")
        return []

    pdf_files = list(data_path.glob("*.pdf"))

    if not pdf_files:
        print(f"⚠️ Nenhum PDF encontrado em {data_dir}")
        return []

    print(f"\n📚 Encontrados {len(pdf_files)} arquivo(s) PDF")

    # Fazer upload de cada arquivo
    uploaded_files = []
    for pdf_file in pdf_files:
        file = upload_pdf_to_gemini(str(pdf_file))
        if file:
            uploaded_files.append(file)

    print(f"✅ {len(uploaded_files)} arquivo(s) carregado(s) com sucesso\n")
    return uploaded_files


def create_document_context(uploaded_files: List[object]) -> str:
    """
    Cria uma descrição textual dos documentos carregados

    Args:
        uploaded_files: Lista de objetos File do Gemini

    Returns:
        String formatada com a lista de documentos disponíveis
    """
    if not uploaded_files:
        return "⚠️ Nenhum documento carregado."

    context = "📄 Documentos disponíveis para consulta:\n\n"
    for idx, file in enumerate(uploaded_files, 1):
        display_name = getattr(file, 'display_name', getattr(
            file, 'name', 'Documento sem nome'))
        context += f"{idx}. {display_name}\n"

    context += "\n✅ Esses são os regulamentos oficiais da FACOMP/UFPA que devem ser usados como única fonte de verdade."

    return context
