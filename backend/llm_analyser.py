import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def analyze_with_llm(parsed_sections: dict) -> dict:
    sectioned_text = "\n\n".join([
        f"=== {k.upper()} ===\n{v}" for k, v in parsed_sections.items() if v.strip()
    ])

    prompt = f"""
You are an expert career advisor AI. Analyze the resume sections below and provide a detailed, personalized analysis in JSON format.

Resume Content:
{sectioned_text}

Instructions:
- Carefully read the candidate's skills, experience, and education.
- Recommend 5 different job roles, prioritized by best fit for the candidate's background. Each role must be relevant to their unique skills and experience.
- For each recommended role, provide a suitability score (0-100) and a justification based on the resume.
- In the skill_gaps section, list:
    - critical_skills: essential skills missing for the top roles,
    - recommended_skills: skills that would improve the candidate's profile,
    - nice_to_have: additional skills that could be beneficial.
- Add a field "missing_from_resume": a list of important skills or keywords that are relevant to the candidate's target roles but are not present in the resume and should be added.
- In learning_advice, suggest specific courses, development tips, and resume improvements tailored to the candidate.

Respond ONLY in this JSON format:
{{
  "candidate_summary": {{
    "education": "...",
    "experience": "...",
    "core_competencies": "...",
    "career_level": "fresher/junior/mid-level/senior"
  }},
  "recommended_roles": [
    {{
      "title": "...",
      "suitability_score": ...,
      "justification": "..."
    }}
    // 4 more roles
  ],
  "skill_gaps": {{
    "critical_skills": [],
    "recommended_skills": [],
    "nice_to_have": [],
    "missing_from_resume": []
  }},
  "learning_advice": {{
    "courses": [],
    "development_tips": [],
    "resume_improvements": []
  }}
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a resume analysis assistant. Return a JSON object matching the provided schema and instructions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.3,
    )

    llm_reply = response.choices[0].message.content
    logger.info(f"Raw LLM output: {llm_reply}")

    try:
        result = json.loads(llm_reply)
        return result
    except Exception as e:
        logger.error(f"LLM output could not be parsed as JSON: {e}")
        raise ValueError("Invalid JSON from LLM.")
