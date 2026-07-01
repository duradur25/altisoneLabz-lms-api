from sqlalchemy.orm import relationship
from database.config import engine
from database.config import Base
from sqlalchemy import String, Integer, Column, ForeignKey, Enum, DateTime, Date, Text


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    name = Column(String(100))
    email = Column(String(100), unique=True)
    progress = Column(Integer, default=0)
    last_active = Column(DateTime)
    mentor_id = Column(Integer, ForeignKey("mentors.id"))

    batch = relationship("Batch", back_populates="students")
    submissions = relationship("Submission", back_populates="student")
    mentor = relationship("Mentor", back_populates="students")


class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialization = Column(String(100))
    name = Column(String(100), nullable=False)

    user = relationship("User", back_populates="mentor")
    batches = relationship("Batch", back_populates="mentor")
    students = relationship("Student", back_populates="mentor")
    assignments = relationship("Assignment", back_populates="mentor")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum("admin", "mentor"), nullable=False)

    mentor = relationship("Mentor", back_populates="user", uselist=False)


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey("mentors.id"))
    name = Column(String(100))
    course = Column(String(100))

    mentor = relationship("Mentor", back_populates="batches")
    students = relationship("Student", back_populates="batch")
    assignments = relationship("Assignment", back_populates="batch")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    title = Column(String(150))
    description = Column(Text)
    due_date = Column(Date)
    max_marks = Column(Integer)
    mentor_id = Column(Integer, ForeignKey("mentors.id"))

    batch = relationship("Batch", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")
    mentor = relationship("Mentor", back_populates="assignments")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    grade = Column(Integer)
    remarks = Column(Text)
    status = Column(
        Enum("pending", "reviewed"),
        default="pending"
    )
    submitted_at = Column(DateTime)

    assignment = relationship("Assignment", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")


Base.metadata.create_all(engine)