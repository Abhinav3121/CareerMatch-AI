from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    original_filename: str
    file_type: str
    extracted_text: str | None
    analysis: dict[str, Any] | None
    score: int | None
    uploaded_at: datetime

    model_config = {
        "from_attributes": True,
    }