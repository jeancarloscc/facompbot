# facompchatbot

![GitHub repo size](https://img.shields.io/github/repo-size/jeancarloscc/facompbot?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/jeancarloscc/facompbot?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/jeancarloscc/facompbot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/jeancarloscc/facompbot?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/jeancarloscc/facompbot?style=for-the-badge)

> Mini-projeto que implementa um chatbot especializado usando modelos de linguagem, prompt engineering e contexto baseado em documentos da FACOMP/UFPA. O objetivo é permitir consultas diretas aos regulamentos disponibilizados.

### Ajustes e melhorias

O projeto está em fase inicial de desenvolvimento e as próximas atualizações serão voltadas para:

* [ ] Estruturação do notebook principal
* [ ] Integração com modelos generativos
* [ ] Upload e leitura dos PDFs regulatórios
* [ ] Implementação dos agentes
* [ ] Painel básico de consulta

## 💻 Pré-requisitos

Antes de começar, verifique se você possui:

* Python 3.10 ou superior instalado
* `pip`, `poetry` ou `uv` como gerenciador de pacotes
* Jupyter Notebook
* Chaves de API válidas do provedor de modelo usado (ex: OpenAI, Anthropic, etc.)

## 🚀 Instalando facompchatbot

### Usando pip

```bash
pip install -r requirements.txt
```

### Usando Poetry

```bash
poetry install
```

### Usando uv

```bash
uv pip install -r requirements.txt
```

## ☕ Usando facompchatbot

### Com pip ou uv

```bash
jupyter notebook
```

### Com Poetry

```bash
poetry run jupyter notebook
```

Abra o notebook principal e execute as células para:

* Carregar os documentos PDF
* Indexar o conteúdo
* Enviar perguntas ao chatbot
* Obter respostas fundamentadas nos arquivos

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
