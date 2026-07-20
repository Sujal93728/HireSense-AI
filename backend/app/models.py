from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship


# ======================================================
# USERS
# ======================================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship(
        "Resume",
        back_populates="user",
        uselist=False
    )

    chat_messages = relationship(
        "ChatMessage",
        back_populates="user"
    )

    interview_sessions = relationship(
        "InterviewSession",
        back_populates="user"
    )

    skills = relationship(
        "UserSkill",
        back_populates="user"
    )


# ======================================================
# JOB POSTINGS
# ======================================================

class JobPosting(Base):
    __tablename__ = "job_postings"

    job_id = Column(BigInteger, primary_key=True)

    company_id = Column(BigInteger)

    company_name = Column(String)

    title = Column(Text)

    description = Column(Text)

    location = Column(String)

    work_type = Column(String)

    formatted_experience_level = Column(String)

    max_salary = Column(Integer)

    med_salary = Column(Integer)

    min_salary = Column(Integer)

    application_url = Column(Text)


# ======================================================
# RESUME
# ======================================================

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    resume_text = Column(Text)

    analysis = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resume")


# ======================================================
# CHAT
# ======================================================

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    session_id = Column(
        String(100),
        index=True,
    )

    role = Column(String(20))

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    user = relationship(
    "User",
    back_populates="chat_messages"
)


# ======================================================
# INTERVIEW SESSION
# ======================================================

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    role = Column(String(100))
    difficulty = Column(String(30))
    score = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="interview_sessions"
    )

    questions = relationship(
        "InterviewQuestion",
        back_populates="session"
    )

    answers = relationship(
        "InterviewAnswer",
        back_populates="interview"
    )


# ======================================================
# INTERVIEW QUESTIONS
# ======================================================

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    question = Column(Text)
    answer = Column(Text)
    feedback = Column(Text)
    score = Column(Integer)

    session = relationship(
        "InterviewSession",
        back_populates="questions"
    )


# ======================================================
# INTERVIEW ANSWERS
# ======================================================

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)

    interview_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False
    )

    question = Column(Text)
    user_answer = Column(Text)
    score = Column(Integer)

    strengths = Column(Text)
    weaknesses = Column(Text)
    suggestions = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    interview = relationship(
        "InterviewSession",
        back_populates="answers"
    )


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    skill = Column(String(100), nullable=False)

    user = relationship(
    "User",
    back_populates="skills"
)

