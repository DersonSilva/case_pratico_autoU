import os
import logging
from io import BytesIO
from typing import Optional

import requests
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PyPDF2 import PdfReader

# --- Configuração de logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Carrega variáveis de ambiente ---
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Configuração do FastAPI ---
app = FastAPI(title="Email Analyzer - AutoU")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
CANDIDATE_LABELS = ["Produtivo", "Improdutivo"]
FALLBACK_REPLIES = {
    "Produtivo": "Obrigado pelo contato. Vamos analisar sua solicitação e retornar em breve.",
    "Improdutivo": "Agradecemos sua mensagem! Não é necessária ação adicional."
}

# --- Página inicial ---
@app.get("/", response_class=HTMLResponse)
async def get_index() -> str:
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# --- Fallback simples ---
def fallback_classification(content: str) -> dict:
    keywords = ["solicito", "atualização", "erro", "problema", "dúvida", "pedido"]
    category = "Produtivo" if any(word in content.lower() for word in keywords) else "Improdutivo"
    return {"category": category, "suggested_reply": FALLBACK_REPLIES[category]}

# --- Função para classificar texto usando Hugging Face ---
def classify_text_hf(text: str) -> dict:
    if not HF_TOKEN:
        return fallback_classification(text)

    url = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": CANDIDATE_LABELS}}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        category = data.get('labels', [None])[0] or "Improdutivo"
        suggested_reply = FALLBACK_REPLIES.get(category, FALLBACK_REPLIES["Improdutivo"])
        return {"category": category, "suggested_reply": suggested_reply}
    except Exception as e:
        logging.error(f"Erro Hugging Face: {e}")
        return fallback_classification(text)

# --- Funções utilitárias para ler arquivos ---
def read_txt_file(file_content: bytes) -> str:
    try:
        return file_content.decode("utf-8")
    except Exception as e:
        logging.error(f"Erro decodificando TXT: {e}")
        raise ValueError("Não foi possível ler o arquivo TXT.")

def read_pdf_file(file_content: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        logging.error(f"Erro lendo PDF: {e}")
        raise ValueError("Não foi possível ler o PDF enviado.")

# --- Endpoint para análise ---
@app.post("/analyze")
async def analyze_email(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
) -> JSONResponse:
    content = ""

    if file:
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            return JSONResponse(content={"error": "Arquivo muito grande. Máx. 5 MB."})

        ext = file.filename.split(".")[-1].lower()
        logging.info(f"Upload recebido: {file.filename} ({ext})")

        try:
            if ext == "txt":
                content = read_txt_file(file_content)
            elif ext == "pdf":
                content = read_pdf_file(file_content)
            else:
                return JSONResponse(content={"error": "Apenas arquivos .txt ou .pdf são suportados."})
        except ValueError as e:
            return JSONResponse(content={"error": str(e)})

    elif text:
        content = text.strip()
    else:
        return JSONResponse(content={"error": "Nenhum texto ou arquivo enviado."})

    if not content:
        return JSONResponse(content={"error": "O conteúdo enviado está vazio."})

    result = classify_text_hf(content)
    return JSONResponse(content=result)




















