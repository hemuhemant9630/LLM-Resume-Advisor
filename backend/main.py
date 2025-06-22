from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import os
import logging
import fitz  # PyMuPDF
import docx
from dotenv import load_dotenv

from backend.preprocessing import clean_text
from backend.parser import parse_resume_sections
from backend.models import ResumeAnalysis
from backend.llm_analyser import analyze_with_llm

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(file_path)
        text = " ".join([page.get_text() for page in doc])
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise ValueError("Failed to extract text from PDF")


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise ValueError("Failed to extract text from DOCX")


@app.post("/analyze-resume/", response_model=ResumeAnalysis)
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            # Extract text
            if file_ext == ".pdf":
                text = extract_text_from_pdf(tmp.name)
            elif file_ext == ".docx":
                text = extract_text_from_docx(tmp.name)
            else:
                text = content.decode("utf-8", errors="ignore")

        os.unlink(tmp.name)  # Clean up

        logger.info(f"Extracted text: {text[:500]}")  # Log first 500 chars

        logger.info("Cleaning resume text...")
        cleaned = clean_text(text)
        logger.info(f"Cleaned text: {cleaned[:500]}")

        logger.info("Parsing resume sections...")
        sections = parse_resume_sections(cleaned)
        logger.info(f"Parsed sections: {sections}")

        logger.info("Sending to LLM for analysis...")
        result = analyze_with_llm(sections)
        logger.info(f"LLM result: {result}")

        return ResumeAnalysis(**result)
    except ValueError as ve:
        logger.error(str(ve))
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
