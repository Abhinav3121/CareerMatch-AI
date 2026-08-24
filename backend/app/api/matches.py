from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db

from app.models.match import JobMatch
from app.models.user import User

from app.schemas.match import MatchHistoryResponse


router = APIRouter(
    prefix="/matches",
    tags=["Match History"],
)


@router.get(
    "",
    response_model=list[MatchHistoryResponse],
)
def list_matches(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    matches = (
        db.query(JobMatch)
        .filter(
            JobMatch.user_id == current_user.id
        )
        .order_by(
            JobMatch.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    results = []

    for match in matches:
        results.append(
            {
                "id": match.id,
                "resume_id": match.resume_id,
                "resume_filename": (
                    match.resume.original_filename
                ),
                "job_id": match.job_id,
                "job_title": match.job.title,
                "company": match.job.company,
                "match_percentage": (
                    match.match_percentage
                ),
                "recommendation": (
                    match.recommendation
                ),
                "matched_skills": (
                    match.matched_skills or []
                ),
                "missing_skills": (
                    match.missing_skills or []
                ),
                "extra_skills": (
                    match.extra_skills or []
                ),
                "created_at": match.created_at,
            }
        )

    return results


@router.get(
    "/{match_id}",
    response_model=MatchHistoryResponse,
)
def get_match(
    match_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    match = (
        db.query(JobMatch)
        .filter(
            JobMatch.id == match_id,
            JobMatch.user_id == current_user.id,
        )
        .first()
    )

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found",
        )

    return {
        "id": match.id,
        "resume_id": match.resume_id,
        "resume_filename": (
            match.resume.original_filename
        ),
        "job_id": match.job_id,
        "job_title": match.job.title,
        "company": match.job.company,
        "match_percentage": (
            match.match_percentage
        ),
        "recommendation": (
            match.recommendation
        ),
        "matched_skills": (
            match.matched_skills or []
        ),
        "missing_skills": (
            match.missing_skills or []
        ),
        "extra_skills": (
            match.extra_skills or []
        ),
        "created_at": match.created_at,
    }
