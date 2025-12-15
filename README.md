# facompchatbot

![GitHub repo size](https://img.shields.io/github/repo-size/jeancarloscc/facompbot?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/jeancarloscc/facompbot?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/jeancarloscc/facompbot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/jeancarloscc/facompbot?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jeancarloscc/facompbot?style=for-the-badge)

> Mini-projeto que implementa um sistema multi-agente especializado usando modelos de linguagem (Gemini), prompt engineering e contexto baseado em documentos da FACOMP/UFPA. O objetivo é permitir consultas inteligentes e automáticas aos regulamentos acadêmicos.

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install google-generativeai google-adk beautifulsoup4 python-dotenv

# 2. Configurar API Key
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env

# 3. Adicionar PDFs na pasta data/

# 4. Executar via Python
python main.py
```

### Status do Projeto

- [x] Estrutura modular e organizada
- [x] Sistema multi-agente com ADK
- [x] Integração com Gemini API
- [x] Upload e leitura de PDFs
- [x] Ferramentas customizadas (busca em link, busca em PDF)
- [x] **MemoryBank - Sistema de memória de longo prazo**
- [x] **AgentOrchestrator - Execução paralela, sequencial e em loop**
- [ ] Testes unitários
- [ ] Deploy em produção

## 📁 Estrutura do Projeto

```
facompbot/
│
├── src/
│   └── facompbot/
│       ├── agent.py              # Classe base dos agentes
│       ├── agents_factory.py     # Factory para criação dos agentes multi-agente
│       ├── prompts.py            # Instruções e prompts do sistema
│       ├── orchestrator.py       # 🆕 Orquestrador (paralelo, sequencial, loop)
│       ├── memory.py             # 🆕 MemoryBank - memória de longo prazo
│       ├── document_tools.py     # Ferramentas (busca em PDFs, busca em links)
│       ├── runner.py             # Runner e integração com ADK
│       ├── config.py             # Configurações e ambiente
│       └── events.py             # Eventos e callbacks customizados
│
├── data/                         # PDFs dos regulamentos
├── notebooks/                    # Jupyter notebooks para experimentos
├── tests/                        # Testes unitários e de integração
│
├── main.py                       # Script principal (multi-agente)
├── pyproject.toml
└── README.md
```

## 💻 Pré-requisitos

- Python 3.10+
- Chave de API do Google (Gemini)
- Google ADK (para interface web e multi-agente)
- beautifulsoup4 (para busca em links)

## 🚀 Instalação

```bash
# Instalar dependências
pip install google-generativeai google-adk beautifulsoup4 python-dotenv

# Ou com poetry
poetry add google-generativeai google-adk beautifulsoup4 python-dotenv

# Configurar API Key
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env
```

## ☕ Como Usar

### Opção 1: Script Python Multi-Agente

```bash
python main.py
# O sistema irá rotear perguntas automaticamente para o agente especializado
```

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/jeancarloscc" title="Jean Carlos">
        <img src="https://github.com/jeancarloscc.png" width="100px;" style="border-radius:50%;" alt="Jean Carlos"/><br>
        <sub><b>Jean Carlos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/emillycaroline" title="Emilly Caroline">
        <img src="https://github.com/emillycaroline.png" width="100px;" style="border-radius:50%;" alt="Emilly Caroline"/><br>
        <sub><b>Emilly Caroline</b></sub>
      </a>
    </td>
  </tr>
</table>
