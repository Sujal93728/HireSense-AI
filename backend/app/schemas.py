from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel
from pydantic import BaseModel

class CareerAssistantRequest(BaseModel):
    question: str


# ==========================
# Job Schema
# ==========================

class Job(BaseModel):
    job_id: int
    company_id: int | None = None
    company_name: str | None = None
    title: str | None = None
    description: str | None = None
    location: str | None = None
    work_type: str | None = None
    formatted_experience_level: str | None = None
    max_salary: float | None = None
    med_salary: float | None = None
    min_salary: float | None = None
    application_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


# ==========================
# Resume Builder
# ==========================

class ResumeBuilderRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    location: str
    summary: str
    skills: list[str]
    experience: str
    projects: str
    education: str


# ==========================
# Authentication
# ==========================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)



# ==========================
# AI Career Assistant
# ==========================

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str

class CareerAssistantRequest(BaseModel):
    question: str


from pydantic import BaseModel


class InterviewStartRequest(BaseModel):
    role: str
    difficulty: str


class InterviewAnswerRequest(BaseModel):
    interview_id: int
    question: str
    answer: str