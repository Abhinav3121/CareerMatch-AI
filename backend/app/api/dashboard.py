from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user

from app.database import get_db

from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("")
def get_dashboard(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    resumes = (
        db.query(Resume)
        .filter(
            Resume.user_id == current_user.id
        )
        .order_by(
            Resume.uploaded_at.desc()
        )
        .all()
    )

    jobs_count = (
        db.query(Job).count()
    )

    latest_resume = (
        resumes[0]
        if resumes
        else None
    )

    return {

        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
        },

        "resume_count": len(resumes),

        "job_count": jobs_count,

        "latest_resume": (
            {
                "id": latest_resume.id,

                "filename": (
                    latest_resume.original_filename
                ),

                "score": latest_resume.score,
            }
            if latest_resume
            else None
        ),
    }