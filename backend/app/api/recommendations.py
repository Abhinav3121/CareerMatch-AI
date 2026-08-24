from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user

from app.database import get_db

from app.models.job import Job
from app.models.resume import Resume
from app.models.user import User

from app.services.skill_normalizer import compare_skills


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/resume/{resume_id}"
)
def recommend_jobs(
    resume_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    resume_skills = []

    if resume.analysis:

        resume_skills = resume.analysis.get(
            "skills",
            [],
        )

    jobs = (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .all()
    )

    recommendations = []

    for job in jobs:

        result = compare_skills(
            resume_skills,
            job.skills,
        )

        percentage = result[
            "match_percentage"
        ]

        if percentage >= 80:

            recommendation = "Strong match"

        elif percentage >= 60:

            recommendation = "Good match"

        elif percentage >= 40:

            recommendation = "Partial match"

        else:

            recommendation = "Low match"

        recommendations.append(
            {
                "job": {
                    "id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                },

                "match_percentage": percentage,

                "matched_skills": result[
                    "matched_skills"
                ],

                "missing_skills": result[
                    "missing_skills"
                ],

                "extra_skills": result[
                    "extra_skills"
                ],

                "recommendation": recommendation,
            }
        )

    recommendations.sort(
        key=lambda item: item[
            "match_percentage"
        ],
        reverse=True,
    )

    return {
        "resume_id": resume.id,

        "resume_skills": resume_skills,

        "recommendations": recommendations,
    }