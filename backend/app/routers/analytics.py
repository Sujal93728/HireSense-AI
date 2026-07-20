from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..security import get_current_user
from ..models import User
from .. import crud

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "average_score": crud.get_average_interview_score(
            db,
            current_user.id
        ),
        "best_score": crud.get_best_interview_score(
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
        )
    }