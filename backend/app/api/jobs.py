from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.dependencies import get_current_user
from app.database import get_db

from app.models.job import Job
from app.models.match import JobMatch
from app.models.resume import Resume
from app.models.user import User

from app.schemas.job import JobCreate
from app.schemas.job import JobMatchResponse
from app.schemas.job import JobResponse

from app.services.skill_normalizer import compare_skills


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


# ============================================================
# CREATE JOB — ADMIN ONLY
# ============================================================

@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    job_data: JobCreate,
    current_user: User = Depends(
        get_current_admin
    ),
    db: Session = Depends(get_db),
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        description=job_data.description,
        skills=job_data.skills,
        experience_min=job_data.experience_min,
        experience_max=job_data.experience_max,
        source_url=job_data.source_url,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# ============================================================
# LIST JOBS — CLIENT + ADMIN
# ============================================================

@router.get(
    "",
    response_model=list[JobResponse],
)
def list_jobs(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(Job)
        .order_by(Job.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return jobs


# ============================================================
# GET SINGLE JOB — CLIENT + ADMIN
# ============================================================

@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    return job


# ============================================================
# MATCH JOB WITH RESUME — CLIENT + ADMIN
# ============================================================

@router.post(
    "/{job_id}/match/{resume_id}",
    response_model=JobMatchResponse,
)
def match_job(
    job_id: int,
    resume_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Find job
    # --------------------------------------------------------

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # --------------------------------------------------------
    # Find user's resume
    # --------------------------------------------------------

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    # --------------------------------------------------------
    # Extract resume skills
    # --------------------------------------------------------

    resume_skills = []

    if resume.analysis:
        resume_skills = resume.analysis.get(
            "skills",
            [],
        )

    # --------------------------------------------------------
    # Compare skills
    # --------------------------------------------------------

    result = compare_skills(
        resume_skills,
        job.skills,
    )

    percentage = float(
        result["match_percentage"]
    )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    if percentage >= 80:
        recommendation = "Strong match"

    elif percentage >= 60:
        recommendation = "Good match"

    elif percentage >= 40:
        recommendation = "Partial match"

    else:
        recommendation = "Low match"

    # --------------------------------------------------------
    # Save match in database
    # --------------------------------------------------------

    match_record = JobMatch(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        match_percentage=percentage,
        recommendation=recommendation,
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        extra_skills=result["extra_skills"],
    )

    db.add(match_record)
    db.commit()
    db.refresh(match_record)

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "job": job,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "extra_skills": result["extra_skills"],
        "match_percentage": percentage,
        "recommendation": recommendation,
    }


# ============================================================
# UPDATE JOB — ADMIN ONLY
# ============================================================

@router.put(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    job_data: JobCreate,
    current_user: User = Depends(
        get_current_admin
    ),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    job.title = job_data.title
    job.company = job_data.company
    job.location = job_data.location
    job.description = job_data.description
    job.skills = job_data.skills
    job.experience_min = job_data.experience_min
    job.experience_max = job_data.experience_max
    job.source_url = job_data.source_url

    db.commit()
    db.refresh(job)

    return job


# ============================================================
# DELETE JOB — ADMIN ONLY
# ============================================================

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    job_id: int,
    current_user: User = Depends(
        get_current_admin
    ),
    db: Session = Depends(get_db),
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    db.delete(job)
    db.commit()

    return None
