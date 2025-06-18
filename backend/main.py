from preprocessing import clean_text
from parser import parse_resume_sections
from models import ResumeAnalysis
from llm_analyser import analyze_with_llm
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os
import logging
from dotenv import load_dotenv
import tempfile
from pathlib import Path
import docx

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
if not os.getenv("OPENROUTER_API_KEY"):
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

app = FastAPI()

# CORS for frontend access
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
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {str(e)}")
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

@app.post("/analyze-resume/", response_model=ResumeAnalysis)
async def analyze_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ['.pdf', '.docx', '.txt']:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF, DOCX, and TXT files are supported"
        )

    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file.flush()
            
            # Extract text based on file type
            try:
                if file_extension == '.pdf':
                    text = extract_text_from_pdf(temp_file.name)
                elif file_extension == '.docx':
                    text = extract_text_from_docx(temp_file.name)
                else:  # .txt
                    text = contents.decode('utf-8', errors='ignore')
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_file.name)
                except Exception as e:
                    logger.warning(f"Failed to delete temporary file: {str(e)}")

        # Process the resume
        logger.info("Cleaning extracted text...")
        cleaned_text = clean_text(text)
        
        logger.info("Parsing resume sections...")
        sections = parse_resume_sections(cleaned_text)
        
        logger.info("Analyzing resume with LLM...")
        analysis = analyze_with_llm(sections)
        
        return ResumeAnalysis(**analysis)

    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the resume"
        )
