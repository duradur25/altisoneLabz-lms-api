from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from database.config import get_db
from api.deps import require_mentor
from models.lms_models import User
from utils.pagination import Pagination
import services.mentor_service as mentor_service

router = APIRouter(prefix="/mentor", tags=["Mentor"])


class AssignmentCreate(BaseModel):
    title: str
    description: str | None = None
    batch_id: int
    due_date: date
    max_marks: int


class SubmissionReview(BaseModel):
    grade: int
    remarks: str


@router.get("/students")
def get_students(
    current_user: User = Depends(require_mentor),
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination)
):
    return mentor_service.get_students(db, current_user, pagination)


@router.get("/assignments")
def get_assignments(
    current_user: User = Depends(require_mentor),
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination)
):
    return mentor_service.get_assignments(db, current_user, pagination)


@router.post("/assignments", status_code=201)
def create_assignment(
    data: AssignmentCreate,
    current_user: User = Depends(require_mentor),
    db: Session = Depends(get_db)
):
    return mentor_service.create_assignment(db, current_user, data)


@router.get("/submissions")
def get_submissions(
    current_user: User = Depends(require_mentor),
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination)
):
    return mentor_service.get_submissions(db, current_user, pagination)


@router.patch("/submissions/{submission_id}")
def review_submission(
    submission_id: int,
    data: SubmissionReview,
    current_user: User = Depends(require_mentor),
    db: Session = Depends(get_db)
):
    return mentor_service.review_submission(db, current_user, submission_id, data)