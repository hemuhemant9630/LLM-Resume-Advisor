from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    doc = fitz.open("temp_resume.pdf")
    text = " ".join([page.get_text() for page in doc])

    prompt = f"""
You are a career coach AI. Analyze the resume below and respond with:

1. Top 3 suitable job roles
2. Missing skill gaps
3. Recommended online courses (mention platforms)
4. 3 resume improvement tips

Resume:
{text}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # IMPORTANT for OpenRouter!
        "X-Title": "LLM Resume Advisor"
    }

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {e}"

    return {"gpt_analysis": reply}
