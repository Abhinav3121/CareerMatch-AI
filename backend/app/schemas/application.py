from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationCreate(BaseModel):
    resume_id: int


class ApplicationUser(BaseModel):
    id: int
    name: str
    email: str


class ApplicationJob(BaseModel):
    id: int
    title: str
    company: str
    location: str | None = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int
    job_id: int
    resume_id: int

    status: str

    applied_at: datetime
    updated_at: datetime

    candidate: ApplicationUser
    job: ApplicationJob

    match_percentage: float | None = None
