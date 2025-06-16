
# Resume Career Advisor using LLM

## Objective
Analyze a student's resume using an LLM and suggest:
- Suitable job roles
- Relevant online courses
- Resume feedback
- Personalized career roadmap

## Tech Stack
- LLM: OpenAI GPT-4
- Resume Parsing: PyMuPDF
- Backend: FastAPI
- Frontend: Streamlit
- Embeddings: Sentence-BERT, FAISS
- Deployment: Streamlit Cloud / Render

## Setup Instructions
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Run backend: `uvicorn backend.main:app --reload`
5. Run frontend: `streamlit run frontend/app.py`

## Deployment Links
- Streamlit: [To be deployed]
- Render API: [To be deployed]

## Sample Prompts
```
Analyze this resume and return:
1. Top 3 job roles
2. Skills to learn
3. Course links (Coursera/Udemy)
4. Resume feedback
```

## API Key Instructions
Store your OpenAI key in `.env`:
```
OPENAI_API_KEY=your-key-here
```
