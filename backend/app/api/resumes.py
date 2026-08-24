from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.resume import Resume
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_analyzer import analyze_resume
from app.services.resume_parser import extract_resume_text


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


UPLOAD_DIR = (
    Path(__file__).resolve().parents[3]
    / "storage"
    / "resumes"
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}


MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    original_filename = file.filename or ""

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are allowed",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size must not exceed 5 MB",
        )

    if (
        extension == ".pdf"
        and not content.startswith(b"%PDF-")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PDF file",
        )

    if (
        extension == ".docx"
        and not content.startswith(b"PK")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid DOCX file",
        )

    stored_filename = (
        f"{uuid4().hex}{extension}"
    )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = UPLOAD_DIR / stored_filename

    file_path.write_bytes(content)

    try:
        extracted_text = extract_resume_text(
            str(file_path)
        )

    except Exception as exc:
        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to extract text from resume",
        ) from exc

    if not extracted_text:
        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No readable text found in resume",
        )

    analysis = analyze_resume(
        extracted_text
    )

    score = analysis.get(
        "score",
        0,
    )

    resume = Resume(
        user_id=current_user.id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        file_type=extension.lstrip("."),
        extracted_text=extracted_text,
        analysis=analysis,
        score=score,
    )

    try:
        db.add(resume)
        db.commit()
        db.refresh(resume)

    except Exception:
        db.rollback()

        file_path.unlink(
            missing_ok=True
        )

        raise

    return resume


@router.get(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return resume
