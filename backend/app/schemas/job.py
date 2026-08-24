from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str
    skills: list[str] = []
    experience_min: int | None = None
    experience_max: int | None = None
    source_url: str | None = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str | None = None
    description: str
    skills: list[str]
    experience_min: int | None = None
    experience_max: int | None = None
    source_url: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class JobMatchResponse(BaseModel):
    job: JobResponse

    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]

    match_percentage: float

    recommendation: str