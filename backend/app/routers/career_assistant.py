from fastapi import APIRouter, Depends
from ..schemas import CareerAssistantRequest
from ..career_assistant import ask_ai
from ..security import get_current_user
from ..models import User

router = APIRouter(
    prefix="/assistant",
    tags=["AI Career Assistant"]
)


@router.post("/ask")
def ask(
    request: CareerAssistantRequest,
    current_user: User = Depends(get_current_user)
):
    answer = ask_ai(
        request.question,
        "default-session"
    )

    return {
        "answer": answer
    }