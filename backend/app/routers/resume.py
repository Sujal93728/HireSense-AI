from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import pdfplumber
import os
from ..dependencies import get_db
from .. import crud
from ..resume_matcher import match_resume
from ..resume_analyzer import analyze_resume
from ..skill_extractor import compare_skills
from ..career_roadmap import generate_roadmap
from ..job_recommender import recommend_jobs
from ..interview_generator import generate_questions
from ..cover_letter import generate_cover_letter
from ..resume_builder import build_resume
from ..schemas import ResumeBuilderRequest
from fastapi.responses import FileResponse
from ..pdf_resume import create_resume_pdf

from ..dependencies import get_db
from ..security import get_current_user
from ..models import User
from .. import crud
from ..resume_ai import analyze_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

LAST_RESUME_TEXT = ""


# =====================================
# Upload Resume
# =====================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    resume_text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

        analysis = analyze_resume(resume_text)

    crud.save_resume(
        db,
        current_user.id,
        resume_text
    )

    crud.save_resume_analysis(
    db,
    current_user.id,
    analysis,
)

    return {
        "success": True,
        "message": "Resume uploaded successfully.",
        "filename": file.filename
    }


# =====================================
# Skill Gap Analysis
# =====================================

@router.get("/skill-gap/{job_id}")
def skill_gap(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    global LAST_RESUME_TEXT

    if LAST_RESUME_TEXT == "":
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume first."
        )

    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return compare_skills(
        LAST_RESUME_TEXT,
        job.description or ""
    )


# =====================================
# Career Roadmap
# =====================================

@router.get("/career-roadmap/{job_id}")
def career_roadmap(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    global LAST_RESUME_TEXT

    if LAST_RESUME_TEXT == "":
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume first."
        )

    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    skill_gap = compare_skills(
        LAST_RESUME_TEXT,
        job.description or ""
    )

    roadmap = generate_roadmap(
        skill_gap["missing_skills"]
    )

    return {
        "score": skill_gap["score"],
        "matched_skills": skill_gap["matched_skills"],
        "missing_skills": skill_gap["missing_skills"],
        "roadmap": roadmap["roadmap"],
        "estimated_days": roadmap["estimated_days"],
        "career_readiness": roadmap["career_readiness"]
    }


# =====================================
# AI Interview Questions
# =====================================

@router.get("/interview/{job_id}")
def interview_questions(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    skills = compare_skills(
        "",
        job.description or ""
    )

    return generate_questions(
        skills["missing_skills"]


    )

@router.get("/cover-letter/{job_id}")
def cover_letter(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    global LAST_RESUME_TEXT

    if LAST_RESUME_TEXT == "":
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume first."
        )

    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    analysis = analyze_resume(LAST_RESUME_TEXT)

    return generate_cover_letter(job, analysis)


# =====================================
# AI Resume Builder
# =====================================

@router.post("/build-resume")
def build_resume_api(data: ResumeBuilderRequest):

    filepath = create_resume_pdf(data.model_dump())

    return FileResponse(
        path=filepath,
        filename="Resume.pdf",
        media_type="application/pdf"
    )