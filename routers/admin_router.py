from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database.config import get_db
from api.deps import require_admin
from models.lms_models import User
from utils.pagination import Pagination
import services.admin_service as admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])


class MentorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    specialization: str | None = None


class MentorUpdate(BaseModel):
    name: str
    specialization: str | None = None


@router.get("/mentors")
def get_mentors(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
    pagination: Pagination = Depends(Pagination)
):
    return admin_service.get_all_mentors(db, pagination)


@router.post("/mentors", status_code=201)
def create_mentor(
    data: MentorCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return admin_service.create_mentor(db, data)


@router.put("/mentors/{mentor_id}")
def update_mentor(
    mentor_id: int,
    data: MentorUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return admin_service.update_mentor(db, mentor_id, data)


@router.delete("/mentors/{mentor_id}")
def delete_mentor(
    mentor_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return admin_service.delete_mentor(db, mentor_id)


@router.get("/dashboard")
def get_dashboard(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return admin_service.get_dashboard(db)