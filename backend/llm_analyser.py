import os
import json
import requests
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import socket
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

# API Configuration
API_BASE_URL = "https://api.openrouter.ai/api/v1"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://openrouter.ai",
    "X-Title": "Resume Analyzer"
}

def check_internet_connection():
    try:
        # Try to resolve Google's DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def make_api_request(url: str, data: dict, max_retries: int = MAX_RETRIES) -> dict:
    if not check_internet_connection():
        raise ConnectionError("No internet connection available. Please check your network connection.")

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=45
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt + 1 < max_retries:
                time.sleep(RETRY_DELAY)
            else:
                raise ValueError(f"Failed to connect to OpenRouter API after {max_retries} attempts. Please check your internet connection and API key.")

def validate_response(response_data: Dict[str, Any]) -> bool:
    """Validate that the response contains all required fields."""
    required_fields = {
        "candidate_summary": ["education", "experience", "core_competencies", "career_level"],
        "recommended_roles": ["title", "suitability_score", "justification"],
        "skill_gaps": ["critical_skills", "recommended_skills", "nice_to_have"],
        "learning_advice": ["courses", "development_tips", "resume_improvements"]
    }

    try:
        # Check top-level structure
        for field in required_fields:
            if field not in response_data:
                logger.error(f"Missing top-level field: {field}")
                return False

        # Check candidate_summary fields
        for field in required_fields["candidate_summary"]:
            if field not in response_data["candidate_summary"]:
                logger.error(f"Missing candidate_summary field: {field}")
                return False

        # Check recommended_roles structure
        if not isinstance(response_data["recommended_roles"], list):
            logger.error("recommended_roles is not a list")
            return False
        for role in response_data["recommended_roles"]:
            for field in required_fields["recommended_roles"]:
                if field not in role:
                    logger.error(f"Missing role field: {field}")
                    return False

        # Check skill_gaps fields
        for field in required_fields["skill_gaps"]:
            if field not in response_data["skill_gaps"]:
                logger.error(f"Missing skill_gaps field: {field}")
                return False

        # Check learning_advice fields
        for field in required_fields["learning_advice"]:
            if field not in response_data["learning_advice"]:
                logger.error(f"Missing learning_advice field: {field}")
                return False

        return True
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return False

def analyze_with_llm(parsed_sections: dict) -> dict:
    try:
        # Create a clean, formatted text from the sections
        sectioned_text = "\n\n".join([
            f"=== {k.upper()} ===\n{v}" 
            for k, v in parsed_sections.items() 
            if v.strip()
        ])

        prompt = f"""You are an expert career advisor AI. Analyze the resume sections below and provide a detailed analysis in JSON format.

Resume Content:
{sectioned_text}

Provide your analysis in the following JSON structure exactly:
{{
    "candidate_summary": {{
        "education": "detailed education summary",
        "experience": "years and key experience summary",
        "core_competencies": "key skills and strengths",
        "career_level": "fresher/junior/mid-level/senior"
    }},
    "recommended_roles": [
        {{
            "title": "job title",
            "suitability_score": number between 0-100,
            "justification": "detailed explanation why"
        }}
    ],
    "skill_gaps": {{
        "critical_skills": ["must-learn skill 1", "must-learn skill 2"],
        "recommended_skills": ["good-to-have skill 1", "good-to-have skill 2"],
        "nice_to_have": ["optional skill 1", "optional skill 2"]
    }},
    "learning_advice": {{
        "courses": ["specific course recommendation 1", "specific course recommendation 2"],
        "development_tips": ["professional development tip 1", "professional development tip 2"],
        "resume_improvements": ["resume improvement suggestion 1", "resume improvement suggestion 2"]
    }}
}}"""

        body = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        logger.info("Checking internet connection...")
        if not check_internet_connection():
            raise ConnectionError("No internet connection available")

        logger.info("Sending request to OpenRouter API...")
        result = make_api_request(f"{API_BASE_URL}/chat/completions", body)

        if "choices" not in result or not result["choices"]:
            raise ValueError("No response choices returned from API")

        reply = result["choices"][0]["message"]["content"].strip()
        
        # Clean up JSON string if needed
        if reply.startswith("```json"):
            reply = reply[7:]
        if reply.endswith("```"):
            reply = reply[:-3]
        
        try:
            analysis = json.loads(reply)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {reply}")
            raise ValueError("Failed to parse API response as JSON")

        # Validate the response structure
        required_fields = {
            "candidate_summary": ["education", "experience", "core_competencies", "career_level"],
            "recommended_roles": ["title", "suitability_score", "justification"],
            "skill_gaps": ["critical_skills", "recommended_skills", "nice_to_have"],
            "learning_advice": ["courses", "development_tips", "resume_improvements"]
        }

        for field, subfields in required_fields.items():
            if field not in analysis:
                raise ValueError(f"Missing required field: {field}")
            
            if field == "recommended_roles":
                if not isinstance(analysis[field], list) or not analysis[field]:
                    raise ValueError("recommended_roles must be a non-empty list")
                for role in analysis[field]:
                    for subfield in subfields:
                        if subfield not in role:
                            raise ValueError(f"Missing subfield in role: {subfield}")
            else:
                for subfield in subfields:
                    if subfield not in analysis[field]:
                        raise ValueError(f"Missing subfield in {field}: {subfield}")

        return analysis

    except ConnectionError as e:
        logger.error(f"Connection error: {str(e)}")
        raise ValueError("Unable to connect to the API. Please check your internet connection.")
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise ValueError("Invalid response format from API")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise ValueError(f"An error occurred while analyzing the resume: {str(e)}")