from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.lms_models import Student, Assignment, Submission, Batch, Mentor


def get_mentor_profile(db: Session, current_user):
    mentor = db.query(Mentor).filter(Mentor.user_id == current_user.id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor profile not found")
    return mentor


def get_students(db: Session, current_user, pagination):
    mentor = get_mentor_profile(db, current_user)
    query = db.query(Student).filter(Student.mentor_id == mentor.id)
    total = query.count()
    students = query.offset(pagination.offset).limit(pagination.limit).all()

    result = []
    for student in students:
        total_assignments = db.query(Assignment).filter(
            Assignment.batch_id == student.batch_id
        ).count()

        completed = db.query(Submission).filter(
            Submission.student_id == student.id,
            Submission.status == "reviewed"
        ).count()

        progress = (completed / total_assignments * 100) if total_assignments > 0 else 0

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "batch": student.batch.name,
            "course": student.batch.course,
            "progress_percentage": round(progress, 1),
            "last_active": student.last_active
        })

    return {"total": total, "page": pagination.page, "limit": pagination.limit, "data": result}


def get_assignments(db: Session, current_user, pagination):
    mentor = get_mentor_profile(db, current_user)
    query = db.query(Assignment).filter(Assignment.mentor_id == mentor.id)
    total = query.count()
    assignments = query.offset(pagination.offset).limit(pagination.limit).all()

    return {
        "total": total,
        "page": pagination.page,
        "limit": pagination.limit,
        "data": [
            {
                "id": a.id,
                "title": a.title,
                "description": a.description,
                "batch": a.batch.name,
                "due_date": a.due_date,
                "max_marks": a.max_marks
            }
            for a in assignments
        ]
    }


def create_assignment(db: Session, current_user, data):
    mentor = get_mentor_profile(db, current_user)

    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    assignment = Assignment(
        title=data.title,
        description=data.description,
        batch_id=data.batch_id,
        mentor_id=mentor.id,
        due_date=data.due_date,
        max_marks=data.max_marks
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "batch": batch.name,
        "due_date": assignment.due_date,
        "max_marks": assignment.max_marks
    }


def get_submissions(db: Session, current_user, pagination):
    mentor = get_mentor_profile(db, current_user)
    query = db.query(Submission).join(Assignment).filter(Assignment.mentor_id == mentor.id)
    total = query.count()
    submissions = query.offset(pagination.offset).limit(pagination.limit).all()

    return {
        "total": total,
        "page": pagination.page,
        "limit": pagination.limit,
        "data": [
            {
                "id": s.id,
                "student": s.student.name,
                "assignment": s.assignment.title,
                "grade": s.grade,
                "remarks": s.remarks,
                "status": s.status
            }
            for s in submissions
        ]
    }


def review_submission(db: Session, current_user, submission_id: int, data):
    mentor = get_mentor_profile(db, current_user)

    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    if submission.assignment.mentor_id != mentor.id:
        raise HTTPException(status_code=403, detail="This submission does not belong to you")

    submission.grade = data.grade
    submission.remarks = data.remarks
    submission.status = "reviewed"

    db.commit()
    db.refresh(submission)

    return {
        "id": submission.id,
        "grade": submission.grade,
        "remarks": submission.remarks,
        "status": submission.status
    }