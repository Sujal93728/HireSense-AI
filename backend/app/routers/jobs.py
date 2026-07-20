from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas
from ..salary_predictor import predict_salary
from ..interview_generator import generate_questions

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get("/", response_model=list[schemas.Job])
def get_jobs(db: Session = Depends(get_db)):
    return crud.get_jobs(db)


@router.get("/{job_id}", response_model=schemas.Job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


@router.get("/{job_id}/salary")
def salary_prediction(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return predict_salary(job)


@router.get("/{job_id}/interview-questions")
def interview_questions(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = crud.get_job_by_id(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    questions = generate_questions(job.description or "")

    return {
        "job_title": job.title,
        "questions": questions
    }