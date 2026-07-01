from pydantic import BaseModel
from datetime import datetime, date
from enum import Enum

class StudentResponse(BaseModel):
    id: int
    batch_id: int
    name: str
    email: str
    progress: int
    last_active: datetime

class MentorResponse(BaseModel):
    id: int
    user_id: int
    specialization: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

class BatchResponse(BaseModel):
    id: int
    mentor_id: int
    name: str
    course: str

class AssignmentResponse(BaseModel):
    id: int
    batch_id: int
    title: str
    description: str
    due_date: date
    max_marks: int

class StatusEnum(str, Enum):
    pending= "pending"
    reviewed= "reviewed"

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    grade: int
    remarks: str
    status: StatusEnum
    submitted_at: datetime