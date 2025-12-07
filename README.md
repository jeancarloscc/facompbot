# facompchatbot

![GitHub repo size](https://img.shields.io/github/repo-size/jeancarloscc/facompbot?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/jeancarloscc/facompbot?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/jeancarloscc/facompbot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/jeancarloscc/facompbot?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jeancarloscc/facompbot?style=for-the-badge)

> Mini-projeto que implementa um chatbot especializado usando modelos de linguagem, prompt engineering e contexto baseado em documentos da FACOMP/UFPA. O objetivo é permitir consultas diretas aos regulamentos disponibilizados.

## 🚀 Quick Start

```bash
# 1. Instalar dependências
pip install google-generativeai google-adk python-dotenv

# 2. Configurar API Key
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env

# 3. Adicionar PDFs na pasta data/

# 4a. Usar ADK Web (interface gráfica)
adk web src

# 4b. Ou executar via Python
python main.py
```

📖 **[Guia Completo de Uso](USAGE.md)**

### Status do Projeto

* [x] Estrutura do projeto organizada
* [x] Integração com Gemini API
* [x] Upload e leitura de PDFs
* [x] Implementação de agentes
* [x] Interface ADK Web
* [ ] Testes unitários
* [ ] Deploy em produção

## 📁 Estrutura do Projeto

```
facompbot/
│
├── src/
│   ├── facomp_agent.py         # Agente para ADK Web
│   └── facompbot/
│       ├── agent/              # Classes de agentes customizados
│       ├── prompts/            # Instruções e prompts do sistema
│       ├── tools/              # Ferramentas (upload PDFs, etc.)
│       ├── utils/              # Utilitários gerais
│       └── config/             # Configurações
│
├── data/                       # PDFs dos regulamentos
├── notebooks/                  # Jupyter notebooks para experimentos
├── tests/                      # Testes unitários e de integração
│
├── main.py                     # Script standalone
├── USAGE.md                    # Documentação de uso detalhada
├── pyproject.toml
└── README.md
```


## 💻 Pré-requisitos

* Python 3.10+
* Chave de API do Google (Gemini)
* Google ADK (opcional, para interface web)

## 🚀 Instalação

```bash
# Instalar dependências
pip install google-generativeai google-adk python-dotenv

# Ou com poetry
poetry add google-generativeai google-adk python-dotenv

# Configurar API Key
echo "GOOGLE_API_KEY=sua-chave-aqui" > .env
```

## ☕ Como Usar

### Opção 1: ADK Web (Interface Gráfica)

```bash
# Iniciar servidor
adk web src

# Acessar no navegador
http://localhost:8000
```

### Opção 2: Script Python

```bash
# Executar com perguntas de demonstração
python main.py

# Para modo interativo, edite main.py e descomente:
# interactive_mode(chat)
```

### Opção 3: Integração com Código

```python
from src.facompbot.tools.document_tools import load_documents
from src.facompbot.prompts.prompts import SYSTEM_INSTRUCTION
import google.generativeai as genai

genai.configure(api_key="sua-chave")
uploaded_files = load_documents("data")

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=SYSTEM_INSTRUCTION
)

chat = model.start_chat()
response = chat.send_message("Sua pergunta aqui")
print(response.text)
```

📖 **[Documentação Completa](USAGE.md)**

## 📫 Contribuindo para facompchatbot

Para contribuir:

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

Para mais detalhes, consulte a documentação do GitHub sobre Pull Requests.

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
