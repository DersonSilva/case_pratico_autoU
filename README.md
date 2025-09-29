# Email Analyzer - AutoU

## Descrição do Projeto

O **Email Analyzer - AutoU** é uma aplicação web que automatiza a **leitura, classificação e sugestão de respostas para emails**, com foco em liberar tempo da equipe que atualmente realiza essa tarefa manualmente.

A aplicação classifica os emails em duas categorias:

- **Produtivo:** Emails que requerem ação ou resposta específica (ex.: solicitação de suporte, atualização de pedido).
- **Improdutivo:** Emails que não necessitam de ação imediata (ex.: mensagens de felicitações, agradecimentos).

A aplicação suporta **upload de arquivos `.txt` e `.pdf`** ou a inserção direta de texto, processando o conteúdo e sugerindo uma resposta automática baseada na categoria identificada.

---

## Funcionalidades

1. **Interface Web (Frontend)**

   - Upload de arquivos `.txt` ou `.pdf` e campo de texto para colar emails diretamente.
   - Botão de análise com feedback visual e loading.
   - Exibição da **categoria do email** e da **resposta sugerida**.
   - Interface responsiva e amigável, preparada para usuários não técnicos.

2. **Backend (Python + FastAPI)**

   - Processamento de texto de arquivos ou input direto.
   - Suporte a PDFs grandes utilizando **PyPDF2**.
   - Classificação automática usando **API Hugging Face** (`facebook/bart-large-mnli`).
   - Fallback inteligente baseado em palavras-chave caso a API falhe.

3. **Hospedagem**

   - A aplicação pode ser hospedada em qualquer serviço de nuvem gratuito (ex.: **Render, Vercel, Heroku**).

---

## Tecnologias Utilizadas

- **Frontend:** HTML, CSS + TailwindCSS, JavaScript
- **Backend:** Python, FastAPI, PyPDF2
- **AI / NLP:** Hugging Face Transformers API
- **Outros:** dotenv (variáveis de ambiente), CORS, Logging

---

## Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/DersonSilva/case_pratico_autoU.git
cd case_pratico_autou

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
# Crie um arquivo .env na raiz do projeto e adicione:
HF_TOKEN=seu_token_huggingface


# Execute a aplicação
uvicorn app:app --reload

# Acesse no navegador
http://127.0.0.1:8000/
```
