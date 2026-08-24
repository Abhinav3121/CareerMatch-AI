from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MatchHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    resume_id: int
    resume_filename: str

    job_id: int
    job_title: str
    company: str

    match_percentage: float
    recommendation: str

    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]

    created_at: datetime
