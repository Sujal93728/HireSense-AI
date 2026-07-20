from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..security import get_current_user
from ..models import User
from ..schemas import ChatRequest

from .. import crud
from ..rag import retrieve_context
from ..career_assistant import ask_ai

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session_id = request.session_id

    # ---------------------------------------
    # Save User Message
    # ---------------------------------------

    crud.save_chat(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        role="user",
        message=request.message
    )

    # ---------------------------------------
    # Conversation History
    # ---------------------------------------

    history = crud.get_chat_history(
        db,
        session_id
    )

    history_text = "\n".join(
        f"{msg.role}: {msg.message}"
        for msg in history
    )

    # ---------------------------------------
    # User Resume
    # ---------------------------------------

    resume = crud.get_resume(
        db,
        current_user.id
    )

    resume_text = ""

    if resume:
        resume_text = resume.resume_text

    # ---------------------------------------
    # Retrieve Relevant Jobs (RAG)
    # ---------------------------------------

    rag_context = retrieve_context(
        request.message
    )

    # retrieve_context may return a list or a string
    if isinstance(rag_context, list):
        rag_text = "\n\n".join(rag_context)
    else:
        rag_text = rag_context

    # ---------------------------------------
    # Build AI Prompt
    # ---------------------------------------

    prompt = f"""
You are HireSense AI.

You are an expert Career Coach.

Answer professionally.

Use the user's resume whenever appropriate.

If relevant job information is available,
use it while answering.

==============================
USER RESUME
==============================

{resume_text}

==============================
RELEVANT JOB INFORMATION
==============================

{rag_text}

==============================
CONVERSATION HISTORY
==============================

{history_text}

==============================
CURRENT QUESTION
==============================

{request.message}

==============================
ASSISTANT
==============================
"""

    # ---------------------------------------
    # Ask LLM
    # ---------------------------------------

    answer = ask_ai(
        prompt,
        session_id
    )

    # ---------------------------------------
    # Save AI Response
    # ---------------------------------------

    crud.save_chat(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
        role="assistant",
        message=answer
    )

    # ---------------------------------------
    # Return Response
    # ---------------------------------------

    return {
        "response": answer,
        "resume_loaded": bool(resume),
        "rag_used": bool(rag_text.strip()),
        "session_id": session_id
    }


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_chat_history(
        db,
        current_user.id
    )


@router.delete("/history")
def clear_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    crud.clear_user_chat(
        db,
        current_user.id
    )

    return {
        "message": "Chat history cleared successfully."
    }