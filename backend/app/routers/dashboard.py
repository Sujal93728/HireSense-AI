from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..security import get_current_user
from .. import crud

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    analysis = crud.get_resume_analysis(
        db,
        current_user.id
    )

    if analysis:
        resume_score = 100  # Replace with actual calculation later
        missing_skills = []
        recommendations = [analysis.analysis] if analysis.analysis else []
    else:
        resume_score = 0
        missing_skills = []
        recommendations = []

    return {
        "resume_score": resume_score,
        "missing_skills": missing_skills,
        "recommendations": recommendations,

        "average_score": crud.get_average_score(
            db,
            current_user.id
        ),

        "best_score": crud.get_best_score(
            db,
            current_user.id
        ),

        "total_interviews": crud.get_total_interviews(
            db,
            current_user.id
        ),

        "recent_interviews": crud.get_recent_interviews(
            db,
            current_user.id
        ),

        "recommended_jobs": crud.get_job_recommendations(
            db,
            current_user.id
        )
    }