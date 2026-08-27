from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.core.dependencies import get_current_user
from app.database import get_db

from app.models.application import Application
from app.models.job import Job
from app.models.match import JobMatch
from app.models.resume import Resume
from app.models.user import User

from app.schemas.application import ApplicationCreate
from app.schemas.application import ApplicationResponse


router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


# ============================================================
# RESPONSE HELPER
# ============================================================

def application_to_response(
    application: Application,
    db: Session,
):
    match = (
        db.query(JobMatch)
        .filter(
            JobMatch.user_id == application.user_id,
            JobMatch.resume_id == application.resume_id,
            JobMatch.job_id == application.job_id,
        )
        .order_by(
            JobMatch.created_at.desc()
        )
        .first()
    )

    return {
        "id": application.id,
        "user_id": application.user_id,
        "job_id": application.job_id,
        "resume_id": application.resume_id,
        "status": application.status,
        "applied_at": application.applied_at,
        "updated_at": application.updated_at,
        "candidate": {
            "id": application.user.id,
            "name": application.user.name,
            "email": application.user.email,
        },
        "job": {
            "id": application.job.id,
            "title": application.job.title,
            "company": application.job.company,
            "location": application.job.location,
        },
        "match_percentage": (
            match.match_percentage
            if match is not None
            else None
        ),
    }


# ============================================================
# CLIENT - APPLY FOR JOB
# ============================================================

@router.post(
    "/{job_id}",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def apply_for_job(
    job_id: int,
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
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

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == application_data.resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    existing_application = (
        db.query(Application)
        .filter(
            Application.user_id == current_user.id,
            Application.job_id == job_id,
        )
        .first()
    )

    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied for this job",
        )

    application = Application(
        user_id=current_user.id,
        job_id=job_id,
        resume_id=resume.id,
        status="pending",
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application_to_response(
        application,
        db,
    )


# ============================================================
# CLIENT - MY APPLICATIONS
# ============================================================

@router.get(
    "/me",
    response_model=list[ApplicationResponse],
)
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    applications = (
        db.query(Application)
        .filter(
            Application.user_id == current_user.id
        )
        .order_by(
            Application.applied_at.desc()
        )
        .all()
    )

    return [
        application_to_response(
            application,
            db,
        )
        for application in applications
    ]


# ============================================================
# ADMIN - ALL APPLICATIONS
# ============================================================

@router.get(
    "/admin/all",
    response_model=list[ApplicationResponse],
)
def get_all_applications(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    applications = (
        db.query(Application)
        .order_by(
            Application.applied_at.desc()
        )
        .all()
    )

    return [
        application_to_response(
            application,
            db,
        )
        for application in applications
    ]


# ============================================================
# CLIENT - SINGLE APPLICATION
# ============================================================

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_my_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application_to_response(
        application,
        db,
    )


# ============================================================
# ADMIN - ACCEPT APPLICATION
# ============================================================

@router.put(
    "/admin/{application_id}/accept",
    response_model=ApplicationResponse,
)
def accept_application(
    application_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    application.status = "accepted"

    db.commit()
    db.refresh(application)

    return application_to_response(
        application,
        db,
    )


# ============================================================
# ADMIN - REJECT APPLICATION
# ============================================================

@router.put(
    "/admin/{application_id}/reject",
    response_model=ApplicationResponse,
)
def reject_application(
    application_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    application.status = "rejected"

    db.commit()
    db.refresh(application)

    return application_to_response(
        application,
        db,
    )
