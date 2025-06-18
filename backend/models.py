from typing import Dict, List
from pydantic import BaseModel

class ResumeAnalysis(BaseModel):
    candidate_summary: Dict[str, str]
    recommended_roles: List[Dict[str, str]]
    skill_gaps: Dict[str, List[str]]
    learning_advice: Dict[str, List[str]]