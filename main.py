from fastapi import FastAPI, UploadFile, File, Form
from utils import extract_text_from_pdf
from summarizer import summarize_text
import pdfplumber

app = FastAPI()

@app.post("/summarize/")
async def summarize_document(file: UploadFile = File(...), question: str = Form(None)):
    # Use file.file directly
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    summary = summarize_text(text, question)

    return {"summary": summary}
