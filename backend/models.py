from pydantic import BaseModel
from typing import List, Dict

class CandidateSummary(BaseModel):
    education: str
    experience: str
    core_competencies: str
    career_level: str

class RecommendedRole(BaseModel):
    title: str
    suitability_score: float
    justification: str

class SkillGaps(BaseModel):
    critical_skills: List[str]
    recommended_skills: List[str]
    nice_to_have: List[str]

class LearningAdvice(BaseModel):
    courses: List[str]
    development_tips: List[str]
    resume_improvements: List[str]

class ResumeAnalysis(BaseModel):
    candidate_summary: CandidateSummary
    recommended_roles: List[RecommendedRole]
    skill_gaps: SkillGaps
    learning_advice: LearningAdvice
