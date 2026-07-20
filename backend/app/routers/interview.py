from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..security import get_current_user
from ..models import User
from ..schemas import (
    InterviewStartRequest,
    InterviewAnswerRequest,
)
from .. import crud
from ..interview_ai import (
    generate_interview_question,
    evaluate_answer,
)

router = APIRouter(
    prefix="/interview",
    tags=["AI Interview"]
)


# =====================================================
# Start Interview
# =====================================================

@router.post("/start")
def start_interview(
    request: InterviewStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interview = crud.create_interview(
        db=db,
        user_id=current_user.id,
        role=request.role,
        difficulty=request.difficulty
    )

    question = generate_interview_question(
        request.role,
        request.difficulty
    )

    return {
        "message": "Interview started successfully.",
        "interview_id": interview.id,
        "question": question
    }


# =====================================================
# Submit Answer
# =====================================================

@router.post("/answer")
def submit_answer(
    request: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # AI Evaluation
    result = evaluate_answer(
        request.question,
        request.answer
    )

    score = result.get("score", 5)

    strengths = result.get("strengths", [])
    weaknesses = result.get("weaknesses", [])
    suggestions = result.get("suggestions", [])

    feedback = f"""
Strengths:
{chr(10).join(strengths)}

Weaknesses:
{chr(10).join(weaknesses)}

Suggestions:
{chr(10).join(suggestions)}
"""

    crud.save_interview_answer(
        db=db,
        interview_id=request.interview_id,
        question=request.question,
        user_answer=request.answer,
        ai_feedback=feedback,
        score=score
    )

    overall_score = crud.update_interview_score(
        db,
        request.interview_id
    )

    return {
        "score": score,
        "overall_score": overall_score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "feedback": feedback
    }


# =====================================================
# Interview History
# =====================================================

@router.get("/history")
def interview_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_interviews(
        db,
        current_user.id
    )


# =====================================================
# Interview Details
# =====================================================

@router.get("/{interview_id}")
def interview_details(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_interview_questions(
        db,
        interview_id
    )


# =====================================================
# Delete Interview
# =====================================================

@router.delete("/{interview_id}")
def delete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    crud.delete_interview(
        db,
        interview_id
    )

    return {
        "message": "Interview deleted successfully."
    }