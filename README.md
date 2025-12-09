# facompchatbot

> Mini-projeto que implementa um sistema multi-agente especializado usando modelos de linguagem (Gemini), prompt engineering e contexto baseado em documentos da FACOMP/UFPA. O objetivo é permitir consultas inteligentes e automáticas aos regulamentos acadêmicos.

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install google-generativeai google-adk beautifulsoup4 python-dotenv

# 2. Configurar API Key
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env

# 3. Adicionar PDFs na pasta data/

# 4a. Usar ADK Web (interface gráfica)
adk web src

# 4b. Ou executar via Python
python main.py
```

### Status do Projeto

- [x] Estrutura modular e organizada
- [x] Sistema multi-agente com ADK
- [x] Integração com Gemini API
- [x] Upload e leitura de PDFs
- [x] Ferramentas customizadas (busca em link, busca em PDF)
- [x] Interface ADK Web
- [ ] Testes unitários
- [ ] Deploy em produção

## 📁 Estrutura do Projeto

```
facompbot/
│
├── src/
│   └── facompbot/
│       ├── __init__.py           # Inicialização do pacote
│       ├── agent.py              # Classe base dos agentes
│       ├── agents_factory.py     # Factory para criação dos agentes multi-agente
│       ├── prompts.py            # Instruções e prompts do sistema
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

### Opção 2: Integração com Código

```python
from facompbot.document_tools import load_documents
from facompbot.prompts import SYSTEM_INSTRUCTION
from facompbot.config import setup_environment
import google.generativeai as genai

# Configurar ambiente
setup_environment()

# Carregar documentos
uploaded_files = load_documents("data")

# Criar modelo
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# Iniciar chat
chat = model.start_chat()
response = chat.send_message("Sua pergunta aqui")
print(response.text)
```

## 📫 Contribuindo para facompchatbot

1. Faça um fork do repositório
2. Crie um branch:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça alterações e confirme:
   ```bash
   git commit -m "Descrição da alteração"
   ```
4. Envie para o repositório:
   ```bash
   git push origin minha-feature
   ```
5. Crie um Pull Request

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
