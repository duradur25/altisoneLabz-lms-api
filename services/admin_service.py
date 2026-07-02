from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.lms_models import User, Mentor, Student, Assignment, Submission
from core.security import hash_pw


def get_all_mentors(db: Session, pagination):
    query = db.query(Mentor)
    total = query.count()
    mentors = query.offset(pagination.offset).limit(pagination.limit).all()

    return {
        "total": total,
        "page": pagination.page,
        "limit": pagination.limit,
        "data": [
            {
                "id": m.id,
                "name": m.name,
                "email": m.user.email,
                "specialization": m.specialization
            }
            for m in mentors
        ]
    }


def create_mentor(db: Session, data):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_pw(data.password),
        role="mentor"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    mentor = Mentor(
        user_id=user.id,
        name=data.name,
        specialization=data.specialization
    )
    db.add(mentor)
    db.commit()
    db.refresh(mentor)

    return {
        "id": mentor.id,
        "name": mentor.name,
        "email": user.email,
        "specialization": mentor.specialization
    }


def update_mentor(db: Session, mentor_id: int, data):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    mentor.name = data.name
    mentor.specialization = data.specialization
    mentor.user.name = data.name

    db.commit()
    db.refresh(mentor)

    return {
        "id": mentor.id,
        "name": mentor.name,
        "email": mentor.user.email,
        "specialization": mentor.specialization
    }


def delete_mentor(db: Session, mentor_id: int):
    mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")

    user = mentor.user
    db.delete(mentor)
    db.delete(user)
    db.commit()

    return {"message": "Mentor deleted successfully"}


def get_dashboard(db: Session):
    total_students = db.query(Student).count()
    total_mentors = db.query(Mentor).count()
    total_assignments = db.query(Assignment).count()
    pending_reviews = db.query(Submission).filter(Submission.status == "pending").count()
    completed_assignments = db.query(Submission).filter(Submission.status == "reviewed").count()

    return {
        "total_students": total_students,
        "total_mentors": total_mentors,
        "total_assignments": total_assignments,
        "pending_reviews": pending_reviews,
        "completed_assignments": completed_assignments
    }