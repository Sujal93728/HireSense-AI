from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..security import get_current_user
from ..models import User
from .. import crud

router = APIRouter(
    prefix="/resume-ai",
    tags=["AI Resume"]
)


@router.get("/analyze")
def analyze(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return crud.analyze_resume_ai(
        db,
        current_user.id
    )