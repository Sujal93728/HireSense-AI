from sqlalchemy.orm import Session
from sqlalchemy import func

from passlib.context import CryptContext

from . import models
from . import schemas

from .resume_reviewer import review_resume
from .job_matcher import calculate_match
from .skill_gap import compare_skills
from .career_roadmap import generate_roadmap

from sqlalchemy import or_
from .models import JobPosting, UserSkill
import json
from .resume_ai import analyze_resume

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =====================================================
# USER CRUD
# =====================================================

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(models.User)
        .filter(models.User.username == username)
        .first()
    )


def create_user(
    db: Session,
    user: schemas.UserCreate
):

    hashed_password = pwd_context.hash(
        user.password
    )

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not pwd_context.verify(
        password,
        user.hashed_password
    ):
        return None

    return user

# =====================================================
# JOB CRUD
# =====================================================

def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 20
):
    return (
        db.query(models.JobPosting)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_job(
    db: Session,
    job_id: int
):
    return (
        db.query(models.JobPosting)
        .filter(
            models.JobPosting.job_id == job_id
        )
        .first()
    )


def search_jobs(
    db: Session,
    keyword: str
):
    return (
        db.query(models.JobPosting)
        .filter(
            models.JobPosting.title.ilike(
                f"%{keyword}%"
            )
        )
        .all()
    )


def filter_jobs(
    db: Session,
    location=None,
    work_type=None
):

    query = db.query(models.JobPosting)

    if location:
        query = query.filter(
            models.JobPosting.location.ilike(
                f"%{location}%"
            )
        )

    if work_type:
        query = query.filter(
            models.JobPosting.work_type.ilike(
                f"%{work_type}%"
            )
        )

    return query.all()


# =====================================================
# JOB MATCH
# =====================================================

def recommend_jobs(
    db: Session,
    user_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:
        return []

    jobs = (
        db.query(models.JobPosting)
        .all()
    )

    recommendations = []

    for job in jobs:

        score = calculate_match(
            resume.resume_text,
            job.description
        )

        recommendations.append({
            "job": job,
            "score": score
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:20]


# =====================================================
# RESUME CRUD
# =====================================================

def get_resume(
    db: Session,
    user_id: int
):
    return (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .first()
    )


def save_resume(
    db: Session,
    user_id: int,
    resume_text: str
):

    resume = get_resume(
        db,
        user_id
    )

    if resume:

        resume.resume_text = resume_text

    else:

        resume = models.Resume(
            user_id=user_id,
            resume_text=resume_text
        )

        db.add(resume)

    db.commit()
    db.refresh(resume)

    return resume


def delete_resume(
    db: Session,
    user_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if resume:

        db.delete(resume)
        db.commit()

    return True

# =====================================================
# AI RESUME REVIEW
# =====================================================

def analyze_resume_ai(
    db: Session,
    user_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:

        return {
            "error": "Resume not uploaded."
        }

    return review_resume(
        resume.resume_text
    )

# =====================================================
# RESUME MATCH
# =====================================================

def resume_job_match(
    db: Session,
    user_id: int,
    job_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:

        return {
            "error": "Resume not uploaded."
        }

    job = (
        db.query(models.JobPosting)
        .filter(
            models.JobPosting.job_id == job_id
        )
        .first()
    )

    if not job:

        return {
            "error": "Job not found."
        }

    score = calculate_match(
        resume.resume_text,
        job.description
    )

    return {
        "job_id": job.job_id,
        "title": job.title,
        "company": job.company_name,
        "match_score": score
    }

# =====================================================
# SKILL GAP
# =====================================================

def skill_gap_analysis(
    db: Session,
    user_id: int,
    job_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:

        return {
            "error": "Resume not uploaded."
        }

    job = (
        db.query(models.JobPosting)
        .filter(
            models.JobPosting.job_id == job_id
        )
        .first()
    )

    if not job:

        return {
            "error": "Job not found."
        }

    return compare_skills(
        resume.resume_text,
        job.description
    )

# =====================================================
# CAREER ROADMAP
# =====================================================

def generate_roadmap(
    db: Session,
    user_id: int,
    target_role: str
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:

        return {
            "error": "Resume not uploaded."
        }

    return generate_roadmap(
        resume.resume_text,
        target_role
    )

# =====================================================
# CHAT CRUD
# =====================================================

def save_chat(
    db: Session,
    user_id: int,
    session_id: str,
    role: str,
    message: str
):
    chat = models.ChatMessage(
        user_id=user_id,
        session_id=session_id,
        role=role,
        message=message
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    session_id: str
):
    return (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.session_id == session_id
        )
        .order_by(
            models.ChatMessage.created_at.asc()
        )
        .all()
    )


def get_user_chat_history(
    db: Session,
    user_id: int
):
    return (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.user_id == user_id
        )
        .order_by(
            models.ChatMessage.created_at.desc()
        )
        .all()
    )


def get_chat_sessions(
    db: Session,
    user_id: int
):
    """
    Returns one record per chat session.
    """

    sessions = (
        db.query(models.ChatMessage.session_id)
        .filter(
            models.ChatMessage.user_id == user_id
        )
        .distinct()
        .all()
    )

    return [s[0] for s in sessions]


def clear_chat_session(
    db: Session,
    session_id: str
):
    (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.session_id == session_id
        )
        .delete()
    )

    db.commit()

    return True


def clear_user_chat(
    db: Session,
    user_id: int
):
    (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.user_id == user_id
        )
        .delete()
    )

    db.commit()

    return True


def delete_chat_message(
    db: Session,
    message_id: int
):
    message = (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.id == message_id
        )
        .first()
    )

    if not message:
        return False

    db.delete(message)
    db.commit()

    return True


def get_last_messages(
    db: Session,
    session_id: str,
    limit: int = 10
):
    return (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.session_id == session_id
        )
        .order_by(
            models.ChatMessage.created_at.desc()
        )
        .limit(limit)
        .all()[::-1]
    )


# =====================================================
# INTERVIEW CRUD
# =====================================================

def create_interview(
    db: Session,
    user_id: int,
    role: str,
    difficulty: str
):
    interview = models.InterviewSession(
        user_id=user_id,
        role=role,
        difficulty=difficulty,
        score=0
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


def get_interview(
    db: Session,
    interview_id: int
):
    return (
        db.query(models.InterviewSession)
        .filter(
            models.InterviewSession.id == interview_id
        )
        .first()
    )


def save_interview_answer(
    db: Session,
    interview_id: int,
    question: str,
    user_answer: str,
    ai_feedback: str,
    score: int
):
    answer = models.InterviewAnswer(
        interview_id=interview_id,
        question=question,
        user_answer=user_answer,
        suggestions=ai_feedback,
        score=score
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


def get_interview_answers(
    db: Session,
    interview_id: int
):
    return (
        db.query(models.InterviewAnswer)
        .filter(
            models.InterviewAnswer.interview_id == interview_id
        )
        .all()
    )


def update_interview_score(
    db: Session,
    interview_id: int
):
    interview = get_interview(
        db,
        interview_id
    )

    if interview is None:
        return 0

    answers = get_interview_answers(
        db,
        interview_id
    )

    if len(answers) == 0:
        interview.score = 0
    else:
        total = sum(a.score for a in answers)
        interview.score = round(total / len(answers))

    db.commit()

    return interview.score


def get_user_interviews(
    db: Session,
    user_id: int
):
    return (
        db.query(models.InterviewSession)
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .order_by(
            models.InterviewSession.created_at.desc()
        )
        .all()
    )


def get_interview_questions(
    db: Session,
    interview_id: int
):
    return get_interview_answers(
        db,
        interview_id
    )


def delete_interview(
    db: Session,
    interview_id: int
):
    db.query(models.InterviewAnswer).filter(
        models.InterviewAnswer.interview_id == interview_id
    ).delete()

    interview = get_interview(
        db,
        interview_id
    )

    if interview:
        db.delete(interview)

    db.commit()

    return True

# =====================================================
# INTERVIEW ANALYTICS
# =====================================================

def get_average_interview_score(
    db: Session,
    user_id: int
):
    result = (
        db.query(
            func.avg(models.InterviewSession.score)
        )
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .scalar()
    )

    return round(result or 0, 2)


def get_total_interviews(
    db: Session,
    user_id: int
):
    return (
        db.query(models.InterviewSession)
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .count()
    )


def get_best_interview_score(
    db: Session,
    user_id: int
):
    result = (
        db.query(
            func.max(models.InterviewSession.score)
        )
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .scalar()
    )

    return result or 0


def get_recent_interviews(
    db: Session,
    user_id: int,
    limit: int = 5
):
    return (
        db.query(models.InterviewSession)
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .order_by(
            models.InterviewSession.created_at.desc()
        )
        .limit(limit)
        .all()
    )

# =====================================================
# DASHBOARD CRUD
# =====================================================

def get_dashboard_stats(
    db: Session,
    user_id: int
):
    resume = get_resume(db, user_id)

    stats = {
        "resume_uploaded": resume is not None,
        "total_jobs": db.query(models.JobPosting).count(),
        "total_interviews": get_total_interviews(db, user_id),
        "average_score": get_average_interview_score(db, user_id),
        "best_score": get_best_interview_score(db, user_id),
        "chat_messages": (
            db.query(models.ChatMessage)
            .filter(models.ChatMessage.user_id == user_id)
            .count()
        )
    }

    return stats


# =====================================================
# RECENT ACTIVITY
# =====================================================

def get_recent_activity(
    db: Session,
    user_id: int
):

    chats = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == user_id)
        .order_by(models.ChatMessage.created_at.desc())
        .limit(5)
        .all()
    )

    interviews = (
        db.query(models.InterviewSession)
        .filter(models.InterviewSession.user_id == user_id)
        .order_by(models.InterviewSession.created_at.desc())
        .limit(5)
        .all()
    )

    return {
        "recent_chats": chats,
        "recent_interviews": interviews
    }

# =====================================================
# INTERVIEW TREND
# =====================================================

def get_interview_trend(
    db: Session,
    user_id: int
):

    interviews = (
        db.query(models.InterviewSession)
        .filter(
            models.InterviewSession.user_id == user_id
        )
        .order_by(
            models.InterviewSession.created_at.asc()
        )
        .all()
    )

    return [
        {
            "date": interview.created_at.strftime("%d %b"),
            "score": interview.score
        }
        for interview in interviews
    ]

# =====================================================
# CHAT ANALYTICS
# =====================================================

def get_chat_statistics(
    db: Session,
    user_id: int
):

    chats = (
        db.query(models.ChatMessage)
        .filter(
            models.ChatMessage.user_id == user_id
        )
        .all()
    )

    user_messages = len(
        [c for c in chats if c.role == "user"]
    )

    ai_messages = len(
        [c for c in chats if c.role == "assistant"]
    )

    return {
        "total_messages": len(chats),
        "user_messages": user_messages,
        "assistant_messages": ai_messages
    }


# =====================================================
# RESUME ANALYTICS
# =====================================================

def get_resume_statistics(
    db: Session,
    user_id: int
):

    resume = get_resume(
        db,
        user_id
    )

    if not resume:
        return {
            "uploaded": False
        }

    words = len(
        resume.resume_text.split()
    )

    chars = len(
        resume.resume_text
    )

    return {
        "uploaded": True,
        "word_count": words,
        "character_count": chars
    }

# =====================================================
# JOB ANALYTICS
# =====================================================

def get_job_statistics(
    db: Session
):

    jobs = db.query(models.JobPosting).all()

    remote = len([
        j for j in jobs
        if j.work_type
        and "remote" in j.work_type.lower()
    ])

    onsite = len([
        j for j in jobs
        if j.work_type
        and "on-site" in j.work_type.lower()
    ])

    hybrid = len([
        j for j in jobs
        if j.work_type
        and "hybrid" in j.work_type.lower()
    ])

    return {
        "total_jobs": len(jobs),
        "remote_jobs": remote,
        "onsite_jobs": onsite,
        "hybrid_jobs": hybrid
    }


# =====================================================
# USER ACTIVITY
# =====================================================

def get_user_activity(
    db: Session,
    user_id: int
):

    return {
        "resume_uploaded": get_resume(db, user_id) is not None,
        "chat_sessions": len(
            get_chat_sessions(
                db,
                user_id
            )
        ),
        "interviews": get_total_interviews(
            db,
            user_id
        )
    }


# =====================================================
# SAVED JOBS
# =====================================================

def save_job(db: Session, user_id: int, job_id: int):

    job = (
        db.query(models.JobPosting)
        .filter(models.JobPosting.job_id == job_id)
        .first()
    )

    if not job:
        return None

    return job


def get_saved_jobs(db: Session, user_id: int):
    """
    Future feature:
    Create a SavedJob table.
    """
    return []

# =====================================================
# AI USAGE
# =====================================================

def get_ai_usage(db: Session, user_id: int):

    chats = (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == user_id)
        .count()
    )

    interviews = (
        db.query(models.InterviewSession)
        .filter(models.InterviewSession.user_id == user_id)
        .count()
    )

    resume_uploaded = (
        get_resume(db, user_id)
        is not None
    )

    return {
        "chat_requests": chats,
        "mock_interviews": interviews,
        "resume_uploaded": resume_uploaded
    }

# =====================================================
# PROFILE
# =====================================================

def get_profile_summary(
    db: Session,
    user_id: int
):

    return {
        "resume": get_resume(db, user_id),
        "dashboard": get_dashboard_stats(db, user_id),
        "activity": get_user_activity(db, user_id),
        "recent": get_recent_activity(db, user_id)
    }

# =====================================================
# PROFILE
# =====================================================


# =====================================================
# SEARCH HISTORY
# =====================================================

def get_recent_searches(
    db: Session,
    user_id: int
):
    """
    Reserved for future implementation.
    """
    return []


# =====================================================
# TOP RECOMMENDATIONS
# =====================================================

def top_recommended_jobs(
    db: Session,
    user_id: int
):

    recommendations = recommend_jobs(
        db,
        user_id
    )

    return recommendations[:5]


# =====================================================
# COMPLETE DASHBOARD
# =====================================================

def dashboard_data(
    db: Session,
    user_id: int
):

    return {
        "stats": get_dashboard_stats(
            db,
            user_id
        ),
        "profile": get_profile_summary(
            db,
            user_id
        ),
        "chat": get_chat_statistics(
            db,
            user_id
        ),
        "resume": get_resume_statistics(
            db,
            user_id
        ),
        "jobs": get_job_statistics(
            db
        ),
        "interviews": get_interview_trend(
            db,
            user_id
        ),
        "recommendations": top_recommended_jobs(
            db,
            user_id
        ),
        "usage": get_ai_usage(
            db,
            user_id
        )
    }


def get_recommended_jobs(db, user_id):
    """
    Return top 10 recommended jobs based on user's skills.
    """

    # Fetch user skills
    user_skills = (
        db.query(models.UserSkill.skill)
        .filter(models.UserSkill.user_id == user_id)
        .all()
    )

    skills = [skill[0] for skill in user_skills]

    if not skills:
        return []

    filters = []

    for skill in skills:
        filters.append(models.JobPosting.title.ilike(f"%{skill}%"))
        filters.append(models.JobPosting.description.ilike(f"%{skill}%"))

    jobs = (
        db.query(models.JobPosting)
        .filter(or_(*filters))
        .limit(10)
        .all()
    )

    return jobs

def get_resume_analysis(db, user_id):
    return (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .first()
    )

    if resume:

        resume.analysis = json.dumps(analysis)

        db.commit()

        db.refresh(resume)


    def get_resume_analysis(db, user_id):
        
        
        resume = (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .first()
    )

    if not resume or not resume.analysis:
        return None

    return json.loads(resume.analysis)


def get_resume_analysis(db, user_id):
    return (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .first()
    )

def create_interview_session(db, user_id, role, difficulty):
    session = models.InterviewSession(
        user_id=user_id,
        role=role,
        difficulty=difficulty,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

def save_questions(db, session_id, questions):
    for q in questions:
        db.add(
            models.InterviewQuestion(
                session_id=session_id,
                question=q,
            )
        )

    db.commit()